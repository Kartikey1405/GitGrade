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
   
    txn_id = str(uuid.uuid4())
    
  
    params = {
        "pa": Config.PAYMENT_UPI_ID, 
        "pn": "GitGrade Support",    
        "tn": request.message,        
        "am": str(request.amount),   
        "cu": "INR"                   
    }
    
    query_string = urllib.parse.urlencode(params)
    upi_link = f"upi://pay?{query_string}"
    
    return PaymentLinkResponse(
        payment_url=upi_link,
        transaction_id=txn_id
    )
