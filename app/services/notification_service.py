from app.services.whatsapp_service import WhatsAppService
wa = WhatsAppService()


def send_summary_whatsapp(user, summary_data):
    if not user.whatsapp_opt_in or not user.phone:
        return

    wa.send_template(
        phone=user.phone,
        template="daily_summary",
        params=[
            user.name,
            summary_data["retarget"],
            summary_data["contacted"],
            summary_data["meetings"],
            summary_data["scraped"],
        ],
    )
