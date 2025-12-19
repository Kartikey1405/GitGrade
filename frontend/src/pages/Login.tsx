




import { motion } from 'framer-motion';
import { Chrome, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import Layout from '@/components/layout/Layout';

const GOOGLE_CLIENT_ID = '565043140238-m62n1otfs1nj8op5jtu64aogqlf0s0n5.apps.googleusercontent.com';


const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const REDIRECT_URI = `${BASE_URL}/api/auth/callback`;

const Login = () => {
  const handleGoogleLogin = () => {
    const googleAuthUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=email+profile`;
    window.location.href = googleAuthUrl;
  };

  return (
    <Layout showFooter={false}>
      <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center px-6">
        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          {/* Back Link */}
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-muted-foreground hover:text-neon transition-colors mb-8"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>

          {/* Login Card */}
          <div className="glass-card p-10">
            {/* Header */}
            <div className="text-center mb-10">
              <motion.div
                className="w-16 h-16 rounded-2xl bg-gradient-neon flex items-center justify-center mx-auto mb-6"
                initial={{ rotate: -10 }}
                animate={{ rotate: 0 }}
                transition={{ type: "spring", stiffness: 200 }}
              >
                <span className="text-3xl font-bold text-void">G</span>
              </motion.div>
              <h1 className="text-3xl font-bold text-foreground mb-3">Welcome Back</h1>
              <p className="text-muted-foreground">
                Sign in to access your dashboard and analyze repositories
              </p>
            </div>

            {/* Google Sign In Button */}
            <motion.button
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center gap-3 px-6 py-4 rounded-xl border border-neon/30 bg-neon/5 hover:bg-neon/10 hover:border-neon/50 transition-all text-foreground font-medium"
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
            >
              <Chrome className="w-5 h-5 text-neon" />
              Sign in with Google
            </motion.button>

            {/* Divider */}
            <div className="flex items-center gap-4 my-8">
              <div className="flex-1 h-px bg-border" />
              <span className="text-sm text-muted-foreground">Secure Authentication</span>
              <div className="flex-1 h-px bg-border" />
            </div>

            {/* Info */}
            <p className="text-center text-sm text-muted-foreground">
              By signing in, you agree to our{' '}
              <a href="#" className="text-neon hover:underline">Terms of Service</a>
              {' '}and{' '}
              <a href="#" className="text-neon hover:underline">Privacy Policy</a>
            </p>
          </div>

          {/* Features reminder */}
          <motion.div
            className="mt-8 flex justify-center gap-6 text-sm text-muted-foreground"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            {['AI-Powered', 'Secure', 'Free to Start'].map((feature, i) => (
              <div key={feature} className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-neon" />
                {feature}
              </div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default Login;
