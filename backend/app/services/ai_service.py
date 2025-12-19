import google.generativeai as genai
import os
import json
from app.config import Config

class AIService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
      
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def analyze_code_quality(self, readme_content: str, files: list, base_score: int):
        """
        Sends repo structure to Gemini to generate specific, high-level feedback
        and detect the technology stack.
        """
        
      
        all_files = " ".join(files)
        is_monorepo = "backend/" in all_files and "frontend/" in all_files
        has_gitignore = ".gitignore" in all_files
        
      
        priority_files = [
            'package.json', 'pom.xml', 'build.gradle', 'requirements.txt', 
            'Dockerfile', 'docker-compose.yml', 'vite.config', 'next.config',
            'tsconfig.json', 'go.mod', 'Cargo.toml', 'App.tsx', 'main.py',
            'tailwind.config.js', '.github/workflows'
        ]
        
        important_files = [
            f for f in files 
            if any(k in f for k in priority_files) or f.count('/') <= 2
        ]
        file_summary = "\n".join(important_files[:80]) 

        
        prompt = f"""
        You are a harsh but helpful Senior Software Architect. 
        Analyze this GitHub repository structure and return a raw JSON response.
        
        CONTEXT:
        - Project Type: {'Full-Stack Monorepo' if is_monorepo else 'Standard Repository'}
        - Base Logic Score: {base_score}/100
        - Has .gitignore: {'YES' if has_gitignore else 'NO'} (Do NOT suggest adding it)
        
        FILES DETECTED (Truncated):
        {file_summary}

        README EXCERPT:
        {readme_content[:1000] if readme_content else "No README detected."}

        INSTRUCTIONS:
        1. **Deep Tech Stack Detection:** Don't just say "JavaScript". Detect specific frameworks (e.g., "React", "Spring Boot", "Tailwind", "Vite").
        2. **Detailed Roadmap:** Provide **5 to 7** distinct, high-impact improvements.
        3. **Structure:** Each roadmap item MUST have a short 'title' and a detailed 'description' explaining HOW to do it.
        4. **Summary:** Write a concise executive summary. **IMPORTANT: Do NOT mention the specific numeric 'Logic Score' (e.g. {base_score}) in the text summary.** Just focus on the code quality description.
        
        OUTPUT FORMAT (JSON ONLY - NO MARKDOWN):
        {{
            "tech_stack": {{
                "frontend": ["List", "frontend", "techs"],
                "backend": ["List", "backend", "techs"],
                "infrastructure": ["Docker", "AWS", "etc"]
            }},
            "summary": "A 3-4 sentence executive summary of the architecture and code quality.",
            "roadmap": [
                {{
                    "title": "Implement Docker Orchestration",
                    "description": "Currently, the services run independently. Create a docker-compose.yml file to link the Spring Boot backend and React frontend via a shared network.",
                    "category": "Architecture"
                }},
                {{
                    "title": "Enhance CI/CD Pipeline",
                    "description": "Create a .github/workflows/deploy.yml file to automate testing and build verification on every push.",
                    "category": "DevOps"
                }}
            ],
            "quality_bonus": 0
        }}
        """

        try:
            response = await self.model.generate_content_async(prompt)
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_text)
        
        except Exception as e:
            print(f"AI Error: {e}")
           
            return {
                "tech_stack": {"frontend": [], "backend": [], "infrastructure": []},
                "summary": "AI Analysis unavailable. Showing fallback data.",
                "roadmap": [
                    {
                        "title": "Error Connecting to AI", 
                        "description": "Please check your API key and internet connection.", 
                        "category": "System"
                    }
                ],
                "quality_bonus": 0
            }
