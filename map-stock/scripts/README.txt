GitHub Projects Automation
=========================

Este script permite automatizar la gestión de issues en GitHub Projects, permitiendo crear nuevas issues y moverlas entre columnas usando palabras clave en los mensajes de commit.

Palabras Clave
-------------
- #backlog  -> Mueve la issue a la columna "Backlog"
- #ready    -> Mueve la issue a la columna "Ready"
- #in-progress -> Mueve la issue a la columna "In progress"
- #review   -> Mueve la issue a la columna "In review"
- #done     -> Mueve la issue a la columna "Done"

Uso
---
1. Crear una nueva issue:
   ```bash
   python3 github_project_automation.py "Implementar nueva funcionalidad #in-progress"
   ```

2. Mover una issue existente:
   ```bash
   python3 github_project_automation.py "Actualización de documentación #done #123"
   ```

Ejemplos
--------
1. Crear una nueva issue y moverla a "In progress":
   ```bash
   python3 github_project_automation.py "Implementar sistema de autenticación #in-progress"
   ```

2. Mover una issue existente a "Done":
   ```bash
   python3 github_project_automation.py "Completar tarea #done #456"
   ```

3. Crear una issue y moverla a "Backlog":
   ```bash
   python3 github_project_automation.py "Nueva idea para implementar #backlog"
   ```

Notas
-----
- El script requiere un token de GitHub con permisos para gestionar issues y proyectos
- El token debe estar configurado en el archivo .env
- Las columnas deben existir en el proyecto de GitHub
- El número del proyecto debe estar configurado en el script 