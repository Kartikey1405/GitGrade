import httpx
import base64
from app.config import Config

class GitHubService:
    BASE_URL = "https://api.github.com/repos"

    async def fetch_repo_data(self, owner: str, repo_name: str):
        """
        Fetches:
        1. Metadata (stars, forks, description)
        2. FULL Recursive File Tree (The Fix for Shallow Vision)
        3. README.md content
        """
        async with httpx.AsyncClient() as client:
            
            # --- Request 1: Get Basic Metadata ---
            repo_resp = await client.get(
                f"{self.BASE_URL}/{owner}/{repo_name}",
                headers=Config.GITHUB_HEADERS
            )
            
            if repo_resp.status_code == 404:
                raise Exception("Repository not found. Check the URL.")
            if repo_resp.status_code == 401:
                raise Exception("GitHub API Token is invalid or expired.")
            
            repo_data = repo_resp.json()

            # --- Request 2: Get FULL Recursive File Structure (The Critical Fix) ---
            # Step A: Find the default branch (usually 'main' or 'master')
            default_branch = repo_data.get("default_branch", "main")
            
            # Step B: Fetch the Git Tree recursively
            tree_resp = await client.get(
                f"{self.BASE_URL}/{owner}/{repo_name}/git/trees/{default_branch}?recursive=1",
                headers=Config.GITHUB_HEADERS
            )
            
            files = []
            if tree_resp.status_code == 200:
                tree_data = tree_resp.json()
                # Filter: Get 'path' only for items that are files (type='blob')
                # We skip folders (type='tree') because we just want the file paths
                files = [item['path'] for item in tree_data.get('tree', []) if item['type'] == 'blob']
            else:
                # Fallback: If recursive fetch fails (rare), return empty list to prevent crash
                print(f"Warning: Recursive tree fetch failed with status {tree_resp.status_code}")
                files = []

            # --- Request 3: Get README Content ---
            readme_content = ""
            readme_resp = await client.get(
                f"{self.BASE_URL}/{owner}/{repo_name}/readme",
                headers=Config.GITHUB_HEADERS
            )
            
            if readme_resp.status_code == 200:
                data = readme_resp.json()
                content_b64 = data['content']
                readme_content = base64.b64decode(content_b64).decode('utf-8', errors='ignore')

            # Return the data
            return {
                "metadata": repo_data,
                "files": files,       # Now contains ["src/App.tsx", "backend/main.py", etc.]
                "readme": readme_content
            }