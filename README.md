# GitGrade API & Analysis Engine

## An Intelligent Backend Service for GitHub Repository Grading and Improvement

GitGrade is an intelligent backend service that analyzes any public GitHub repository, assigns a numerical **grade (out of 100)**, generates an executive summary, and provides a **prioritized roadmap for improvement**, all powered by **Google’s Gemini AI**.

The service is built using **FastAPI** and deployed on **Render**, featuring secure authentication and a custom **Keep-Alive mechanism** to ensure zero cold-start delays.

---

## Key Features

### AI-Powered Repository Analysis
- Uses **Gemini 2.5-Flash** to critically analyze:
  - Repository structure  
  - Code quality  
  - Documentation standards  

### Repository Grading
- Assigns a clear and quantifiable score (e.g., `92/100`) to evaluate overall project health.

### Improvement Roadmap
- Generates actionable and categorized recommendations such as:
  - Quality Assurance  
  - Documentation  
  - Code Maintainability  

### Google OAuth Authentication
- Secure and seamless login using Google OAuth.

### PDF Report Generation
- Generates professional, downloadable PDF reports using **FPDF**.

### Robust Email Delivery
- Sends reports reliably using **SendGrid HTTP API**.
- Avoids SMTP issues on cloud platforms like Render that often result in `Connection unexpectedly closed` errors.

### Zero Cold Start
- Implements a custom **Keep-Alive Thread** using Python `threading` and `requests`.
- Prevents Render Free Tier services from sleeping after 15 minutes, ensuring instant responses.

---

## Technology Stack

| Component        | Technology            | Purpose |
|------------------|-----------------------|---------|
| Framework        | FastAPI               | High-performance asynchronous backend |
| AI Engine        | Gemini 2.5-Flash      | Repository analysis and roadmap generation |
| Authentication  | Google OAuth          | Secure user login |
| Email Service   | SendGrid (HTTP API)   | Reliable email delivery |
| PDF Generation  | FPDF                  | Structured PDF reports |
| Deployment      | Render                | Cloud hosting platform |
| Keep-Alive      | Python threading, requests | Prevents cold starts |

---

## Project Structure & Logic Flow

The backend follows a modular architecture:

### Authentication
**`app/routers/auth.py`**
- Handles Google OAuth callbacks
- Issues secure JWT tokens

### Analysis
**`app/routers/analyze.py`**
- Fetches GitHub repository data
- Calls Gemini API for:
  - Analysis
  - Scoring
  - Improvement roadmap
- Triggers email delivery

### Email Service
**`app/services/email_service.py`**
- `generate_pdf()` creates analysis reports
- `send_email()` uses `SendGridAPIClient` for reliable HTTPS-based email delivery

### Main Application
**`main.py`**
- Initializes FastAPI and CORS middleware
- Starts the Keep-Alive thread on application startup
- Continuously pings the Render service URL

---

## Setup and Configuration

### Prerequisites
- Python 3.10+
- pip
- SendGrid account with:
  - Verified sender email
  - API key
- Google OAuth credentials (Client ID & Secret)

---

## Local Setup

### Clone the Repository
```bash
git clone https://github.com/Kartikey1405/GitGrade.git
cd GitGrade
