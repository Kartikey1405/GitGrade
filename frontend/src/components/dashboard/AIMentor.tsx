import { motion } from 'framer-motion';
import { Bot, Sparkles, ArrowRight, CheckCircle, Code2, Server, Layers } from 'lucide-react';
import { RoadmapItem, TechStack } from '@/types/analysis';

interface AIMentorProps {
  summary: string;
  roadmap: RoadmapItem[]; // Updated to accept detailed objects
  tech_stack?: TechStack; // Added optional tech stack
}

const AIMentor = ({ summary, roadmap, tech_stack }: AIMentorProps) => {

  // Helper function to render colorful tech badges
  const renderTechBadges = (techs: string[] | undefined, colorClass: string) => {
    if (!techs || techs.length === 0) return null;
    return techs.map((tech, i) => (
      <span key={i} className={`text-[10px] px-2 py-0.5 rounded-full border bg-opacity-10 ${colorClass}`}>
        {tech}
      </span>
    ));
  };

  return (
    <div className="glass-card p-6 h-full">
      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
        <Bot className="w-5 h-5 text-neon" />
        AI Mentor Feedback
      </h3>

      {/* NEW: Tech Stack Section */}
      {tech_stack && (
        <motion.div 
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-wrap gap-4 mb-6 border-b border-border/50 pb-4"
        >
           <div className="space-y-1.5">
              <div className="text-xs text-muted-foreground flex items-center gap-1"><Code2 size={12}/> Frontend</div>
              <div className="flex gap-2 flex-wrap">{renderTechBadges(tech_stack.frontend, "border-blue-400 text-blue-400")}</div>
           </div>
           <div className="space-y-1.5">
              <div className="text-xs text-muted-foreground flex items-center gap-1"><Server size={12}/> Backend</div>
              <div className="flex gap-2 flex-wrap">{renderTechBadges(tech_stack.backend, "border-green-400 text-green-400")}</div>
           </div>
           <div className="space-y-1.5">
              <div className="text-xs text-muted-foreground flex items-center gap-1"><Layers size={12}/> Infra</div>
              <div className="flex gap-2 flex-wrap">{renderTechBadges(tech_stack.infrastructure, "border-purple-400 text-purple-400")}</div>
           </div>
        </motion.div>
      )}

      {/* Summary Card */}
      <motion.div
        className="bg-neon/5 border border-neon/20 rounded-xl p-4 mb-6"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-neon flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-4 h-4 text-void" />
          </div>
          <div>
            <h4 className="font-medium text-foreground mb-1">Analysis Summary</h4>
            <p className="text-sm text-muted-foreground leading-relaxed">{summary}</p>
          </div>
        </div>
      </motion.div>

      {/* Roadmap Section */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-4">
          Improvement Roadmap
        </h4>
        <div className="space-y-3">
          {roadmap.map((item, index) => (
            <motion.div
              key={index}
              className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 border border-border/50 hover:border-neon/30 transition-colors group"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
            >
              <div className="w-6 h-6 rounded-full bg-neon/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-xs font-semibold text-neon">{index + 1}</span>
              </div>
              
              <div className="flex-1">
                {/* FIX: Render Title & Description separately (Prevents Object Error) */}
                <h5 className="text-sm font-semibold text-foreground group-hover:text-neon transition-colors">
                  {item.title}
                </h5>
                <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
                  {item.description}
                </p>
                <span className="inline-block mt-2 text-[10px] uppercase tracking-widest text-muted-foreground bg-white/5 px-1.5 py-0.5 rounded border border-white/5">
                  {item.category || "General"}
                </span>
              </div>

              <ArrowRight className="w-4 h-4 text-muted-foreground mt-0.5 opacity-0 group-hover:opacity-100 transition-opacity" />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Completion badge */}
      <motion.div
        className="mt-6 flex items-center gap-2 text-sm text-muted-foreground"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <CheckCircle className="w-4 h-4 text-neon" />
        Analysis powered by Gemini AI
      </motion.div>
    </div>
  );
};

export default AIMentor;