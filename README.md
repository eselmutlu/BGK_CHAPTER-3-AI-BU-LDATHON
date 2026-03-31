# 💊 Gümüş Asistan — Akıllı İlaç & Yan Etki Yönetimi

> Yaşlı bireylerin ilaç karmaşasını çözen, AI destekli kişisel sağlık asistanı.

🔗 **Canlı Demo:** [Uygulamayı Aç](https://bgkchapter-3-ai-bu-ldathon-ezawsed2kp5wmeylmrapa4.streamlit.app/)

---

## 📖 Projenin Hikayesi

Her ziyarette büyükannemin/büyükbabamın yanında onlarca ilaç kutusu görürdüm. Sabah bu hap, öğle o şurup, akşam başka bir tablet... Ama hiçbir zaman tam olarak hangisinin ne işe yaradığını, birbirleriyle nasıl etkileşime girdiğini ya da ıspanak yemenin kan sulandırıcıyla tehlikeli bir kombinasyon oluşturabileceğini bilmiyorlardı.

Bu karmaşa sadece bizim ailemizin sorunu değil. Türkiye'de milyonlarca yaşlı birey aynı durumda. Prospektüsler teknik dille yazılmış, doktor randevuları kısa, eczacıya her şeyi sormak mümkün değil.

**Gümüş Asistan** işte bu boşluğu doldurmak için doğdu. Bir hafta boyunca sıfırdan kodlamayı öğrenerek, yapay zekanın gücüyle büyükannem/büyükbabam gibi milyonlarca insanın hayatını kolaylaştırabilecek bir araç geliştirdim.
🌟 Portfolyo Metni
Gümüş Asistan, yaşlı bireylerin ilaç yönetimini kolaylaştırmak için geliştirdiğim yapay zeka destekli bir sağlık asistanıdır. Büyükannem her gün onlarca ilaç kullanıyor; hangisinin ne işe yaradığını, hangi yiyeceklerle tehlikeli kombinasyon oluşturduğunu bilmiyordu. Bu sorunu çözmek için harekete geçtim.
Uygulama; ilaç kutusu fotoğrafını tanıyabiliyor, gıda-ilaç etkileşimlerini analiz ediyor, semptomlara göre uyarı veriyor. Yapay zeka sayesinde önceki sorguları hatırlıyor ve kişiselleştirilmiş yanıtlar üretiyor. İlaç hatırlatıcı, PDF rapor ve otomatik haftalık e-posta özellikleriyle tam anlamıyla akıllı bir asistan haline geldi.
Sıfır kodlama bilgisiyle başladığım bu yolculukta Python, Streamlit, OpenRouter API ve n8n gibi araçları öğrendim. Bir hafta içinde çalışan, yayında olan ve gerçek bir sorunu çözen bir uygulama geliştirdim. Teknolojiyi insan hayatına dokunacak şekilde kullanmak mümkün — Gümüş Asistan bunun kanıtı.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f531aec8-1058-49af-9e78-53d2635c3961" width="800" alt="Uygulama Ana Ekranı">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cbc05a0a-6a2a-4854-b8ca-4e85b5458b14" width="350" alt="Uygulama Detay Görünümü">
</p>




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
