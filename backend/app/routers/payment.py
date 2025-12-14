from fastapi import APIRouter
from app.models import PaymentRequest, PaymentLinkResponse
from app.config import Config
import uuid
import urllib.parse

router = APIRouter()

@router.post("/generate-link", response_model=PaymentLinkResponse)
async def generate_payment_link(request: PaymentRequest):
    """
    Generates a UPI Payment Link (Standard Format).
    Frontend can turn this into a QR Code.
    """
    # Create a unique transaction ID
    txn_id = str(uuid.uuid4())
    
    # Construct the UPI string
    # upi://pay?pa=ADDRESS&pn=NAME&tn=NOTE&am=AMOUNT&cu=INR
    params = {
        "pa": Config.PAYMENT_UPI_ID,  # Your VPA from .env
        "pn": "GitGrade Support",     # Payee Name
        "tn": request.message,        # Note
        "am": str(request.amount),    # Amount
        "cu": "INR"                   # Currency
    }
    
    query_string = urllib.parse.urlencode(params)
    upi_link = f"upi://pay?{query_string}"
    
    return PaymentLinkResponse(
        payment_url=upi_link,
        transaction_id=txn_id
    )