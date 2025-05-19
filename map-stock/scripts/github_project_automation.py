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

# Mapeo de palabras clave a campos adicionales
FIELD_MAP = {
    'priority': {
        'field_name': 'Priority',
        'values': ['P0', 'P1', 'P2']
    },
    'size': {
        'field_name': 'Size',
        'values': ['XS', 'S', 'M', 'L', 'XL']
    }
}

class GitHubProjectAutomation:
    def __init__(self):
        if not GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN no encontrado en las variables de entorno")
        
        self.debug_mode = False  # Agregar flag para modo debug
        
        # Configurar el cliente GraphQL
        transport = AIOHTTPTransport(
            url='https://api.github.com/graphql',
            headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
            ssl=True  # Habilitar verificación SSL
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.repository_id = None

    def set_debug_mode(self, message: str) -> None:
        """Activa o desactiva el modo debug basado en el mensaje"""
        self.debug_mode = "#debug-hook" in message.lower()

    def debug_print(self, message: str) -> None:
        """Imprime mensajes solo si estamos en modo debug"""
        if self.debug_mode:
            print(message)

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
            print("\nGitHub connection successful")
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
            
            self.debug_print("\nProyectos disponibles en el repositorio:")
            if projects:
                for project in projects:
                    self.debug_print(f"- Proyecto #{project['number']}: {project['title']} (ID: {project['id']})")
            else:
                self.debug_print("No se encontraron proyectos en el repositorio")
        except Exception as e:
            self.debug_print(f"\nError al listar proyectos: {str(e)}")
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
            self.debug_print("\nInformación del repositorio:")
            self.debug_print(f"- Nombre: {result['repository']['name']}")
            self.debug_print(f"- Propietario: {result['repository']['owner']['login']}")
            
            if result['repository']['projectV2']:
                project = result['repository']['projectV2']
                self.debug_print(f"\nInformación del proyecto:")
                self.debug_print(f"- ID: {project['id']}")
                self.debug_print(f"- Título: {project['title']}")
                self.debug_print(f"- Número: {project['number']}")
                self.debug_print("\nCampos encontrados:")
                for field in project['fields']['nodes']:
                    self.debug_print(f"- {field['name']}")
                    if 'options' in field:
                        self.debug_print("  Opciones:")
                        for option in field['options']:
                            self.debug_print(f"  - {option['name']}")
            else:
                self.debug_print("\nNo se encontró el proyecto. Verifica:")
                self.debug_print("1. El número del proyecto es correcto")
                self.debug_print("2. El proyecto está en el repositorio correcto")
                self.debug_print("3. El token tiene permisos para acceder al proyecto")
            
            return result
        except Exception as e:
            self.debug_print(f"\nError al obtener información del proyecto: {str(e)}")
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
                self.debug_print(f"\nError: La issue #{issue_number} no existe en el repositorio {REPO_OWNER}/{REPO_NAME}")
                self.debug_print("Por favor, crea la issue primero o usa un número de issue válido.")
                raise ValueError(f"No se encontró la issue #{issue_number}")
            
            issue = result['repository']['issue']
            self.debug_print(f"\nIssue encontrada:")
            self.debug_print(f"- Título: {issue['title']}")
            self.debug_print(f"- Estado: {issue['state']}")
            return issue['id']
        except Exception as e:
            if "Could not resolve to an Issue" in str(e):
                self.debug_print(f"\nError: La issue #{issue_number} no existe en el repositorio {REPO_OWNER}/{REPO_NAME}")
                self.debug_print("Por favor, crea la issue primero o usa un número de issue válido.")
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
                query($owner: String!, $repo: String!, $projectNumber: Int!) {
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
                "projectNumber": PROJECT_NUMBER
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

    def find_field_values(self, message: str) -> Dict[str, str]:
        """Encuentra los valores de los campos en el mensaje del commit"""
        field_values = {}
        
        # Buscar valores de campos con formato #campo:valor
        for field, config in FIELD_MAP.items():
            pattern = f"#{field}:([A-Za-z0-9]+)"
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                value = match.group(1).upper()
                if value in config['values']:
                    field_values[field] = value
        
        # Buscar fechas con formato #start:YYYY-MM-DD o #end:YYYY-MM-DD
        date_patterns = {
            'Start date': r"#start:(\d{4}-\d{2}-\d{2})",
            'End date': r"#end:(\d{4}-\d{2}-\d{2})"
        }
        
        for field, pattern in date_patterns.items():
            match = re.search(pattern, message)
            if match:
                field_values[field] = match.group(1)
        
        # Buscar estimación con formato #estimate:N
        estimate_match = re.search(r"#estimate:(\d+)", message)
        if estimate_match:
            field_values['estimate'] = estimate_match.group(1)
        
        return field_values

    async def update_issue_fields(self, issue_number: str, field_values: Dict[str, str]) -> None:
        """Actualiza los campos adicionales de una issue"""
        if not field_values:
            return
        
        # Obtener información del proyecto y sus campos
        query = gql("""
            query($owner: String!, $repo: String!, $projectNumber: Int!) {
                repository(owner: $owner, name: $repo) {
                    projectV2(number: $projectNumber) {
                        id
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
                                ... on ProjectV2IterationField {
                                    id
                                    name
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
        project = result['repository']['projectV2']
        
        # Obtener el ID del item del proyecto
        get_item_query = gql("""
            query($owner: String!, $repo: String!, $projectNumber: Int!) {
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
            "projectNumber": PROJECT_NUMBER
        }
        
        get_item_result = await self.client.execute_async(get_item_query, variable_values=get_item_variables)
        project_item_id = None
        
        for item in get_item_result['repository']['projectV2']['items']['nodes']:
            if item['content']['number'] == int(issue_number):
                project_item_id = item['id']
                break
        
        if not project_item_id:
            raise ValueError(f"No se pudo encontrar la issue #{issue_number} en el proyecto")
        
        # Actualizar cada campo
        for field_name, field_value in field_values.items():
            field_id = None
            field_type = None
            
            # Buscar el campo en el proyecto
            for field in project['fields']['nodes']:
                if field['name'] == FIELD_MAP.get(field_name, {}).get('field_name', field_name):
                    field_id = field['id']
                    if 'options' in field:
                        field_type = 'singleSelect'
                    elif field_name in ['Start date', 'End date']:
                        field_type = 'date'
                    elif field_name == 'Estimate':
                        field_type = 'text'
                    break
            
            if not field_id:
                print(f"Campo {field_name} no encontrado en el proyecto")
                continue
            
            # Preparar la mutación según el tipo de campo
            if field_type == 'singleSelect':
                # Buscar el ID de la opción
                option_id = None
                for field in project['fields']['nodes']:
                    if field['id'] == field_id:
                        for option in field['options']:
                            if option['name'] == field_value:
                                option_id = option['id']
                                break
                        break
                
                if not option_id:
                    print(f"Opción {field_value} no encontrada para el campo {field_name}")
                    continue
                
                mutation = gql("""
                    mutation($input: UpdateProjectV2ItemFieldValueInput!) {
                        updateProjectV2ItemFieldValue(input: $input) {
                            projectV2Item {
                                id
                            }
                        }
                    }
                """)
                
                variables = {
                    "input": {
                        "projectId": project['id'],
                        "itemId": project_item_id,
                        "fieldId": field_id,
                        "value": {
                            "singleSelectOptionId": option_id
                        }
                    }
                }
            
            elif field_type == 'date':
                mutation = gql("""
                    mutation($input: UpdateProjectV2ItemFieldValueInput!) {
                        updateProjectV2ItemFieldValue(input: $input) {
                            projectV2Item {
                                id
                            }
                        }
                    }
                """)
                
                variables = {
                    "input": {
                        "projectId": project['id'],
                        "itemId": project_item_id,
                        "fieldId": field_id,
                        "value": {
                            "date": field_value
                        }
                    }
                }
            
            elif field_type == 'text':
                mutation = gql("""
                    mutation($input: UpdateProjectV2ItemFieldValueInput!) {
                        updateProjectV2ItemFieldValue(input: $input) {
                            projectV2Item {
                                id
                            }
                        }
                    }
                """)
                
                variables = {
                    "input": {
                        "projectId": project['id'],
                        "itemId": project_item_id,
                        "fieldId": field_id,
                        "value": {
                            "text": field_value
                        }
                    }
                }
            
            try:
                await self.client.execute_async(mutation, variable_values=variables)
                print(f"Campo {field_name} actualizado a {field_value}")
            except Exception as e:
                print(f"Error al actualizar el campo {field_name}: {str(e)}")

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
            self.debug_print(f"\nIssue creada exitosamente:")
            self.debug_print(f"- Número: #{issue['number']}")
            self.debug_print(f"- Título: {issue['title']}")
            return f"#{issue['number']}"  # Devolver el número de la issue con el #
        except Exception as e:
            self.debug_print(f"\nError al crear la issue: {str(e)}")
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
    
    # Configurar modo debug
    automation.set_debug_mode(message)
    
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
        automation.debug_print(f"No se encontró el proyecto #{PROJECT_NUMBER}")
        return
    
    # Extraer número de issue, palabra clave y valores de campos
    issue_number = automation.extract_issue_number(message)
    keyword = automation.find_keyword(message)
    field_values = automation.find_field_values(message)
    
    if not keyword and not field_values:
        automation.debug_print("No se encontró palabra clave ni campos para actualizar en el mensaje")
        return
    
    try:
        if not issue_number:
            # Si no hay número de issue, crear una nueva
            title = message.split('#')[0].strip()  # Usar el mensaje como título
            result = await automation.create_issue(title)
            # Extraer el número de la issue del resultado
            issue_number = result.split('#')[1].split()[0]  # Obtener el número después del #
            automation.debug_print(f"Usando issue #{issue_number}")
        else:
            # Verificar si la issue existe
            await automation.get_issue_node_id(issue_number)
        
        # Mover la issue si hay palabra clave
        if keyword:
            await automation.move_issue_to_column(issue_number, COLUMN_MAP[keyword])
            print(f"Issue #{issue_number} movida a {COLUMN_MAP[keyword]}")
        
        # Actualizar campos adicionales si hay valores
        if field_values:
            await automation.update_issue_fields(issue_number, field_values)
            
    except Exception as e:
        automation.debug_print(f"Error al procesar la issue: {str(e)}")

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