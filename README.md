# 💊 Gümüş Asistan — Akıllı İlaç & Yan Etki Yönetimi

> Yaşlı bireylerin ilaç karmaşasını çözen, AI destekli kişisel sağlık asistanı.

🔗 **Canlı Demo:** [Uygulamayı Aç](https://bgkchapter-3-ai-bu-ldathon-ezawsed2kp5wmeylmrapa4.streamlit.app/)

---

## 🎯 Problem

Polifarmasi — yani birden fazla ilaç kullanımı — yaşlı bireyler için ciddi bir risk oluşturuyor:

- İlaçların birbirleriyle olan **gizli etkileşimleri** bilinmiyor
- Günlük gıdaların (greyfurt, süt, ıspanak) ilaçlarla **tehlikeli kombinasyonlar** oluşturabileceği fark edilmiyor
- Prospektüsler **teknik dil** nedeniyle anlaşılamıyor

## 💡 Çözüm

Gümüş Asistan, yapay zeka kullanarak bu sorunları basit ve anlaşılır bir arayüzle çözüyor.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 📸 İlaç Tanıma | İlaç kutusu fotoğrafı yükle, AI tanımlasın |
| 🥗 Gıda-İlaç Etkileşimi | Hangi yiyeceklerin ilaçlarla tehlikeli olduğunu öğren |
| 🩺 Semptom Takibi | Semptomların ilaçlarla ilişkisini analiz et |
| 🧠 Konuşma Belleği | AI önceki sorgularını hatırlıyor |
| ⏰ İlaç Hatırlatıcı | İlaç saatlerini kaydet, unutma |
| 📄 PDF Rapor | Analiz sonuçlarını PDF olarak indir |
| 🔐 Kullanıcı Girişi | Kişisel verilerin güvende |
| 📧 Haftalık Rapor | n8n ile otomatik e-posta otomasyonu |

---

## 🚀 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/eselmutlu/BGK_CHAPTER-3-AI-BU-LDATHON.git

# Klasöre gir
cd BGK_CHAPTER-3-AI-BU-LDATHON

# Paketleri yükle
pip install -r requirements.txt

# .env dosyası oluştur
cp .env.example .env
# .env dosyasına OPENROUTER_API_KEY ekle

# Uygulamayı başlat
streamlit run app.py
```

---

## 🛠️ Teknolojiler

- **Python** — Backend
- **Streamlit** — Arayüz
- **OpenRouter API** — AI modeli
- **SQLite** — Veritabanı
- **n8n** — Otomasyon
- **Streamlit Cloud** — Yayın

---

## 👩‍💻 Geliştirici

**Esel Mutlu** — BGK Chapter 3 AI Buildathon

---

*Bu uygulama tıbbi tavsiye vermez. Sağlık kararları için mutlaka bir doktora danışın.*
