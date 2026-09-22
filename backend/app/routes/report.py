from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services.report import generate_report

router = APIRouter(prefix="/api/report", tags=["report"])


@router.post("/generate")
def generate_pdf_report(payload: dict):
    try:
        inputs = payload.get("inputs", {})
        recommendations = payload.get("recommendations", [])
        compliance = payload.get("compliance", {"warnings": [], "info_notes": [], "disclaimer": ""})

        pdf_bytes = generate_report(inputs, recommendations, compliance)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=packsmart_report.pdf"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
