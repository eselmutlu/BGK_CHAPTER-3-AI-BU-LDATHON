# Gümüş Asistan

Gümüş Asistan, yaşlı bireyler ve kronik hastalar için geliştirilen yapay zeka destekli bir sağlık yardımcı uygulamasıdır.  
Streamlit tabanlı arayüz ile ilaç tanıma, gıda-ilaç etkileşim analizi, semptom değerlendirmesi ve ilaç hatırlatıcı yönetimi sağlar.

## Kurulum

1. Proje klasörüne geçin.
2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
streamlit run app.py
```

## Özellikler

- Kullanıcı adı/şifre ile giriş sistemi (SQLite üzerinde saklama)
- Fotoğraf ile ilaç tanıma (AI destekli analiz)
- Gıda-ilaç etkileşim kontrolü ve risk seviyesi (yeşil/sarı/kırmızı)
- Semptom analizi (kesin teşhis vermeyen yönlendirici çıktı)
- Sonuçları düzenli kartlarda görüntüleme
- PDF rapor indirme (tarih, ilaç bilgisi, analiz çıktısı)
- İlaç hatırlatıcı ekleme, listeleme ve silme
- Tarayıcı bildirimi ile hatırlatma (izin gerekli)

## Ekran Görüntüsü

Bu bölüme uygulama ekran görüntülerini ekleyebilirsiniz:

- Giriş ekranı
- Ana analiz ekranı
- Hatırlatıcı paneli
- PDF rapor çıktısı örneği

> Örnek kullanım:
> `screenshots/login.png`, `screenshots/dashboard.png`
