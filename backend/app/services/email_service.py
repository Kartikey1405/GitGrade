from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import ssl 
from app.config import Config 

class EmailService:
    def generate_pdf(self, analysis_data):
        # ... (PDF generation logic unchanged) ...
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
        Sends the generated PDF via SMTP (SendGrid).
        """
        from_email = Config.SMTP_EMAIL
        # 🛑 The SendGrid API Key is read here as the password
        password = Config.SMTP_PASSWORD 

        if not from_email or not password:
            print(f"❌ CREDENTIAL ERROR: Could not find SMTP_EMAIL or SMTP_PASSWORD in Config.")
            print("Please check your .env file/Render config.")
            return False

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "Your GitGrade Analysis Report 🚀"

        body = "Here is your detailed GitHub analysis report attached below.\n\nKeep coding!\n- The GitGrade Team"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(pdf_path)}",
                )
                msg.attach(part)

            #  FINAL CODE: Connect to SendGrid SMTP (using starttls) and timeout
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=10)
            server.starttls()
            
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False
