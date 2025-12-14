import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface TerminalLoaderProps {
  repoUrl: string;
}

const TerminalLoader = ({ repoUrl }: TerminalLoaderProps) => {
  const [lines, setLines] = useState<string[]>([]);
  
  // Safe fallback if repoUrl is missing
  const safeUrl = repoUrl || "https://github.com/unknown/repo";

  const terminalLines = [
    `$ git clone ${safeUrl}`,
    'Cloning repository...',
    'Receiving objects: 100% (234/234), done.',
    'Resolving deltas: 100% (89/89), done.',
    '',
    '$ gitgrade analyze --deep',
    '[INFO] Initializing Gemini AI Core...',
    '[INFO] Loading language models...',
    '[SCAN] Analyzing file structure...',
    '[SCAN] Detecting code patterns...',
    '[SCAN] Checking security vulnerabilities...',
    '[SCAN] Evaluating code quality metrics...',
    '[AI] Generating improvement roadmap...',
    '[AI] Synthesizing recommendations...',
    '',
    '[SUCCESS] Analysis complete!',
    'Preparing results...',
  ];

  useEffect(() => {
    // Reset lines on mount
    setLines([]);
    
    let index = 0;
    const interval = setInterval(() => {
      if (index < terminalLines.length) {
        setLines(prev => [...prev, terminalLines[index]]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [repoUrl]); // Re-run if URL changes

  return (
    <div className="glass-card p-6 font-mono text-sm overflow-hidden max-h-[400px]">
      <div className="flex items-center gap-2 mb-4 pb-4 border-b border-border">
        <div className="w-3 h-3 rounded-full bg-destructive" />
        <div className="w-3 h-3 rounded-full bg-yellow-500" />
        <div className="w-3 h-3 rounded-full bg-neon" />
        <span className="ml-2 text-muted-foreground text-xs">terminal — gitgrade</span>
      </div>
      
      <div className="space-y-1 overflow-y-auto max-h-[300px]">
        {lines.map((line, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.1 }}
            className={`
              ${(line && line.startsWith('$')) ? 'text-neon font-semibold' : ''}
              ${(line && line.startsWith('[INFO]')) ? 'text-blue-400' : ''}
              ${(line && line.startsWith('[SCAN]')) ? 'text-yellow-400' : ''}
              ${(line && line.startsWith('[AI]')) ? 'text-purple-400' : ''}
              ${(line && line.startsWith('[SUCCESS]')) ? 'text-neon' : ''}
              ${(line && !line.startsWith('[') && !line.startsWith('$')) ? 'text-muted-foreground' : ''}
            `}
          >
            {line || '\u00A0'}
          </motion.div>
        ))}
        <motion.span
          className="inline-block w-2 h-4 bg-neon ml-1"
          animate={{ opacity: [1, 0, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      </div>
    </div>
  );
};

export default TerminalLoader;