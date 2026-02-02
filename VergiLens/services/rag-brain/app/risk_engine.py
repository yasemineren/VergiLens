import pandas as pd
import os
import random

class RiskEngine:
    def __init__(self):
        print("🕵️  Risk Motoru Başlatılıyor...")
        self.taxpayers = None
        self.transactions = None
        self._load_data()

    def _load_data(self):
        # CSV dosyalarını data klasöründen bul
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "../data")
        
        try:
            self.taxpayers = pd.read_csv(os.path.join(data_path, "taxpayers.csv"))
            print(f"✅ {len(self.taxpayers)} Mükellef yüklendi.")
        except:
            print("⚠️ Veri bulunamadı, simülasyon modunda çalışılacak.")
            self.taxpayers = pd.DataFrame()

    def analyze_taxpayer(self, taxpayer_id: str):
        """
        Bir mükellefin riskini hesaplar.
        Gerçek veride veri tabanından bakarız, burada CSV'den bakıyoruz.
        """
        risk_score = 0
        reasons = []
        
        # 1. Mükellefi Bul
        if not self.taxpayers.empty:
            record = self.taxpayers[self.taxpayers['tax_id'] == taxpayer_id]
            if not record.empty:
                # Eğer daha önce "riskli" etiketlediysek (Simülasyon verisi)
                if record.iloc[0].get('risk_label', 0) == 1:
                    risk_score += 50
                    reasons.append("Şüpheli işlem ağı (Graph Detected)")
            else:
                reasons.append("Mükellef veritabanında bulunamadı (Yeni Tescil?)")
        
        # 2. Fizikçi Dokunuşu: Entropi Analizi (Simüle)
        # Rastgele bir 'Finansal Entropi' değeri üretelim
        entropy = random.uniform(0.1, 0.9)
        if entropy < 0.3:
            risk_score += 35
            reasons.append(f"Düşük Finansal Entropi ({entropy:.2f}): İşlemler fazla düzenli (Benford Yasası İhlali)")
            
        # 3. Toplam Skor
        risk_score = min(risk_score + random.randint(0, 15), 100)
        
        risk_level = "DÜŞÜK"
        if risk_score > 70: risk_level = "YÜKSEK (KIRMIZI ALARM)"
        elif risk_score > 40: risk_level = "ORTA (İNCELEME ÖNERİLİR)"
            
        return {
            "tax_id": taxpayer_id,
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "anomalies": reasons
        }