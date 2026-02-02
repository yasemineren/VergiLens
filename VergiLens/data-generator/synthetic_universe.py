import pandas as pd
import numpy as np
from faker import Faker
import uuid
import random
from datetime import datetime, timedelta

# Fizikçi Dokunuşu: Deterministik kaos için tohum (seed) ekiyoruz.
Faker.seed(42)
np.random.seed(42)
fake = Faker('tr_TR')

def create_taxpayers(n=100):
    """
    Mükellef (Node) evrenini yaratır.
    """
    data = []
    sectors = ['Teknoloji', 'İnşaat', 'Tekstil', 'Lojistik', 'Danışmanlık']
    
    for _ in range(n):
        data.append({
            'tax_id': str(uuid.uuid4())[:8],
            'company_name': fake.company(),
            'sector': random.choice(sectors),
            'city': fake.city(),
            'risk_label': 0  # Varsayılan: Temiz
        })
    return pd.DataFrame(data)

def inject_fraud_ring(df, n_fraudsters=5):
    """
    Özel Görev: Sisteme bir 'Sahte Fatura Çetesi' (Düşük Entropi Grubu) ekler.
    Bu şirketler birbirine dairesel fatura kesecek (Circular Trading).
    """
    fraud_indices = df.sample(n_fraudsters).index
    df.loc[fraud_indices, 'risk_label'] = 1
    
    # Çete üyelerini işaretleyelim
    fraudsters = df.loc[fraud_indices, 'tax_id'].tolist()
    print(f"🕵️  Tespit Edilecek 'Gölge' Şirketler: {fraudsters}")
    return df, fraudsters

def generate_transactions(users_df, fraudsters, n_transactions=5000):
    """
    İşlemleri (Edges) oluşturur.
    Burada 'Finansal Termodinamik' devreye giriyor:
    - Normal işlemler: Benford yasasına uygun, gürültülü (random) tutarlar.
    - Hileli işlemler: Yuvarlak, tekrarlayan ve döngüsel.
    """
    transactions = []
    user_ids = users_df['tax_id'].tolist()
    
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(n_transactions):
        # 1. Taraf seçimi (Gönderici -> Alıcı)
        sender = random.choice(user_ids)
        receiver = random.choice(user_ids)
        while sender == receiver:
            receiver = random.choice(user_ids)
            
        date = start_date + timedelta(days=random.randint(0, 365))
        
        # 2. Tutar Belirleme (Fizik Modeli)
        if sender in fraudsters and receiver in fraudsters:
            # SUÇ MODELİ: Şüpheli derecede düzgün rakamlar (Düşük Entropi)
            # Örn: 50.000, 100.000 gibi
            amount = random.choice([50000, 75000, 100000, 150000])
            is_laundering = 1
        else:
            # DOĞAL MODEL: Log-normal dağılım (Benford Yasası'na yakınsar)
            amount = round(np.random.lognormal(8, 1), 2)
            is_laundering = 0
            
        transactions.append({
            'date': date.strftime("%Y-%m-%d"),
            'sender_id': sender,
            'receiver_id': receiver,
            'amount': amount,
            'is_suspicious': is_laundering
        })
        
    return pd.DataFrame(transactions)

if __name__ == "__main__":
    print("🌌 VergiLens Evreni Oluşturuluyor...")
    
    # 1. Mükellefleri Yarat
    df_users = create_taxpayers(n=200)
    
    # 2. İçeriye 'Karanlık Madde' (Suçlu) Enjekte Et
    df_users, fraud_ring = inject_fraud_ring(df_users, n_fraudsters=10)
    
    # 3. Para Akışını (Enerji Transferi) Başlat
    df_transactions = generate_transactions(df_users, fraud_ring, n_transactions=10000)
    
    # 4. Kaydet
    df_users.to_csv("taxpayers.csv", index=False)
    df_transactions.to_csv("transactions.csv", index=False)
    
    print(f"✅ Evren Hazır! {len(df_users)} şirket ve {len(df_transactions)} işlem simüle edildi.")
    print("📂 Dosyalar: taxpayers.csv, transactions.csv")