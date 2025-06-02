import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Login from './components/Login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = (credentials) => {
    // TODO: Implementar la lógica de autenticación con el backend
    console.log('Login attempt with:', credentials);
    // Por ahora, solo simulamos un login exitoso
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <Navbar onLogout={() => setIsAuthenticated(false)} />
      <main className="App-main">
        <h2>Bienvenido a Map Stock</h2>
      </main>
    </div>
  );
}

export default App; 