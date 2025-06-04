
# PIN2_public
## Objetivo

GH Actions - apache – AWS

El objetivo de este PIN, será utilizar github actions para desplegar un apache
en una ec2 de terraform.

Para esto pueden utilizar de ayuda el Repositorio:

https://github.com/tercemundo/gh-tf-mio

# Terraform AWS Webserver Setup

Este proyecto usa **Terraform** para crear y configurar una infraestructura básica en **AWS**. La infraestructura incluye una **VPC**, **subred**, **Internet Gateway**, una **instancia EC2** con Apache, y la configuración del backend para el estado de Terraform en **S3** con bloqueo mediante **DynamoDB**.

## Requisitos

- **Terraform** instalado.
- Una cuenta en **AWS** con permisos suficientes para crear recursos como VPC, EC2, S3, DynamoDB, etc.
- El archivo de configuración `aws_access_key_id` y `aws_secret_access_key` configurado en tu entorno o en el archivo `~/.aws/credentials`.

## Estructura del Proyecto

Este proyecto se divide en varios archivos que describen cómo se deben crear los recursos de AWS.

### Archivos principales:
- **`create_and_destroy_backend.tf`**: A través de un backend local crea una estructura de backend en AWS.
- **`setup.tf`**: Define los recursos básicos de infraestructura, como VPC, Internet Gateway, subred y grupo de seguridad.
- **`main.tf`**: Crea y configura la instancia EC2 y asigna el script de configuración de Apache.
- **`backend.tf`**: Configura el backend remoto para almacenar el estado de Terraform en S3 y utiliza DynamoDB para el bloqueo del estado.
- **`create_apache.sh`**: Script que se ejecuta cuando la instancia EC2 se lanza, instalando y habilitando Apache.

## Recursos creados

1. **S3 y DynamoDB**: Almacenar el backend de terraform para la creación de los demás recursos en AWS que se mencionan en los siguientes puntos.
2. **VPC**: Crea una red privada con el bloque CIDR `10.0.0.0/16`.
3. **Internet Gateway (IGW)**: Proporciona acceso a Internet para los recursos dentro de la VPC.
4. **Tabla de Rutas**: Se configura una ruta predeterminada que permite el acceso a Internet usando el Internet Gateway.
5. **Subred**: Crea una subred con el bloque CIDR `10.0.1.0/24`.
6. **Security Group**: Permite el tráfico entrante en los puertos `22` (SSH) y `80` (HTTP).
7. **Instancia EC2 (Web Server)**: Lanza una instancia de Amazon Linux 2 con Apache instalado y configurado para iniciar automáticamente.
8. **Backend de Terraform**: El estado de Terraform se almacena en un bucket de S3, y el bloqueo de estado se gestiona mediante DynamoDB.

## Organización
Se tienen dos carpetas con archivos para ejecutar terraform **create_or_destroy_backend** (Recursos creados 1) y **pin2** para los demás recursos. **polities** es el archivo yaml con los permisos que se asocian al usuario de AWS para poder crear todos los recursos. **doc_files** incluye material de documentación.

