from datetime import datetime

class ScoringService:
    def calculate_score(self, metadata, files, readme_content):
        """
        Advanced Scoring Algorithm v3.0 (Strict & Detailed)
        Total Score: 0 - 100
        """
        score = 0
        repo_files = set(files) # Set for fast O(1) lookups
        
        # Convert all paths to a single string for substring searching (Fix for Monorepos)
        # This allows us to find 'src' even if it is in 'frontend/src'
        all_files_str = " ".join(files)
        
        readme_lower = readme_content.lower() if readme_content else ""
        
        # --- EDGE CASE: Empty Repository ---
        if len(files) < 2:
            return 10 # Participation award only.

        # =========================================================
        # 1. REPOSITORY HYGIENE (Max 20 pts)
        # =========================================================
        
        # A. Root Directory Clutter (5 pts)
        # Good repos have clean roots. Bad repos have 50 files in root.
        # We count files that don't have a '/' in them (meaning they are at the root)
        root_file_count = sum(1 for f in files if "/" not in f)
        if root_file_count < 15:
            score += 5
        else:
            score += 0 # Too messy

        # B. The "Trash" Check (Negative Scoring)
        # Penalize for committing system files or secrets
        penalty = 0
        garbage_files = ['.DS_Store', 'Thumbs.db', '__pycache__', 'node_modules', '.env', 'venv']
        
        # Check if any garbage string appears anywhere in the file paths
        for junk in garbage_files:
            if any(junk in f for f in files):
                penalty += 5 # Heavy penalty for each mistake
        
        score = max(0, score - penalty) # Deduct from current score

        # C. Standard Folders (15 pts)
        # We look for 'src', 'app', 'lib', or 'public' to see structure
        # We search 'all_files_str' to find these folders even if nested
        structure_folders = ['src/', 'app/', 'lib/', 'components/', 'pages/', 'public/', 'server/', 'client/']
        if any(folder in all_files_str for folder in structure_folders):
            score += 15
        elif len(files) > 3:
            score += 5 # Partial credit for having *some* files

        # =========================================================
        # 2. DOCUMENTATION DEPTH (Max 20 pts)
        # =========================================================
        
        if readme_content:
            # A. Length (5 pts)
            if len(readme_content) > 1000: score += 5
            elif len(readme_content) > 300: score += 2
            
            # B. "How-To" Instructions (10 pts)
            # A readme is useless without setup steps
            setup_keywords = ['npm install', 'pip install', 'setup', 'getting started', 'run the app', 'docker run', 'mvn install', './mvnw']
            if any(k in readme_lower for k in setup_keywords):
                score += 10
            
            # C. Visuals/Badges (5 pts)
            # Checks for images (screenshots) or badges in markdown
            if '![' in readme_content or '<img' in readme_lower:
                score += 5

        # =========================================================
        # 3. ENGINEERING STANDARDS (Max 20 pts)
        # =========================================================
        
        # A. Version Control (10 pts)
        if '.gitignore' in repo_files or '.gitignore' in all_files_str:
            score += 10
        
        # B. Dependency Locking (10 pts)
        # Shows they care about reproducible builds
        lock_files = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock', 'go.sum', 'Cargo.lock', 'pom.xml', 'build.gradle']
        if any(f in all_files_str for f in lock_files):
            score += 10

        # =========================================================
        # 4. TESTING & QA (Max 20 pts)
        # =========================================================
        
        # A. Tests Existence (15 pts)
        test_indicators = ['test', 'tests', '__tests__', 'spec', 'pytest.ini']
        if any(t in all_files_str for t in test_indicators):
            score += 15
            
        # B. Automation/CI (5 pts)
        if '.github' in all_files_str or '.travis.yml' in all_files_str or 'circleci' in all_files_str:
            score += 5

        # =========================================================
        # 5. ACTIVITY & HEALTH (Max 10 pts)
        # =========================================================
        
        # Check last update time (Must parse ISO format)
        last_push = metadata.get('pushed_at')
        if last_push:
            try:
                # Format: 2023-10-25T14:30:00Z
                push_date = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ")
                days_inactive = (datetime.now() - push_date).days
                
                if days_inactive < 30: score += 10   # Active
                elif days_inactive < 90: score += 5  # Okay
                else: score += 0                     # Stale
            except:
                score += 5 # Benefit of doubt if parsing fails

        # =========================================================
        # 6. THE GOLDEN STANDARD (Max 10 pts)
        # =========================================================
        
        # A. Licensing (5 pts) - Open Source Standard
        if metadata.get('license') is not None or 'LICENSE' in all_files_str:
            score += 5
            
        # B. Description (5 pts) - GitHub UI Standard
        if metadata.get('description') and len(metadata['description']) > 10:
            score += 5

        return max(0, min(100, score))