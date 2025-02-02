import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import axios from 'axios';

// Define User interface
interface User {
  id?: number;
  username: string;
  email: string;
  isAdmin?: boolean;
}

// Define AuthContext type
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const login = async (username: string, password: string) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('/api/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      const { access_token } = response.data;

      // Decode token to get user info (assuming JWT)
      const tokenParts = access_token.split('.');
      if (tokenParts.length === 3) {
        const decodedPayload = JSON.parse(atob(tokenParts[1]));
        
        const userData: User = {
          username: decodedPayload.sub,
          email: decodedPayload.email || `${decodedPayload.sub}@example.com`,
          isAdmin: decodedPayload.is_superuser || false
        };

        // Store token and user data
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(userData));
        
        setToken(access_token);
        setUser(userData);

        console.log('Login successful:', userData);
      } else {
        throw new Error('Invalid token format');
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = () => {
    const storedToken = localStorage.getItem('token');
    return !!storedToken;
  };

  // Restore session on context initialization
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ 
      user, 
      token, 
      login, 
      logout, 
      isAuthenticated 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
