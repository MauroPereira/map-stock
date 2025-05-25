# Componentes del Frontend

## Navbar.js
- Es la barra de navegación superior de la aplicación
- Contiene:
  - Logo de la aplicación
  - Menú de navegación
  - Botones de acción principales
  - Información del usuario (si hay autenticación)

## ProductList.js
- Es el componente que muestra la lista de productos
- Funcionalidades:
  - Muestra todos los productos en una lista
  - Maneja la paginación
  - Filtros de búsqueda
  - Ordenamiento
- Es el "contenedor" que organiza cómo se muestran los productos

## ProductCard.js
- Es el componente individual para cada producto
- Muestra:
  - Imagen del producto
  - Nombre
  - Precio
  - Stock
  - Botones de acción (editar, eliminar, etc.)
- Es reutilizado dentro de ProductList.js

## Estructura de Componentes
```
Navbar.js
    │
    └── ProductList.js
            │
            └── ProductCard.js (múltiples instancias)
``` 