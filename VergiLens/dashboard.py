import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="VergiLens AI | 2026",
    layout="wide",
    page_icon="🦅",
    initial_sidebar_state="expanded"
)

# --- THEME: FUTURE DUSK & GLASSMORPHISM ---
# Bu CSS, arkaplanı, kartları ve metinleri tamamen değiştirir.
st.markdown("""
    <style>
    /* 1. Arkaplan: Future Dusk (Karanlık Menekşe - Gece Mavisi) Gradyanı */
    .stApp {
        background: rgb(15,23,42);
        background: linear-gradient(160deg, rgba(15,23,42,1) 0%, rgba(30,27,75,1) 50%, rgba(49,46,129,1) 100%);
    }

    /* 2. Kenar Çubuğu (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: rgba(17, 24, 39, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3. Kartlar (Metrics & Containers) - Buzlu Cam Efekti */
    div[data-testid="stMetric"], div[data-testid="stContainer"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }

    /* 4. Başlıklar ve Metinler */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #E2E8F0 !important;
        font-weight: 200;
    }
    .big-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(0deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 5. Butonlar */
    .stButton > button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
    }
    
    /* 6. Gereksiz Streamlit öğelerini gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK ALANI ---
col_logo, col_title = st.columns([1, 6])
with col_title:
    st.markdown('<div class="big-title">VergiLens AI</div>', unsafe_allow_html=True)
    st.markdown("##### <span style='color:#94a3b8'>Mevzuat Uyum & Anomali Tespit Platformu</span>", unsafe_allow_html=True)

st.markdown("---")

# --- YAN MENÜ ---
with st.sidebar:
    st.header("🎛️ Kontrol Paneli")
    
    with st.container():
        st.caption("HEDEF MÜKELLEF")
        tax_id = st.text_input("VKN / TCKN", value="12345678", help="Simülasyon ID")
        
        st.caption("DENETİM MODU")
        audit_scope = st.selectbox("Mod Seçimi", 
            ["⚡ Hızlı Risk Taraması", "🛡️ Tam Kapsamlı Denetim", "⚖️ Sadece Mevzuat"])
    
    st.markdown("###")
    
    if st.button("DENETİMİ BAŞLAT", use_container_width=True):
        with st.spinner('Veri tabanları taranıyor...'):
            try:
                response = requests.post(
                    "http://localhost:8000/audit/full-scan",
                    json={"tax_id": tax_id, "query": "Cezai işlem gerektirir mi?"},
                    timeout=10
                )
                if response.status_code == 200:
                    st.session_state['result'] = response.json()
                    st.toast('Analiz Tamamlandı', icon='🦅')
                else:
                    st.error("Sunucu Hatası")
            except:
                st.error("Backend Bağlantısı Yok")

# --- SONUÇ ALANI ---
if 'result' in st.session_state:
    res = st.session_state['result']
    risk_data = res.get("risk_analysis", {})
    legal_data = res.get("legal_context", [])
    score = risk_data.get('risk_score', 0)

    # 1. KPI KARTLARI (Buzlu Cam)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Denetlenen VKN", risk_data.get('tax_id', '-'))
    
    # Renkli Risk Göstergesi
    risk_text = risk_data.get('risk_level', '-')
    kpi2.metric("Risk Seviyesi", risk_text, f"%{score} Skor", delta_color="inverse")
    
    kpi3.metric("Anomali Sayısı", len(risk_data.get('anomalies', [])))
    kpi4.metric("Mevzuat Eşleşmesi", len(legal_data))

    st.markdown("###")

    # 2. DETAY SEKMELERİ
    tab_risk, tab_legal = st.tabs(["📊 ANOMALİ GRAFİĞİ", "⚖️ MEVZUAT RAPORU"])

    with tab_risk:
        c1, c2 = st.columns([1, 2])
        with c1:
            # Modern Gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Entropi Skoru", 'font': {'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "white"},
                    'bar': {'color': "#ef4444" if score>70 else "#f59e0b" if score>40 else "#10b981"},
                    'bgcolor': "rgba(255,255,255,0.1)",
                    'bordercolor': "rgba(255,255,255,0.2)"
                }
            ))
            fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True) # DEPRECATION FIX BURADA
        
        with c2:
            st.markdown("#### Tespit Edilen Bulgular")
            if risk_data.get('anomalies'):
                for note in risk_data['anomalies']:
                    st.error(f"🚨 {note}")
            else:
                st.success("Temiz Kayıt - Anomali Saptanmadı")

    with tab_legal:
        st.markdown("#### İlgili Kanun Maddeleri (RAG Engine)")
        for item in legal_data:
            st.info(f"**Kaynak:** {item['source']} (Alaka: %{int(item['score']*100)})")
            st.markdown(f"> *{item['text']}*")

# --- BAŞLANGIÇ EKRANI (Placeholder) ---
else:
    # O saçma resim yerine temiz bir "Hazır" ekranı
    st.markdown("###")
    with st.container():
        st.markdown("""
        <div style="text-align: center; padding: 50px; border: 1px dashed rgba(255,255,255,0.2); border-radius: 15px;">
            <h2 style="color: #6366f1;">Sistem Hazır</h2>
            <p style="color: #94a3b8;">Yapay zeka destekli denetim başlatmak için sol menüyü kullanın.</p>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                <span style="background: rgba(99, 102, 241, 0.2); padding: 5px 15px; border-radius: 20px; color: #a5b4fc; font-size: 0.8rem;">● RAG Active</span>
                <span style="background: rgba(16, 185, 129, 0.2); padding: 5px 15px; border-radius: 20px; color: #6ee7b7; font-size: 0.8rem;">● Risk Engine Online</span>
            </div>
        </div>
        """, unsafe_allow_html=True)