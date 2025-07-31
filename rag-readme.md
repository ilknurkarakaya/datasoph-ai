# 🔍 DATASOPH AI - RAG System Documentation

## 🎯 **Genel Bakış**

DATASOPH AI RAG (Retrieval-Augmented Generation) sistemi, kullanıcıların PDF, DOCX, TXT, CSV ve JSON dosyalarını yükleyip bu belgelerden bilgi çekebilmelerini sağlayan gelişmiş bir yapay zeka modülüdür.

## 🏗️ **Sistem Mimarisi**

### **1. Document Processor**
- **Dosya İşleme**: PDF, DOCX, TXT, CSV, JSON dosyalarını işleme
- **Chunking**: Metni anlamlı parçalara bölme
- **Metadata Extraction**: Dosya bilgilerini çıkarma

### **2. Vector Store (ChromaDB)**
- **Embedding Generation**: Metinleri vektörlere dönüştürme
- **Similarity Search**: Benzerlik araması
- **Persistent Storage**: Kalıcı vektör depolama

### **3. RAG Pipeline**
- **Document Upload**: Belge yükleme ve işleme
- **Question Answering**: Soru-cevap sistemi
- **Context Retrieval**: İlgili bağlamı bulma

## 🚀 **Özellikler**

### **✅ Desteklenen Dosya Türleri**
- **PDF**: PDF belgeleri
- **DOCX**: Word belgeleri
- **TXT**: Metin dosyaları
- **CSV**: Veri dosyaları
- **JSON**: JSON veri dosyaları

### **✅ Gelişmiş Özellikler**
- **Semantic Search**: Anlamsal arama
- **Context-Aware Answers**: Bağlam farkında cevaplar
- **Source Attribution**: Kaynak atıfı
- **Multi-Document Support**: Çoklu belge desteği
- **Chunking Optimization**: Optimize edilmiş parçalama

## 📋 **Gereksinimler**

```bash
# RAG System Requirements
langchain>=0.3.0
langchain-openai>=0.3.0
langchain-community>=0.3.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
pypdf>=3.15.0
python-docx>=0.8.11
pandas>=2.0.0
numpy>=1.20.0
streamlit>=1.25.0
openai>=1.0.0
faiss-cpu>=1.7.0
tiktoken>=0.5.0
```

## 🛠️ **Kurulum**

### **1. Bağımlılıkları Yükleme**
```bash
cd rag_system
pip install -r requirements.txt
```

### **2. Environment Variables**
```bash
# .env dosyası
OPENAI_API_KEY=your_openai_api_key_here
```

### **3. Sistem Başlatma**
```python
from rag_pipeline import RAGPipeline

# RAG sistemi başlatma
rag = RAGPipeline(api_key="your_api_key")
```

## 🎯 **Kullanım**

### **1. Belge Yükleme**
```python
# Tek dosya yükleme
result = rag.upload_documents(['document.pdf'])

# Çoklu dosya yükleme
result = rag.upload_documents(['doc1.pdf', 'doc2.docx', 'data.csv'])

# Sonuç kontrolü
if result["success"]:
    print(f"✅ {result['documents_processed']} belge işlendi")
    print(f"📄 {result['chunks_created']} parça oluşturuldu")
```

### **2. Soru Sorma**
```python
# Basit soru
answer = rag.ask_question("Bu belge ne hakkında?")

# Detaylı soru
answer = rag.ask_question("Machine learning algoritmaları nelerdir?", k=10)

# Sonuç kontrolü
if answer["success"]:
    print(f"🤖 Cevap: {answer['answer']}")
    print(f"📚 Kaynaklar: {answer['sources']}")
    print(f"📄 Bağlam belgeleri: {answer['context_documents']}")
```

### **3. Sistem İstatistikleri**
```python
# Sistem durumu
stats = rag.get_system_stats()
print(f"RAG Sistemi: {stats['rag_system']}")
print(f"API Bağlı: {stats['api_connected']}")
print(f"Toplam Belge: {stats['vector_store']['total_documents']}")
```

## 🔧 **Teknik Detaylar**

### **1. Document Processing Pipeline**

```python
# Belge işleme süreci
document_processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)

# Dosya işleme
documents = document_processor.process_document('sample.pdf')

# Çoklu dosya işleme
documents = document_processor.process_multiple_documents(['file1.pdf', 'file2.docx'])

# Özet alma
summary = document_processor.get_document_summary(documents)
```

### **2. Vector Store Operations**

```python
# Vector store başlatma
vector_store = VectorStore(persist_directory="./vectorstore")

# Belge ekleme
success = vector_store.add_documents(documents)

# Benzerlik araması
results = vector_store.similarity_search("query", k=5)

# İstatistikler
stats = vector_store.get_collection_stats()
```

### **3. RAG Pipeline Workflow**

```python
# 1. Belge yükleme ve işleme
documents = document_processor.process_multiple_documents(file_paths)

# 2. Vector store'a ekleme
vector_store.add_documents(documents)

# 3. Soru sorma ve cevap alma
similar_docs = vector_store.similarity_search(question, k=5)
context = "\n\n".join([doc.page_content for doc, _ in similar_docs])

# 4. LLM ile cevap üretme
response = llm_chain.run({"context": context, "question": question})
```

## 📊 **Performans Metrikleri**

