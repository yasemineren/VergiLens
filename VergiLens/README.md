# 🦅 VergiLens: AI-Powered Digital Audit Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge&logo=fastapi)
![Status](https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge)

> **"Finansal Termodinamik Yaklaşımıyla Vergi Denetimi"**
>
> VergiLens; büyük veri analitiği, RAG (Retrieval-Augmented Generation) ve fizik tabanlı anomali tespiti (Entropi Analizi) yöntemlerini birleştirerek dijital vergi denetimi yapan yeni nesil bir yapay zeka platformudur.

---

## 📸 Proje Önizlemesi

| 🚨 Risk Analizi (Kırmızı Alarm) | ⚖️ Mevzuat & Hukuki Dayanak |
|---------------------------------|-----------------------------|
| ![Risk Ekranı](https://via.placeholder.com/600x300/1e1e2e/e53e3e?text=Anomaly+Detection+Dashboard) | ![Mevzuat Ekranı](https://via.placeholder.com/600x300/1e1e2e/4fd1c5?text=Legal+RAG+Evidence) |
*Simülasyon ortamında tespit edilen yüksek riskli (döngüsel işlem) mükellef analizi.*

---

## 💡 Temel Felsefe: "Finansal Entropi"

Bir fizikçi gözüyle bakıldığında, doğal finansal akışlar yüksek entropiye (düzensizliğe) sahiptir. Ancak vergi kaçakçılığı ve sahte fatura döngüleri, **"yapay bir düzen"** (düşük entropi) içerir.

Bu projede:
1.  **Graph Theory:** Para transferleri bir ağ (network) olarak modellenmiş, döngüsel (A→B→C→A) işlemler tespit edilmiştir.
2.  **Entropi Analizi:** Fatura tutarlarındaki rakam dağılımı (Benford Yasası) ve işlem sıklığı, termodinamik sistemler gibi analiz edilerek anomaliler yakalanmıştır.
3.  **LLM & RAG:** Tespit edilen suç unsuru, *Vergi Usul Kanunu (VUK)* ile eşleştirilerek hukuki gerekçesi (Kanıt Zinciri) sunulmuştur.

---

## 🛠️ Teknik Mimari (Tech Stack)

* **Frontend:** Streamlit (Future Dusk Theme, Glassmorphism UI)
* **Backend:** FastAPI (Asenkron Mikroservis)
* **AI Engine:**
    * *RAG:* LlamaIndex + HuggingFace (Local Embeddings - Privacy First)
    * *Risk:* Scikit-Learn (Isolation Forest), NetworkX (Graph Analysis)
* **Data:** Pandas (Sentetik Veri Üretimi), Plotly (Görselleştirme)
* **DevOps:** Docker (Containerization)

---

## 🚀 Kurulum ve Çalıştırma

Bu projeyi yerel makinenizde test etmek için:

```bash
# 1. Repoyu Klonlayın
git clone [https://github.com/KULLANICI_ADIN/VergiLens.git](https://github.com/KULLANICI_ADIN/VergiLens.git)
cd VergiLens

# 2. Backend Sunucusunu Başlatın (FastAPI)
cd services/rag-brain
uvicorn app.main:app --reload --port 8000

# 3. Dashboard'u Başlatın (Yeni Terminalde)
# (Ana dizine dönmeyi unutmayın)
cd ../../
streamlit run dashboard.py