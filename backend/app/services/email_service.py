from fpdf import FPDF
import os
import base64 # Required for encoding the PDF file
from app.config import Config 

#  NEW IMPORTS for SendGrid API
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)


class EmailService:
    def generate_pdf(self, analysis_data):
        """
        Generates a PDF report from the AnalysisResult object.
        (PDF generation logic remains unchanged)
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # --- Header ---
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, f"GitGrade Analysis Report", ln=True, align='C')
        pdf.ln(10)

        # --- Repository Details ---
        pdf.set_font("Arial", 'B', 12)
        owner = getattr(analysis_data.details, 'owner', 'Unknown')
        name = getattr(analysis_data.details, 'name', 'Repo')
        language = getattr(analysis_data.details, 'language', 'Unknown')
        stars = getattr(analysis_data.details, 'stars', 0)
        forks = getattr(analysis_data.details, 'forks', 0)

        pdf.cell(0, 10, f"Repository: {owner}/{name}", ln=True)
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f"Language: {language}", ln=True)
        pdf.cell(0, 8, f"Stars: {stars} | Forks: {forks}", ln=True)
        pdf.ln(5)

        # --- Scores ---
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Final Grade: {analysis_data.score}/100", ln=True)
        pdf.ln(5)

        # --- Executive Summary ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Executive Summary:", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, self._clean_text(analysis_data.summary))
        pdf.ln(5)

        # --- Roadmap ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Improvement Roadmap:", ln=True)
        
        pdf.set_font("Arial", '', 11)
        roadmap_items = analysis_data.roadmap if analysis_data.roadmap else []
        
        for i, item in enumerate(roadmap_items, 1):
            if hasattr(item, 'title'): 
                title = self._clean_text(item.title)
                category = self._clean_text(item.category)
                desc = self._clean_text(item.description)
                
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 8, f"{i}. {title} [{category}]", ln=True)
                
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 6, desc)
                pdf.ln(3)
            else:
                clean_item = self._clean_text(str(item))
                pdf.multi_cell(0, 8, f"{i}. {clean_item}")

        # --- Save PDF ---
        if not os.path.exists("reports"):
            os.makedirs("reports")
            
        file_path = f"reports/{name}_report.pdf"
        pdf.output(file_path)
        return file_path

    def _clean_text(self, text):
        """Helper to handle encoding issues with FPDF"""
        if not text: 
            return ""
        text = str(text).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-')
        return text.encode('latin-1', 'ignore').decode('latin-1')

    def send_email(self, to_email, pdf_path):
        """
        Sends the generated PDF via the robust SendGrid API (HTTPS).
        This bypasses all cloud firewall/SMTP handshake issues.
        """
        from_email = Config.SMTP_EMAIL
        # SMTP_PASSWORD holds the SendGrid API Key (SG.xxxx)
        api_key = Config.SMTP_PASSWORD 

        if not from_email or not api_key:
            print(f"❌ CREDENTIAL ERROR: Could not find SMTP_EMAIL or SendGrid API Key in Config.")
            return False

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='Your GitGrade Analysis Report 🚀',
            html_content='<strong>Here is your detailed GitHub analysis report attached below.</strong><br><br>Keep coding!<br>- The GitGrade Team'
        )

        # Add the PDF attachment
        try:
            with open(pdf_path, 'rb') as f:
                data = f.read()
            encoded_file = base64.b64encode(data).decode()
        except FileNotFoundError:
            print(f"❌ PDF File not found: {pdf_path}")
            return False
        
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(pdf_path)),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

        try:
            # Send email via HTTPS API call
            sg = SendGridAPIClient(api_key)
            # The API call uses standard HTTPS (Port 443), which cannot be blocked.
            response = sg.send(message)
            
            if response.status_code >= 200 and response.status_code < 300:
                print(f"✅ SendGrid API Success. Status: {response.status_code}")
                return True
            else:
                # Log the specific SendGrid API error for debugging
                print(f"❌ SendGrid API Error. Status: {response.status_code}")
                print(f"Response Body: {response.body}")
                return False
                
        except Exception as e:
            print(f"SendGrid API Exception: {e}")
            return False