### **İşleme Hızları**
- **PDF İşleme**: ~2-5 saniye/sayfa
- **DOCX İşleme**: ~1-3 saniye/sayfa
- **TXT İşleme**: ~0.5-1 saniye/dosya
- **CSV İşleme**: ~1-2 saniye/dosya

### **Arama Performansı**
- **Similarity Search**: < 1 saniye
- **Context Retrieval**: < 2 saniye
- **Answer Generation**: 3-10 saniye (API bağlı)

### **Depolama**
- **Vector Storage**: ChromaDB ile kalıcı depolama
- **Embedding Model**: OpenAI text-embedding-ada-002
- **Chunk Size**: 1000 karakter (varsayılan)
- **Chunk Overlap**: 200 karakter (varsayılan)

## 🧪 **Test Sistemi**

### **Test Çalıştırma**
```bash
cd rag_system
python test_rag.py
```

### **Test Kapsamı**
- ✅ Document Processor Tests
- ✅ Vector Store Tests
- ✅ RAG Pipeline Tests
- ✅ Integration Tests
- ✅ Error Handling Tests

### **Demo Çalıştırma**
```bash
cd rag_system
python rag_demo.py
```

## 🔍 **Kullanım Senaryoları**

### **1. Akademik Araştırma**
```python
# Araştırma makalelerini yükleme
rag.upload_documents(['paper1.pdf', 'paper2.pdf', 'paper3.pdf'])

# Spesifik sorular sorma
answer = rag.ask_question("Bu makalelerde hangi machine learning algoritmaları kullanılmış?")
```

### **2. İş Dokümantasyonu**
```python
# Şirket dokümanlarını yükleme
rag.upload_documents(['policy.pdf', 'procedures.docx', 'guidelines.txt'])

# Politika soruları
answer = rag.ask_question("Çalışan izin politikası nedir?")
```

### **3. Veri Analizi**
```python
# CSV verilerini yükleme
rag.upload_documents(['sales_data.csv', 'customer_data.csv'])

# Veri analizi soruları
answer = rag.ask_question("En çok satış yapılan bölge hangisi?")
```

## 🚀 **Gelişmiş Özellikler**

### **1. Custom Chunking**
```python
# Özel chunk boyutları
processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
```

### **2. Metadata Filtering**
```python
# Metadata ile filtreleme
results = vector_store.similarity_search(
    "query", 
    filter_metadata={"file_type": ".pdf"}
)
```

### **3. System Reset**
```python
# Sistemi sıfırlama
success = rag.reset_system()
```

### **4. Export System Info**
```python
# Sistem bilgilerini dışa aktarma
info = rag.export_system_info()
```

## 🔒 **Güvenlik ve Hata Yönetimi**

### **1. Dosya Güvenliği**
- Dosya türü doğrulama
- Boyut sınırlamaları
- Güvenli dosya işleme

### **2. Hata Yönetimi**
- Graceful error handling
- Detailed error messages
- Fallback mechanisms

### **3. API Güvenliği**
- Environment variable kullanımı
- API key koruması
- Rate limiting

## 📈 **Optimizasyon**

### **1. Chunking Optimizasyonu**
- Semantic chunking
- Context-aware splitting
- Overlap optimization

### **2. Vector Search Optimizasyonu**
- Index optimization
- Query optimization
- Caching strategies

### **3. Memory Management**
- Efficient document processing
- Vector storage optimization
- Garbage collection

## 🔮 **Gelecek Geliştirmeler**

### **Kısa Vadeli (1-3 ay)**
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Real-time document updates
- [ ] Conversation memory

### **Orta Vadeli (3-6 ay)**
- [ ] Fine-tuning capabilities
- [ ] Custom embedding models
- [ ] Advanced RAG techniques
- [ ] Multi-modal support

### **Uzun Vadeli (6+ ay)**
- [ ] Distributed processing
- [ ] Advanced analytics
- [ ] Enterprise features
- [ ] API marketplace

## 🆘 **Troubleshooting**

### **Yaygın Sorunlar**

#### **1. API Key Hatası**
```python
# Çözüm: Environment variable ayarlama
import os
os.environ["OPENAI_API_KEY"] = "your_api_key"
```

#### **2. Dosya Yükleme Hatası**
```python
# Çözüm: Dosya türü kontrolü
supported_types = ['.pdf', '.docx', '.txt', '.csv', '.json']
```

#### **3. Vector Store Hatası**
```python
# Çözüm: Vector store sıfırlama
rag.reset_system()
```

### **Debug Modu**
```python
# Detaylı loglama
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 **Destek**

### **Dokümantasyon**
- [RAG System Guide](rag-readme.md)
- [API Reference](docs/api.md)
- [Tutorial Videos](docs/tutorials.md)

### **Topluluk**
- [GitHub Issues](https://github.com/ilknurkarakaya/datasoph-ai/issues)
- [Discord Community](https://discord.gg/datasoph)
- [Email Support](support@datasoph.ai)

---

## 🎉 **Sonuç**

DATASOPH AI RAG sistemi, kullanıcıların belgelerini yükleyip bu belgelerden bilgi çekebilmelerini sağlayan güçlü bir yapay zeka modülüdür. Gelişmiş belge işleme, vektör depolama ve anlamsal arama özellikleri ile kullanıcılara kesin ve bağlamsal cevaplar sunar.

**GitHub Repository**: https://github.com/ilknurkarakaya/datasoph-ai 