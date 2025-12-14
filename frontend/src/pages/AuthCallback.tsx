import { useEffect, useState, useRef } from 'react'; // <--- Added useRef
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import axios from 'axios';
import Layout from '@/components/layout/Layout';

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth(); 
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Authenticating...');
  
  // --- CRITICAL FIX: Prevent Double-Firing in React Strict Mode ---
  const effectRan = useRef(false);

  useEffect(() => {
    // If we already ran this logic, STOP immediately.
    if (effectRan.current) return;

    const handleAuth = async () => {
      const code = searchParams.get('code');

      if (!code) {
        setStatus('error');
        setMessage('No authorization code found');
        return;
      }
      
      // Mark that we are running it now, so we don't run it again
      effectRan.current = true;

      try {
        setMessage('Verifying credentials...');
        
        // --- Direct Call to Python Backend ---
        const response = await axios.post('http://localhost:8000/api/auth/google', { 
          code 
        });
        
        // The backend returns { access_token: "...", token_type: "bearer" }
        const token = response.data.access_token;

        // Save to Storage
        localStorage.setItem('access_token', token);

        // Update Context
        if (login) {
             // Pass 'null' for user since backend didn't send full profile yet
             login(token, null); 
        }

        setStatus('success');
        setMessage('Authentication successful!');
        
        setTimeout(() => {
          navigate('/dashboard');
        }, 1500);

      } catch (error: any) {
        console.error('Auth error:', error);
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Authentication failed');
      }
    };

    handleAuth();
  }, [searchParams, login, navigate]);

  // --- UI CONFIG (Unchanged) ---
  const statusConfig = {
    loading: {
      icon: Loader2,
      iconClass: 'text-neon animate-spin',
      bgClass: 'bg-neon/10',
    },
    success: {
      icon: CheckCircle,
      iconClass: 'text-neon',
      bgClass: 'bg-neon/20',
    },
    error: {
      icon: XCircle,
      iconClass: 'text-destructive',
      bgClass: 'bg-destructive/10',
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Layout showFooter={false}>
      <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center px-6">
        <motion.div
          className="glass-card p-12 text-center max-w-md w-full"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <motion.div
            className={`w-20 h-20 rounded-2xl ${config.bgClass} flex items-center justify-center mx-auto mb-6`}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
          >
            <Icon className={`w-10 h-10 ${config.iconClass}`} />
          </motion.div>

          <h2 className="text-2xl font-bold text-foreground mb-3">
            {status === 'loading' && 'Signing You In'}
            {status === 'success' && 'Welcome!'}
            {status === 'error' && 'Oops!'}
          </h2>

          <p className="text-muted-foreground mb-6">{message}</p>

          {status === 'loading' && (
            <div className="flex justify-center gap-1">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 rounded-full bg-neon"
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                />
              ))}
            </div>
          )}

          {status === 'error' && (
            <button
              onClick={() => navigate('/login')}
              className="btn-ghost mt-4"
            >
              Try Again
            </button>
          )}
        </motion.div>
      </div>
    </Layout>
  );
};

export default AuthCallback;