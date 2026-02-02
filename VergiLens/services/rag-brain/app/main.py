from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_engine import MevzuatRAG
from app.risk_engine import RiskEngine

app = FastAPI(title="VergiLens AI", version="0.3.0")

# İki motoru da başlat
rag_engine = MevzuatRAG()
risk_engine = RiskEngine()

class AuditRequest(BaseModel):
    tax_id: str
    query: str = "Bu durum için hangi ceza uygulanır?"

@app.post("/audit/full-scan")
def full_audit(request: AuditRequest):
    """
    UÇTAN UCA DENETİM:
    1. Risk Motoru: Mükellefin açığını bulur.
    2. RAG Motoru: O açık için kanun maddesini getirir.
    """
    print(f"🚨 Denetim Başladı: {request.tax_id}")
    
    # 1. Risk Analizi Yap
    risk_report = risk_engine.analyze_taxpayer(request.tax_id)
    
    # 2. Mevzuat Araştırması Yap (Risk raporundaki bulguya göre)
    # Eğer risk yüksekse "Kaçakçılık", düşükse genel bilgi arayalım.
    search_query = request.query
    if risk_report['risk_score'] > 50:
        search_query = "Vergi kaçakçılığı ve sahte fatura cezası nedir?"
        
    legal_evidence = rag_engine.search(search_query)
    
    return {
        "status": "Audit Complete",
        "risk_analysis": risk_report,
        "legal_context": legal_evidence
    }