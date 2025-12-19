import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Send, Loader2, Mail } from 'lucide-react';
import { toast } from 'sonner';
import Layout from '@/components/layout/Layout';
import ScoreGauge from '@/components/dashboard/ScoreGauge';
import FileTree from '@/components/dashboard/FileTree';
import AIMentor from '@/components/dashboard/AIMentor';
import TerminalLoader from '@/components/dashboard/TerminalLoader';
import RepoDetails from '@/components/dashboard/RepoDetails';
import { analysisApi } from '@/lib/api'; 
import { AnalysisResult } from '@/types/analysis';

const Dashboard = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isSendingReport, setIsSendingReport] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoUrl.trim()) {
      toast.error('Please enter a GitHub repository URL');
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    try {
      
      const data = await analysisApi.analyze(repoUrl);
      setResult(data);
      toast.success('Analysis complete!');
      
      
    } catch (error: any) {
      console.error("Analysis Failed:", error);
      toast.error(error.response?.data?.detail || 'Analysis failed. Is the Backend running?');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSendReport = async () => {
    if (!result) return;
    
    setIsSendingReport(true);
    try {
    
      await analysisApi.sendReport(result);
      toast.success('Report sent to your email!');
      
      
    } catch (error: any) {
      console.error("Email Failed:", error);
      toast.error(error.response?.data?.detail || 'Failed to send report. Are you logged in?');
    } finally {
      setIsSendingReport(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        {/* Search Section */}
        <motion.div
          className="max-w-3xl mx-auto mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-3xl md:text-4xl font-bold text-foreground text-center mb-2">
            Analyze Your Repository
          </h1>
          <p className="text-muted-foreground text-center mb-8">
            Paste your GitHub repository URL and get instant AI-powered insights
          </p>

          <form onSubmit={handleAnalyze} className="relative">
            <div className="relative">
              <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="input-cyber pl-14 pr-36"
                disabled={isAnalyzing}
              />
              <button
                type="submit"
                disabled={isAnalyzing}
                className="absolute right-2 top-1/2 -translate-y-1/2 btn-neon py-2 px-6 text-sm flex items-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Analyzing
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    Analyze
                  </>
                )}
              </button>
            </div>
          </form>
        </motion.div>

        {/* Loading State */}
        <AnimatePresence mode="wait">
          {isAnalyzing && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="max-w-3xl mx-auto"
            >
              <TerminalLoader repoUrl={repoUrl} />
            </motion.div>
          )}

          {/* Results */}
          {result && !isAnalyzing && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Repo Details */}
              <RepoDetails details={result.details} />

              {/* Score and Main Content */}
              <div className="grid lg:grid-cols-3 gap-8">
                {/* Score Gauge */}
                <motion.div
                  className="glass-card p-8 flex items-center justify-center"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <ScoreGauge score={result.score} />
                </motion.div>

                {/* File Tree */}
                <motion.div
                  className="lg:col-span-2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <FileTree files={result.file_structure} />
                </motion.div>
              </div>

              {/* AI Mentor */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <AIMentor summary={result.summary} roadmap={result.roadmap} />
              </motion.div>

              {/* Send Report Button */}
              <motion.div
                className="flex justify-center pt-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <motion.button
                  onClick={handleSendReport}
                  disabled={isSendingReport}
                  className="btn-neon flex items-center gap-3 text-lg relative overflow-hidden"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {/* Pulse effect */}
                  <motion.span
                    className="absolute inset-0 bg-white/20"
                    animate={{ opacity: [0, 0.5, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                  {isSendingReport ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Mail className="w-5 h-5" />
                  )}
                  {isSendingReport ? 'Sending...' : 'Send Official Report to Email'}
                </motion.button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Empty State */}
        {!result && !isAnalyzing && (
          <motion.div
            className="text-center py-20"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="glass-card inline-flex p-8 flex-col items-center max-w-md">
              <Search className="w-16 h-16 text-neon/30 mb-4" />
              <h3 className="text-xl font-semibold text-foreground mb-2">
                Ready to Analyze
              </h3>
              <p className="text-muted-foreground">
                Enter a GitHub repository URL above to get started with your code health analysis.
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </Layout>
  );
};

export default Dashboard;
