import React, { createContext, useContext, useState, useEffect } from 'react';
import { mockApi, type User } from '@/services/mockApi';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<{ error?: string }>;
  signup: (email: string, username: string, password: string) => Promise<{ error?: string }>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const currentUser = await mockApi.getCurrentUser();
      setUser(currentUser);
      setLoading(false);
    };
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    const result = await mockApi.login(email, password);
    if (!result.error) {
      setUser(result.user);
    }
    return { error: result.error };
  };

  const signup = async (email: string, username: string, password: string) => {
    const result = await mockApi.signup(email, username, password);
    if (!result.error) {
      setUser(result.user);
    }
    return { error: result.error };
  };

  const logout = async () => {
    await mockApi.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
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
