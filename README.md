GitGrade API & Analysis Engine 🚀An Intelligent Backend Service for GitHub Repository Grading and ImprovementGitGrade is an intelligent backend service that analyzes any public GitHub repository, assigns a numerical "Grade" (out of 100), generates an executive summary, and provides a prioritized roadmap for improvement—all powered by Google's Gemini AI.The service is built on FastAPI and is deployed on Render, featuring robust authentication and a custom Keep-Alive solution to ensure zero cold-start delays.✨ Key FeaturesAI-Powered Analysis: Utilizes the Gemini 2.5-Flash model to critically review repository structure, code quality, and documentation.Repository Grading: Assigns a clear, quantifiable score (e.g., 92/100) to measure project health.Improvement Roadmap: Generates actionable, categorized steps (e.g., QUALITY ASSURANCE, DOCUMENTATION) for the owner to follow.Google OAuth: Secure and seamless login using Google for user authentication.PDF Report Generation: Creates professional, downloadable analysis reports using FPDF.Robust Email Service: Sends the generated reports reliably via SendGrid's HTTP API,  bypassing common cloud hosting (Render) firewall issues that blocked standard SMTP connections (which repeatedly caused a Connection unexpectedly closed error).Zero Cold Start: Implements a custom Keep-Alive Thread (using Python's threading and requests) to prevent the Render Free Tier service from sleeping after 15 minutes, ensuring instant response times for end-users.🛠 Technology StackComponentTechnologyPurposeFrameworkFastAPIHigh-performance, asynchronous Python web framework.AI EngineGemini 2.5-FlashCore large language model for analysis and roadmap generation.AuthenticationGoogle OAuthHandles secure user login and identity.Email ServiceSendGrid (HTTP API)Reliable email sending for report delivery.PDF GenerationFPDFUsed to create structured PDF report attachments.DeploymentRenderCloud hosting platform for the FastAPI backend.Keep-AlivePython threading & requestsCustom solution to prevent cold starts on the Free Tier.📐 Project Structure & Logic FlowThe backend is structured into modular routers and services:Authentication (app/routers/auth.py): Handles Google OAuth callbacks and issues secure JWT tokens.Analysis (app/routers/analyze.py):Fetches GitHub repository data.Calls the Gemini API for analysis, scoring, and roadmap generation.Calls the EmailService.Email Service (app/services/email_service.py):Contains the generate_pdf and send_email methods.The send_email method uses the SendGridAPIClient to make an HTTPS request for reliable delivery.Main Application (main.py):Initializes the FastAPI application and CORS middleware.Starts the Keep-Alive Thread (start_keep_alive_thread) on the startup event to continuously ping the service URL.⚙️ Setup and ConfigurationPrerequisitesPython 3.10+pip (using requirements.txt which must include fastapi, google-generativeai, fpdf2, sendgrid, and requests).A SendGrid Account with a verified sender and a generated API Key.Google OAuth Credentials (Client ID and Secret).Local SetupClone the repository:Bashgit clone https://github.com/Kartikey1405/GitGrade.git
cd GitGrade
Install dependencies:Bashpip install -r requirements.txt
Create .env file:Create a .env file in the root directory and populate it with the required environment variables:Code snippet# --- API Keys ---
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

# --- Google OAuth ---
GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI="http://localhost:8000/api/auth/callback" 
FRONTEND_URL="http://localhost:3000"

# --- JWT Security ---
JWT_SECRET_KEY="A_STRONG_RANDOM_STRING"

# --- SendGrid API Configuration ---
SMTP_EMAIL="your_verified_sender@gmail.com"
SMTP_PASSWORD="YOUR_SENDGRID_API_KEY_STARTING_WITH_SG." 
# SMTP_SERVER/SMTP_PORT are now primarily placeholders but required by Config class
SMTP_SERVER="smtp.sendgrid.net"
SMTP_PORT=2525
Run the application:Bashuvicorn main:app --reload
The API will be running at http://localhost:8000.Render Deployment ConfigurationWhen deploying to Render, ensure these critical variables are set in your environment:VariableValuePurposeGEMINI_API_KEYYOUR_API_KEYPowers the core analysis engine.SMTP_EMAILkartikeykushagra14@gmail.comYour verified sender email.SMTP_PASSWORDSG.xxxxxxxxxxxxxxxxxxxxxThe SendGrid API Key (used by the API client).RENDER_EXTERNAL_URLhttps://your-service-name.onrender.comCRITICAL: Used by the Keep-Alive thread to prevent service spin-down.
