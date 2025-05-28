import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>Map Stock</h1>
      </div>
      
      <div className="navbar-menu">
        <ul className="navbar-nav">
          <li className="nav-item">
            <a href="/" className="nav-link">Inicio</a>
          </li>
          <li className="nav-item">
            <a href="/products" className="nav-link">Productos</a>
          </li>
          <li className="nav-item">
            <a href="/inventory" className="nav-link">Inventario</a>
          </li>
        </ul>
      </div>

      <div className="navbar-end">
        <button className="btn-primary">Nuevo Producto</button>
      </div>
    </nav>
  );
};

export default Navbar; 