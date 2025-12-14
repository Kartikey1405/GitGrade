// New interface for the detailed roadmap items
export interface RoadmapItem {
  title: string;
  description: string;
  category: string;
}

// New interface for the detected tech stack
export interface TechStack {
  frontend: string[];
  backend: string[];
  infrastructure: string[];
}

// Updated AnalysisResult to include the new complex data
export interface AnalysisResult {
  details: {
    name: string;
    owner: string;
    description: string;
    stars: number;
    forks: number;
    open_issues: number;
    language: string;
  };
  score: number;
  summary: string;
  roadmap: RoadmapItem[]; // <--- CHANGED: Now an array of objects, not strings
  tech_stack?: TechStack; // <--- ADDED: Optional field for tech stack
  file_structure: string[];
}

export interface User {
  email: string;
  name: string;
  picture?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}