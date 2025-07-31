# 📱 DATASOPH AI - Kullanıcı Akışı Dokümanı

## 🎯 **Proje Özeti**

DATASOPH AI, kullanıcıların veri analizi, doküman araştırması ve istatistiksel analiz yapabilmelerini sağlayan kapsamlı bir platformdur.

## 👥 **Hedef Kullanıcılar**

### **Birincil Kullanıcılar:**
- **Veri Bilimcileri** - Gelişmiş analiz ve görselleştirme araçlarına ihtiyaç duyanlar
- **İş Analistleri** - Kolay kullanılabilir veri içgörüleri ve raporlama isteyenler
- **Araştırmacılar** - Dokümanlarla sohbet edip içgörü çıkarmak isteyenler
- **Öğrenciler** - Veri bilimi öğrenen ve AI desteğine ihtiyaç duyanlar
- **Danışmanlar** - Taşınabilir, profesyonel veri analizi araçlarına ihtiyaç duyanlar

## 🔄 **Ana Kullanıcı Akışları**

### **1. Kayıt ve Giriş Akışı**

#### **1.1 İlk Kez Kullanıcı (Kayıt)**
```
1. Kullanıcı web uygulamasına gider (localhost:8501)
2. "Kayıt Ol" butonuna tıklar
3. Firebase Authentication ile:
   - Google hesabı ile giriş
   - Email/şifre ile kayıt
   - Telefon numarası ile doğrulama
4. Profil bilgilerini doldurur:
   - Ad-soyad
   - Şirket/organizasyon
   - Veri bilimi deneyim seviyesi
   - Tercih ettiği AI modeli
5. Hoş geldin ekranında özellikler tanıtılır
6. Ana dashboard'a yönlendirilir
```

#### **1.2 Mevcut Kullanıcı (Giriş)**
```
1. Kullanıcı web uygulamasına gider
2. "Giriş Yap" butonuna tıklar
3. Firebase Authentication ile giriş yapar
4. JWT token alır ve oturum başlatılır
5. Son oturum bilgileri yüklenir
6. Ana dashboard'a yönlendirilir
```

### **2. Veri Analizi Akışı**

#### **2.1 Veri Yükleme ve Analiz**
```
1. Kullanıcı "Veri Analizi" sekmesine gider
2. "Dosya Yükle" butonuna tıklar
3. Desteklenen formatları seçer:
   - CSV, Excel, JSON, Parquet
   - PDF, DOCX, TXT (doküman analizi için)
4. Dosyayı sürükleyip bırakır veya seçer
5. Dosya yüklenir ve işlenir:
   - Dosya boyutu kontrol edilir
   - Format doğrulanır
   - Veri önizlemesi gösterilir
6. "Analiz Et" butonuna tıklar
7. AI analiz türünü seçer:
   - Kapsamlı analiz
   - İstatistiksel analiz
   - Görselleştirme odaklı
   - Özel analiz parametreleri
8. Analiz başlatılır ve sonuçlar gösterilir
```

#### **2.2 Analiz Sonuçları**
```
1. Analiz tamamlandığında sonuçlar gösterilir:
   - Veri özeti (satır, sütun sayısı)
   - Eksik değer analizi
   - Veri tipleri ve dağılımlar
   - Korelasyon matrisi
   - Aykırı değer tespiti
2. Görselleştirmeler:
   - Histogramlar
   - Scatter plotlar
   - Box plotlar
   - Heat map'ler
3. AI önerileri:
   - İstatistiksel test önerileri
   - Makine öğrenmesi modelleri
   - İş içgörüleri
4. Kullanıcı sonuçları kaydedebilir veya paylaşabilir
```

### **3. Doküman Sohbeti (RAG) Akışı**

#### **3.1 Doküman Yükleme**
```
1. Kullanıcı "Doküman Sohbeti" sekmesine gider
2. "Doküman Yükle" butonuna tıklar
3. Desteklenen formatları seçer:
   - PDF, DOCX, TXT, MD
4. Dokümanı yükler
5. Doküman işlenir:
   - Metin çıkarılır
   - Chunk'lara bölünür
   - Vector database'e kaydedilir
6. İşlem tamamlandığında bildirim alır
```

#### **3.2 Dokümanla Sohbet**
```
1. Kullanıcı yüklenen dokümanları görür
2. Sohbet etmek istediği dokümanı seçer
3. Sohbet arayüzünde soru sorar:
   - "Bu dokümanın ana konusu nedir?"
   - "Belirli bir konu hakkında ne diyor?"
   - "Özet çıkarır mısın?"
4. AI dokümandan bilgi çıkararak cevap verir
5. Kaynak paragraflar gösterilir
6. Kullanıcı takip soruları sorabilir
7. Sohbet geçmişi kaydedilir
```

