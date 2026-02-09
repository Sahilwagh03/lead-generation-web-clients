from fastapi import APIRouter
from app.services.whatsapp_service import WhatsAppService

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

wa = WhatsAppService()


@router.post("/test")
def test_whatsapp(phone: str):
    return wa.send_template(
        phone,
        "daily_summary",
        ["User", "5", "2", "1", "20"]
    )
