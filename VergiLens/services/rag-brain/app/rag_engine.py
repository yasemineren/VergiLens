import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter

# 🛑 KRİTİK AYAR: OpenAI'yı Devre Dışı Bırak (Global Config)
# Bu ayarları sınıfın dışına, en tepeye yazıyoruz.
print("⚙️  AI Modelleri Yükleniyor (Lokal)...")
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

class MevzuatRAG:
    def __init__(self):
        print("🧠 RAG Motoru Başlatılıyor...")
        self.index = None
        self._build_index()

    def _build_index(self):
        """
        Kanun metinlerini okur ve vektör veritabanına gömer.
        """
        # data klasörünün yolunu dinamik olarak bul
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "../data")
        
        if not os.path.exists(data_path):
            print(f"⚠️ HATA: {data_path} bulunamadı!")
            return

        print("📚 Dokümanlar okunuyor...")
        documents = SimpleDirectoryReader(data_path).load_data()
        
        # Metni mantıklı parçalara böl
        parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        
        print("🔢 Vektörleştirme (Embedding) işlemi başladı...")
        self.index = VectorStoreIndex.from_documents(
            documents, 
            transformations=[parser]
        )
        print("✅ İndeksleme tamamlandı! Mevzuat hafızaya alındı.")

    def search(self, query: str, k=3):
        if not self.index:
            return [{"text": "Sistem hazır değil.", "score": 0}]
            
        retriever = self.index.as_retriever(similarity_top_k=k)
        results = retriever.retrieve(query)
        
        evidence = []
        for node in results:
            evidence.append({
                "score": round(node.score, 3), 
                "text": node.text,
                "source": node.metadata.get('file_name', 'Bilinmeyen')
            })
        
        return evidence