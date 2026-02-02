# 🦅 VergiLens: AI-Powered Digital Tax Auditor

![Python](https://img.shields.io/badge/Python-3.9-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green) ![Architecture](https://img.shields.io/badge/Architecture-Microservices-orange) ![Status](https://img.shields.io/badge/Status-Prototype-red)

**VergiLens**, büyük veri analitiği, RAG (Retrieval-Augmented Generation) ve anomali tespiti yöntemlerini kullanarak dijital vergi denetimi yapan yeni nesil bir platformdur.

## 🚀 Özellikler (Features)

- **🔍 Mevzuat RAG Motoru:** Vergi kanunlarını ve tebliğleri vektörel olarak tarar ve kaynak göstererek cevaplar.
- **⚡ Risk Skorlama (Anomaly Detection):** *Isolation Forest* ve *Graph Theory* kullanarak sahte fatura döngülerini ve vergi kaçağı örüntülerini yakalar.
- **🛡️ Audit Logging:** Tüm sorgu ve işlemler değiştirilemez bir denetim kaydına alınır.

## 🏗️ Mimari (Architecture)

Proje **Monorepo** yapısında olup şu servislerden oluşur:

| Servis | Teknoloji | Görev |
|--------|-----------|-------|
| `rag-brain` | Python / FastAPI | AI, RAG ve Risk Analizi |
| `gateway-guard` | Java / Spring Boot | API Gateway & Security (WIP) |
| `infra` | Docker / Postgres | Veri ve Altyapı |

## 🛠️ Kurulum (Installation)

```bash
# Projeyi klonlayın
git clone [https://github.com/KULLANICI_ADIN/VergiLens.git](https://github.com/KULLANICI_ADIN/VergiLens.git)

# Docker ile tüm sistemi ayağa kaldırın
docker-compose up --build