### **4. AI Sohbet Akışı**

#### **4.1 Genel AI Sohbeti**
```
1. Kullanıcı "AI Sohbet" sekmesine gider
2. Yeni sohbet başlatır veya mevcut sohbeti açar
3. AI modelini seçer:
   - Claude 3 Sonnet (varsayılan)
   - GPT-4
   - Llama 2
   - Mistral
4. Sohbet parametrelerini ayarlar:
   - Sıcaklık (creativity)
   - Maksimum token
   - Sistem prompt'u
5. Soru sorar veya görev verir
6. AI cevap verir ve konuşma devam eder
7. Sohbet geçmişi kaydedilir
```

#### **4.2 Uzmanlaşmış Sohbetler**
```
1. Kullanıcı sohbet türünü seçer:
   - Veri Analizi Uzmanı
   - İstatistik Uzmanı
   - Makine Öğrenmesi Uzmanı
   - İş Zekası Uzmanı
2. Uzman AI ile sohbet eder
3. Uzman özel araçları kullanır:
   - İstatistiksel testler
   - Görselleştirme araçları
   - Model eğitimi
4. Sonuçlar ve öneriler alır
```

### **5. Mobil Uygulama Akışı**

#### **5.1 Mobil Giriş**
```
1. Kullanıcı mobil uygulamayı açar
2. Firebase Authentication ile giriş yapar
3. Biyometrik kimlik doğrulama (opsiyonel)
4. Ana ekrana yönlendirilir
```

#### **5.2 Mobil Veri Analizi**
```
1. Kullanıcı "Veri Analizi" sekmesine gider
2. Kamera ile fotoğraf çeker veya galeriden seçer
3. OCR ile veri çıkarılır
4. Analiz başlatılır
5. Sonuçlar mobil uyumlu görselleştirmelerle gösterilir
```

#### **5.3 Mobil Doküman Sohbeti**
```
1. Kullanıcı "Doküman Sohbeti" sekmesine gider
2. Dokümanı mobil cihazdan yükler
3. Ses ile soru sorabilir
4. AI ses ile cevap verir
5. Sonuçlar paylaşılabilir
```

## 🎨 **Kullanıcı Arayüzü Akışları**

### **Web Uygulaması (Streamlit)**

#### **Ana Dashboard**
```
┌─────────────────────────────────────┐
│ 📊 DATASOPH AI - Ana Dashboard     │
├─────────────────────────────────────┤
│ [Veri Analizi] [Doküman Sohbeti]   │
│ [AI Sohbet] [Profil] [Ayarlar]     │
├─────────────────────────────────────┤
│ Son Aktiviteler:                    │
│ • 3 analiz tamamlandı              │
│ • 2 doküman yüklendi               │
│ • 5 sohbet oturumu                 │
├─────────────────────────────────────┤
│ Hızlı Eylemler:                     │
│ [Dosya Yükle] [Yeni Sohbet]        │
│ [Doküman Yükle] [Analiz Başlat]    │
└─────────────────────────────────────┘
```

#### **Veri Analizi Sayfası**
```
┌─────────────────────────────────────┐
│ 📈 Veri Analizi                     │
├─────────────────────────────────────┤
│ Dosya Yükleme Alanı:               │
│ ┌─────────────────────────────────┐ │
│ │ Dosyayı buraya sürükleyin      │ │
│ │ veya tıklayarak seçin          │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ Analiz Türü:                       │
│ ○ Kapsamlı Analiz                 │
│ ○ İstatistiksel Analiz            │
│ ○ Görselleştirme Odaklı           │
│ ○ Özel Analiz                     │
├─────────────────────────────────────┤
│ [Analiz Başlat] [Geçmiş Analizler] │
└─────────────────────────────────────┘
```

#### **Doküman Sohbeti Sayfası**
```
┌─────────────────────────────────────┐
│ 📚 Doküman Sohbeti                 │
├─────────────────────────────────────┤
│ Yüklenen Dokümanlar:               │
│ • rapor.pdf (2.3MB)               │
│ • analiz.docx (1.1MB)             │
│ • veri.txt (0.5MB)                │
├─────────────────────────────────────┤
│ Sohbet Alanı:                      │
│ ┌─────────────────────────────────┐ │
│ │ Kullanıcı: Bu raporun ana      │ │
│ │ konusu nedir?                  │ │
│ │                                 │ │
│ │ AI: Bu rapor, şirketin Q4      │ │
│ │ performansını analiz ediyor... │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ [Soru Sor] [Kaynakları Göster]     │
└─────────────────────────────────────┘
```

### **Mobil Uygulama (Flutter)**

