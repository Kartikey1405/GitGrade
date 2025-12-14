import { useState } from 'react';
import { Github, Twitter, Linkedin, Heart, Zap } from 'lucide-react';
import { motion } from 'framer-motion';
import FuelReactor from '@/components/dashboard/FuelReactor';

const Footer = () => {
  const [isFuelOpen, setIsFuelOpen] = useState(false);

  const socialLinks = [
    { icon: Github, href: 'https://github.com/Kartikey1405', label: 'GitHub' },
    { icon: Twitter, href: 'https://x.com/Kartikey1405', label: 'Twitter' },
    { icon: Linkedin, href: 'https://www.linkedin.com/in/kartikey-kushagra14', label: 'LinkedIn' },
  ];

  return (
    <footer className="relative z-10 border-t border-neon/10">
      <div className="container mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Brand */}
          <div className="flex items-center gap-3">
            <motion.div
              className="w-8 h-8 rounded-lg bg-gradient-neon flex items-center justify-center"
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.5 }}
            >
              <Github className="w-4 h-4 text-void" />
            </motion.div>
            <span className="text-lg font-semibold text-foreground">GitGrade</span>
          </div>

          {/* Fuel Reactor Button */}
          <motion.button
            onClick={() => setIsFuelOpen(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl border border-primary/30 bg-primary/10 text-primary hover:bg-primary/20 hover:shadow-lg hover:shadow-primary/20 transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Zap className="w-4 h-4" />
            <span className="text-sm font-medium">Fuel the Algorithm</span>
          </motion.button>

          {/* Tagline */}
          <p className="text-muted-foreground text-sm flex items-center gap-2">
            Built with <Heart className="w-4 h-4 text-primary animate-pulse" /> by developers, for developers
          </p>

          {/* Social Links */}
          <div className="flex items-center gap-4">
            {socialLinks.map(({ icon: Icon, href, label }) => (
              <motion.a
                key={label}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg border border-neon/20 hover:border-neon/50 hover:bg-neon/10 transition-all"
                whileHover={{ scale: 1.1, y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                <Icon className="w-5 h-5 text-muted-foreground hover:text-neon transition-colors" />
              </motion.a>
            ))}
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-primary/10 text-center">
          <p className="text-muted-foreground text-sm">
            © {new Date().getFullYear()} GitGrade. All rights reserved.
          </p>
        </div>
      </div>

      {/* Fuel Reactor Modal */}
      <FuelReactor isOpen={isFuelOpen} onClose={() => setIsFuelOpen(false)} />
    </footer>
  );
};

export default Footer;
