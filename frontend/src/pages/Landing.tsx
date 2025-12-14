import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Shield, FileText, Github, Code2, Zap, Target } from 'lucide-react';
import Layout from '@/components/layout/Layout';

const Landing = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'Gemini AI Core',
      description: 'Powered by Google\'s advanced AI to provide intelligent code analysis and actionable feedback.',
    },
    {
      icon: Shield,
      title: 'Deep Static Analysis',
      description: 'Comprehensive code quality checks including security vulnerabilities, code smells, and best practices.',
    },
    {
      icon: FileText,
      title: 'Official PDF Reports',
      description: 'Professional, shareable reports delivered straight to your inbox with detailed insights.',
    },
  ];

  const stats = [
    { value: '10K+', label: 'Repositories Analyzed' },
    { value: '98%', label: 'Accuracy Rate' },
    { value: '500+', label: 'Happy Developers' },
  ];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="min-h-[calc(100vh-6rem)] flex items-center justify-center px-6">
        <div className="container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-neon/30 bg-neon/5 mb-8"
            >
              <Zap className="w-4 h-4 text-neon" />
              <span className="text-sm text-neon font-medium">AI-Powered Code Analysis</span>
            </motion.div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight">
              <span className="block">Analyze.</span>
              <span className="block text-glow text-neon">Optimize.</span>
              <span className="block">Dominate.</span>
            </h1>

            {/* Subheading */}
            <p className="text-xl md:text-2xl text-muted-foreground mb-10 max-w-2xl mx-auto">
              Get instant AI-powered insights into your GitHub repositories. 
              Elevate your code quality to the next level.
            </p>

            {/* CTA Buttons */}
            <motion.div
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Link to="/login" className="btn-neon flex items-center gap-2 text-lg">
                Check My Score
                <ArrowRight className="w-5 h-5" />
              </Link>
              <a href="#features" className="btn-ghost flex items-center gap-2">
                Learn More
              </a>
            </motion.div>
          </motion.div>

          {/* Floating Stats */}
          <motion.div
            className="mt-20 flex flex-wrap justify-center gap-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                className="glass-card px-8 py-6 text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
              >
                <div className="text-3xl md:text-4xl font-bold text-neon mb-1">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-6">
        <div className="container mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              Powerful <span className="text-neon">Features</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Everything you need to understand and improve your codebase
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="glass-card-hover p-8"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.15 }}
              >
                <div className="w-14 h-14 rounded-2xl bg-gradient-neon flex items-center justify-center mb-6">
                  <feature.icon className="w-7 h-7 text-void" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-6">
        <div className="container mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              How It <span className="text-neon">Works</span>
            </h2>
          </motion.div>

          <div className="max-w-4xl mx-auto">
            {[
              { step: '01', icon: Code2, title: 'Paste Your Repo URL', desc: 'Simply drop your GitHub repository link' },
              { step: '02', icon: Sparkles, title: 'AI Analyzes Your Code', desc: 'Our Gemini-powered engine scans every file' },
              { step: '03', icon: Target, title: 'Get Your Score & Roadmap', desc: 'Receive actionable insights and improvement tips' },
            ].map((item, index) => (
              <motion.div
                key={item.step}
                className="flex items-start gap-6 mb-12 last:mb-0"
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
              >
                <div className="flex-shrink-0 w-16 h-16 rounded-2xl border border-neon/30 bg-neon/5 flex items-center justify-center">
                  <span className="text-2xl font-bold text-neon">{item.step}</span>
                </div>
                <div className="glass-card flex-1 p-6 flex items-center gap-4">
                  <item.icon className="w-8 h-8 text-neon flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-semibold text-foreground mb-1">{item.title}</h3>
                    <p className="text-muted-foreground">{item.desc}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Open Source Section */}
      <section id="opensource" className="py-24 px-6">
        <div className="container mx-auto">
          <motion.div
            className="glass-card p-12 md:p-16 text-center max-w-4xl mx-auto"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            <motion.div
              className="w-20 h-20 rounded-3xl bg-gradient-neon flex items-center justify-center mx-auto mb-8"
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.7 }}
            >
              <Github className="w-10 h-10 text-void" />
            </motion.div>
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Open Source & Community Driven
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              GitGrade is built by developers, for developers. Join our community and help shape the future of code analysis.
            </p>
            <motion.a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost inline-flex items-center gap-2"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Github className="w-5 h-5" />
              Contribute on GitHub
            </motion.a>
          </motion.div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-6">
        <div className="container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
              Ready to <span className="text-neon text-glow">Level Up</span>?
            </h2>
            <p className="text-xl text-muted-foreground mb-10">
              Start analyzing your code in seconds. No credit card required.
            </p>
            <Link to="/login">
              <motion.button
                className="btn-neon text-lg px-10 py-5"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Get Started Free
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>
    </Layout>
  );
};

export default Landing;
