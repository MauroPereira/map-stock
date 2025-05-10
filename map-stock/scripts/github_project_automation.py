#!/usr/bin/env python3
import os
import sys
from typing import Dict, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
import re
import json

# Cargar variables de entorno
load_dotenv()

# Configuración
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
PROJECT_NUMBER = 8  # Reemplazar con tu número de proyecto
REPO_OWNER = "MauroPereira"  # Reemplazar con tu nombre de usuario/organización
REPO_NAME = "map-stock"  # Reemplazar con el nombre de tu repositorio

# Mapeo de palabras clave a columnas
COLUMN_MAP = {
    '#backlog': 'Backlog',
    '#ready': 'Ready',
    '#in-progress': 'In progress',  # Nota: cambiado a minúscula para coincidir con la API
    '#review': 'In review',         # Nota: cambiado a minúscula para coincidir con la API
    '#done': 'Done'
}

class GitHubProjectAutomation:
    def __init__(self):
        if not GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN no encontrado en las variables de entorno")
        
        print(f"Configurando cliente GraphQL con:")
        print(f"- Repositorio: {REPO_OWNER}/{REPO_NAME}")
        print(f"- Número de proyecto: {PROJECT_NUMBER}")
        print(f"- Token (primeros 4 caracteres): {GITHUB_TOKEN[:4]}...")
        
        # Configurar el cliente GraphQL
        transport = AIOHTTPTransport(
            url='https://api.github.com/graphql',
            headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
            ssl=True  # Habilitar verificación SSL
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.repository_id = None

    async def verify_connection(self) -> None:
        """Verifica la conexión con GitHub y los permisos del token"""
        query = gql("""
            query {
                viewer {
                    login
                    name
                }
            }
        """)
        
        try:
            result = await self.client.execute_async(query)
            print("\nConexión exitosa con GitHub:")
            print(f"- Usuario autenticado: {result['viewer']['login']}")
            print(f"- Nombre: {result['viewer']['name']}")
        except Exception as e:
            print(f"\nError al conectar con GitHub: {str(e)}")
            raise

    async def list_projects(self) -> None:
        """Lista todos los proyectos disponibles en el repositorio"""
        query = gql("""
            query($owner: String!, $repo: String!) {
                repository(owner: $owner, name: $repo) {
                    projectsV2(first: 10) {
                        nodes {
                            id
                            title
                            number
                        }
                    }
                }
            }
        """)
        
        variables = {
            "owner": REPO_OWNER,
            "repo": REPO_NAME
        }
        
        try:
            result = await self.client.execute_async(query, variable_values=variables)
            projects = result['repository']['projectsV2']['nodes']
            
            print("\nProyectos disponibles en el repositorio:")
            if projects:
                for project in projects:
                    print(f"- Proyecto #{project['number']}: {project['title']} (ID: {project['id']})")
            else:
                print("No se encontraron proyectos en el repositorio")
        except Exception as e:
            print(f"\nError al listar proyectos: {str(e)}")
            raise

    async def get_project_info(self) -> Dict:
        """Obtiene información del proyecto y sus columnas"""
        query = gql("""
            query($owner: String!, $repo: String!, $projectNumber: Int!) {
                repository(owner: $owner, name: $repo) {
                    name
                    owner {
                        login
                    }
                    projectV2(number: $projectNumber) {
                        id
                        title
                        number
                        fields(first: 20) {
                            nodes {
                                ... on ProjectV2Field {
                                    id
                                    name
                                }
                                ... on ProjectV2SingleSelectField {
                                    id
                                    name
                                    options {
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """)
        
        variables = {
            "owner": REPO_OWNER,
            "repo": REPO_NAME,
            "projectNumber": PROJECT_NUMBER
        }
        
        try:
            result = await self.client.execute_async(query, variable_values=variables)
            print("\nInformación del repositorio:")
            print(f"- Nombre: {result['repository']['name']}")
            print(f"- Propietario: {result['repository']['owner']['login']}")
            
            if result['repository']['projectV2']:
                project = result['repository']['projectV2']
                print(f"\nInformación del proyecto:")
                print(f"- ID: {project['id']}")
                print(f"- Título: {project['title']}")
                print(f"- Número: {project['number']}")
                print("\nCampos encontrados:")
                for field in project['fields']['nodes']:
                    print(f"- {field['name']}")
                    if 'options' in field:
                        print("  Opciones:")
                        for option in field['options']:
                            print(f"  - {option['name']}")
            else:
                print("\nNo se encontró el proyecto. Verifica:")
                print("1. El número del proyecto es correcto")
                print("2. El proyecto está en el repositorio correcto")
                print("3. El token tiene permisos para acceder al proyecto")
            
            return result
        except Exception as e:
            print(f"\nError al obtener información del proyecto: {str(e)}")
            raise

    async def get_issue_node_id(self, issue_number: str) -> str:
        """Obtiene el Node ID de una issue"""
        query = gql("""
            query($owner: String!, $repo: String!, $issueNumber: Int!) {
                repository(owner: $owner, name: $repo) {
                    issue(number: $issueNumber) {
                        id
                        title
                        state
                    }
                }
            }
        """)
        
        variables = {
            "owner": REPO_OWNER,
            "repo": REPO_NAME,
            "issueNumber": int(issue_number)
        }
        
        try:
            result = await self.client.execute_async(query, variable_values=variables)
            if not result['repository']['issue']:
                print(f"\nError: La issue #{issue_number} no existe en el repositorio {REPO_OWNER}/{REPO_NAME}")
                print("Por favor, crea la issue primero o usa un número de issue válido.")
                raise ValueError(f"No se encontró la issue #{issue_number}")
            
            issue = result['repository']['issue']
            print(f"\nIssue encontrada:")
            print(f"- Título: {issue['title']}")
            print(f"- Estado: {issue['state']}")
            return issue['id']
        except Exception as e:
            if "Could not resolve to an Issue" in str(e):
                print(f"\nError: La issue #{issue_number} no existe en el repositorio {REPO_OWNER}/{REPO_NAME}")
                print("Por favor, crea la issue primero o usa un número de issue válido.")
            raise

    async def move_issue_to_column(self, issue_number: str, status_value: str) -> None:
        """Mueve una issue a un estado específico"""
        # Primero obtenemos el ID del campo de estado
        query = gql("""
            query($owner: String!, $repo: String!, $projectNumber: Int!) {
                repository(owner: $owner, name: $repo) {
                    projectV2(number: $projectNumber) {
                        id
                        fields(first: 20) {
                            nodes {
                                ... on ProjectV2SingleSelectField {
                                    id
                                    name
                                    options {
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """)
        
        variables = {
            "owner": REPO_OWNER,
            "repo": REPO_NAME,
            "projectNumber": PROJECT_NUMBER
        }
        
        result = await self.client.execute_async(query, variable_values=variables)
        status_field = None
        status_option = None
        
        # Buscar el campo Status y su opción correspondiente
        for field in result['repository']['projectV2']['fields']['nodes']:
            if isinstance(field, dict) and field.get('name') == 'Status':
                status_field = field
                for option in field.get('options', []):
                    if option.get('name') == status_value:
                        status_option = option
                        break
                break
        
        if not status_field or not status_option:
            raise ValueError(f"No se encontró el campo Status o la opción {status_value}")
        
        # Obtener el Node ID de la issue
        issue_node_id = await self.get_issue_node_id(issue_number)
        
        # Primero, agregar la issue al proyecto si no está
        add_item_mutation = gql("""
            mutation($input: AddProjectV2ItemByIdInput!) {
                addProjectV2ItemById(input: $input) {
                    item {
                        id
                    }
                }
            }
        """)
        
        add_item_variables = {
            "input": {
                "projectId": result['repository']['projectV2']['id'],
                "contentId": issue_node_id
            }
        }
        
        try:
            add_result = await self.client.execute_async(add_item_mutation, variable_values=add_item_variables)
            project_item_id = add_result['addProjectV2ItemById']['item']['id']
        except Exception as e:
            # Si la issue ya está en el proyecto, obtener su ID
            get_item_query = gql("""
                query($owner: String!, $repo: String!, $projectNumber: Int!, $issueNumber: Int!) {
                    repository(owner: $owner, name: $repo) {
                        projectV2(number: $projectNumber) {
                            items(first: 100) {
                                nodes {
                                    id
                                    content {
                                        ... on Issue {
                                            number
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            """)
            
            get_item_variables = {
                "owner": REPO_OWNER,
                "repo": REPO_NAME,
                "projectNumber": PROJECT_NUMBER,
                "issueNumber": int(issue_number)
            }
            
            get_item_result = await self.client.execute_async(get_item_query, variable_values=get_item_variables)
            for item in get_item_result['repository']['projectV2']['items']['nodes']:
                if item['content']['number'] == int(issue_number):
                    project_item_id = item['id']
                    break
            else:
                raise ValueError(f"No se pudo encontrar la issue #{issue_number} en el proyecto")
        
        # Actualizamos el estado de la issue
        update_mutation = gql("""
            mutation($input: UpdateProjectV2ItemFieldValueInput!) {
                updateProjectV2ItemFieldValue(input: $input) {
                    projectV2Item {
                        id
                    }
                }
            }
        """)
        
        update_variables = {
            "input": {
                "projectId": result['repository']['projectV2']['id'],
                "itemId": project_item_id,
                "fieldId": status_field['id'],
                "value": {
                    "singleSelectOptionId": status_option['id']
                }
            }
        }
        
        await self.client.execute_async(update_mutation, variable_values=update_variables)

    def extract_issue_number(self, message: str) -> Optional[str]:
        """Extrae el número de issue del mensaje del commit"""
        match = re.search(r'#(\d+)', message)
        return match.group(1) if match else None

    def find_keyword(self, message: str) -> Optional[str]:
        """Encuentra la palabra clave en el mensaje del commit"""
        message_lower = message.lower()
        for keyword in COLUMN_MAP.keys():
            if keyword in message_lower:
                return keyword
        return None

    async def create_issue(self, title: str, body: str = "") -> str:
        """Crea una nueva issue en el repositorio"""
        mutation = gql("""
            mutation($input: CreateIssueInput!) {
                createIssue(input: $input) {
                    issue {
                        id
                        number
                        title
                    }
                }
            }
        """)
        
        variables = {
            "input": {
                "repositoryId": self.repository_id,
                "title": title,
                "body": body
            }
        }
        
        try:
            result = await self.client.execute_async(mutation, variable_values=variables)
            issue = result['createIssue']['issue']
            print(f"\nIssue creada exitosamente:")
            print(f"- Número: #{issue['number']}")
            print(f"- Título: {issue['title']}")
            return f"#{issue['number']}"  # Devolver el número de la issue con el #
        except Exception as e:
            print(f"\nError al crear la issue: {str(e)}")
            raise

    async def get_repository_id(self) -> str:
        """Obtiene el ID del repositorio"""
        query = gql("""
            query($owner: String!, $repo: String!) {
                repository(owner: $owner, name: $repo) {
                    id
                }
            }
        """)
        
        variables = {
            "owner": REPO_OWNER,
            "repo": REPO_NAME
        }
        
        result = await self.client.execute_async(query, variable_values=variables)
        return result['repository']['id']

async def process_commit_message(message: str) -> None:
    """Procesa un mensaje de commit y mueve la issue si es necesario"""
    automation = GitHubProjectAutomation()
    
    # Verificar conexión
    await automation.verify_connection()
    
    # Obtener el ID del repositorio
    automation.repository_id = await automation.get_repository_id()
    
    # Listar proyectos disponibles
    await automation.list_projects()
    
    # Obtener información del proyecto
    project_info = await automation.get_project_info()
    project = project_info['repository']['projectV2']
    
    if not project:
        print(f"No se encontró el proyecto #{PROJECT_NUMBER}")
        return
    
    # Extraer número de issue y palabra clave
    issue_number = automation.extract_issue_number(message)
    keyword = automation.find_keyword(message)
    
    if not keyword:
        print("No se encontró palabra clave en el mensaje")
        return
    
    try:
        if not issue_number:
            # Si no hay número de issue, crear una nueva
            title = message.split('#')[0].strip()  # Usar el mensaje como título
            result = await automation.create_issue(title)
            # Extraer el número de la issue del resultado
            issue_number = result.split('#')[1].split()[0]  # Obtener el número después del #
            print(f"Usando issue #{issue_number}")
        else:
            # Verificar si la issue existe
            await automation.get_issue_node_id(issue_number)
        
        # Mover la issue
        await automation.move_issue_to_column(issue_number, COLUMN_MAP[keyword])
        print(f"Issue #{issue_number} movida a {COLUMN_MAP[keyword]}")
    except Exception as e:
        print(f"Error al procesar la issue: {str(e)}")

if __name__ == "__main__":
    import asyncio
    
    if len(sys.argv) < 2:
        print("Uso: python3 github_project_automation.py 'mensaje del commit'")
        print("Ejemplo: python3 github_project_automation.py 'Implementación de nueva funcionalidad #in-progress'")
        print("Opciones:")
        print("1. Crear nueva issue: 'Título de la issue #in-progress'")
        print("2. Mover issue existente: 'Título #in-progress #123'")
        sys.exit(1)
    
    commit_message = sys.argv[1]
    asyncio.run(process_commit_message(commit_message)) 