#### **Ana Ekran**
```
┌─────────────────────────────────────┐
│ 📱 DATASOPH AI                     │
├─────────────────────────────────────┤
│ 👤 Kullanıcı Adı                   │
│ 📊 Son Analizler                   │
│ 📚 Yüklenen Dokümanlar             │
│ 💬 Aktif Sohbetler                 │
├─────────────────────────────────────┤
│ [📊 Analiz] [📚 Doküman] [💬 Sohbet] │
└─────────────────────────────────────┘
```

## 🔧 **Teknik Kullanıcı Akışları**

### **API Kullanımı**

#### **1. Kimlik Doğrulama**
```bash
# 1. Firebase token al
curl -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# 2. JWT token al
curl -X POST "http://localhost:8000/auth/firebase-login" \
  -H "Content-Type: application/json" \
  -d '{"firebase_token":"firebase_token_here"}'
```

#### **2. Veri Yükleme**
```bash
# 3. Dosya yükle
curl -X POST "http://localhost:8000/analysis/upload" \
  -H "Authorization: Bearer jwt_token_here" \
  -F "file=@data.csv"
```

#### **3. Analiz Başlatma**
```bash
# 4. Analiz başlat
curl -X POST "http://localhost:8000/analysis/analyze" \
  -H "Authorization: Bearer jwt_token_here" \
  -H "Content-Type: application/json" \
  -d '{"analysis_type":"comprehensive"}'
```

### **Docker Kullanımı**

#### **1. Servisleri Başlatma**
```bash
# Tüm servisleri başlat
docker-compose up -d

# Servis durumlarını kontrol et
docker-compose ps

# Logları görüntüle
docker-compose logs -f backend
```

#### **2. Veritabanı Yönetimi**
```bash
# PostgreSQL'e bağlan
docker exec -it datasoph-postgres psql -U datasoph -d datasoph

# Redis'e bağlan
docker exec -it datasoph-redis redis-cli
```

## 📊 **Kullanıcı Metrikleri ve Analiz**

### **Performans Metrikleri**
- **Sayfa Yükleme Süresi**: < 3 saniye
- **API Yanıt Süresi**: < 2 saniye
- **Dosya Yükleme**: < 10MB/saniye
- **Analiz Süresi**: < 30 saniye (ortalama)

### **Kullanıcı Deneyimi Metrikleri**
- **İlk Kullanım Tamamlama**: %85
- **Kullanıcı Memnuniyeti**: 4.5/5
- **Günlük Aktif Kullanıcı**: Hedef 1000+
- **Aylık Kullanıcı Tutma**: %90

### **İş Metrikleri**
- **Analiz Başına Ortalama Süre**: 15 dakika
- **Doküman Başına Sohbet**: 8 mesaj
- **Kullanıcı Başına Aylık Analiz**: 25
- **Premium Dönüşüm Oranı**: %15

## 🔄 **Hata Durumu Akışları**

### **1. Dosya Yükleme Hatası**
```
1. Kullanıcı desteklenmeyen dosya yükler
2. Sistem hata mesajı gösterir
3. Desteklenen formatlar listelenir
4. Kullanıcı doğru format seçer
5. Yükleme tekrar denenir
```

### **2. AI Servis Hatası**
```
1. AI servisi yanıt vermez
2. Sistem otomatik olarak yedek modele geçer
3. Kullanıcıya bilgi verilir
4. İşlem devam eder
5. Hata loglanır
```

### **3. Ağ Bağlantı Hatası**
```
1. İnternet bağlantısı kesilir
2. Mobil uygulama offline moda geçer
3. Yerel cache'den veriler gösterilir
4. Bağlantı geri geldiğinde senkronizasyon yapılır
5. Kullanıcıya bilgi verilir
```

## 🎯 **Gelecek Geliştirmeler**

### **Kısa Vadeli (3-6 ay)**
- **Ses ile Sohbet**: AI ile sesli konuşma
- **Gelişmiş Görselleştirmeler**: 3D grafikler, interaktif dashboardlar
- **Takım Çalışması**: Çoklu kullanıcı desteği
- **API Marketplace**: Üçüncü parti entegrasyonlar

### **Orta Vadeli (6-12 ay)**
- **Özel Model Eğitimi**: Kullanıcı verilerine özel AI modelleri
- **Gerçek Zamanlı İşbirliği**: Canlı doküman düzenleme
- **Gelişmiş RAG**: Çoklu dil desteği
- **Mobil Gelişmiş Özellikler**: AR/VR entegrasyonu

### **Uzun Vadeli (1+ yıl)**
- **AI Agent Marketplace**: Özel AI ajanları
- **Endüstri Çözümleri**: Sağlık, finans, pazarlama odaklı
- **Kuantum Hesaplama**: Kuantum AI entegrasyonu
- **Global Ölçek**: Çoklu dil ve bölge desteği

---

