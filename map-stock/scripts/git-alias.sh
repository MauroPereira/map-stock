#!/bin/bash

# Crear el alias de git
git config --local alias.commit-auto '!f() { python3 map-stock/scripts/github_project_automation.py "$1" && git commit -m "$1"; }; f'

echo "Alias creado. Ahora puedes usar:"
echo "git commit-auto 'Implementar sistema de autenticación #in-progress'"

# Copiar el hook al directorio .git/hooks
cp map-stock/scripts/pre-commit .git/hooks/

# Luego simplemente usa git commit normal:
git commit -m "Implementar sistema de autenticación #in-progress" 