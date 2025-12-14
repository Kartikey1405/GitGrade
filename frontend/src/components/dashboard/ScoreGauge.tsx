import { motion } from 'framer-motion';

interface ScoreGaugeProps {
  score: number;
}

const ScoreGauge = ({ score }: ScoreGaugeProps) => {
  const circumference = 2 * Math.PI * 90;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'hsl(142, 69%, 58%)'; // neon green
    if (score >= 60) return 'hsl(48, 96%, 53%)'; // yellow
    if (score >= 40) return 'hsl(25, 95%, 53%)'; // orange
    return 'hsl(0, 84%, 60%)'; // red
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Work';
  };

  const color = getScoreColor(score);

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative w-56 h-56">
        {/* Background circle */}
        <svg className="w-full h-full -rotate-90" viewBox="0 0 200 200">
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="hsl(143, 30%, 12%)"
            strokeWidth="12"
          />
          {/* Animated score circle */}
          <motion.circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            style={{
              filter: `drop-shadow(0 0 10px ${color})`,
            }}
          />
        </svg>

        {/* Score number */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className="text-6xl font-bold text-foreground"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, type: "spring" }}
          >
            {score}
          </motion.span>
          <motion.span
            className="text-sm text-muted-foreground uppercase tracking-wider mt-1"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            out of 100
          </motion.span>
        </div>
      </div>

      {/* Score label */}
      <motion.div
        className="mt-4 px-4 py-2 rounded-full border"
        style={{
          borderColor: color,
          backgroundColor: `${color}20`,
        }}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
      >
        <span className="font-medium" style={{ color }}>
          {getScoreLabel(score)}
        </span>
      </motion.div>
    </div>
  );
};

export default ScoreGauge;
