import { createContext, useContext, useState, useEffect } from 'react';
import client from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('nhatki_token');
    if (!token) { setLoading(false); return; }
    client.get('/api/auth/me')
      .then(res => setUser(res.data))
      .catch(() => localStorage.removeItem('nhatki_token'))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const res = await client.post('/api/auth/login', { email, password });
    localStorage.setItem('nhatki_token', res.data.access_token);
    const me = await client.get('/api/auth/me');
    setUser(me.data);
  }

  async function register(email, username, password, display_name) {
    await client.post('/api/auth/register', { email, username, password, display_name });
    await login(email, password);
  }

  function logout() {
    localStorage.removeItem('nhatki_token');
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
