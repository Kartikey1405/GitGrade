import { motion } from 'framer-motion';
import { Star, GitFork, AlertCircle, Code2 } from 'lucide-react';

interface RepoDetailsProps {
  details: {
    name: string;
    owner: string;
    description: string;
    stars: number;
    forks: number;
    open_issues: number;
    language: string;
  };
}

const RepoDetails = ({ details }: RepoDetailsProps) => {
  const stats = [
    { icon: Star, label: 'Stars', value: details.stars, color: 'text-yellow-400' },
    { icon: GitFork, label: 'Forks', value: details.forks, color: 'text-blue-400' },
    { icon: AlertCircle, label: 'Issues', value: details.open_issues, color: 'text-orange-400' },
    { icon: Code2, label: 'Language', value: details.language, color: 'text-neon' },
  ];

  return (
    <motion.div
      className="glass-card p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
        <div>
          <h2 className="text-xl font-bold text-foreground">
            {details.owner} / <span className="text-neon">{details.name}</span>
          </h2>
          <p className="text-muted-foreground text-sm mt-1 max-w-2xl">{details.description}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-muted/30"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            <stat.icon className={`w-4 h-4 ${stat.color}`} />
            <span className="text-sm text-muted-foreground">{stat.label}:</span>
            <span className="text-sm font-medium text-foreground">{stat.value}</span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default RepoDetails;
