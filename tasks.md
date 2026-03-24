# Gümüş Asistan - Geliştirme Görev Listesi

Bu görev listesi `prd.md` temel alınarak hazırlanmıştır. Sıra, bağımlılıkları ve hızlı MVP çıkışını dikkate alır.

## 0) Proje Kurulumu ve Altyapı

- [x] Monorepo yapılandırmasını netleştir (`apps/web`, `apps/api`, `packages/shared`, `db`, `docs`).
- [x] `apps/web` için React + Tailwind başlangıç kurulumunu tamamla.
- [x] `apps/api` için Node.js + TypeScript API iskeletini tamamla.
- [x] Ortak `packages/shared` alanında temel tip ve şema yapısını kur.
- [x] Ortam değişkenleri şablonunu oluştur (`.env.example`): Gemini API anahtarı, veritabanı URL'i vb.
- [x] Temel hata yönetimi ve loglama yaklaşımını belirle.

## 1) Veri Modeli ve Veritabanı (PostgreSQL)

- [x] Temel tabloları tasarla: `users`, `medications`, `meal_logs`, `symptom_logs`, `interaction_checks`.
- [x] Yaşlı ve kronik hasta senaryolarına uygun ilaç kullanım alanlarını ekle (doz, sıklık, saat).
- [ ] Migration dosyalarını oluştur ve çalıştır.
- [x] Geliştirme için örnek seed verileri ekle.
- [x] Veri saklama/silme politikaları için gerekli alanları ekle (KVKK/GDPR uyumu).

## 2) Ortak Domain Tipleri ve Doğrulama

- [x] `packages/shared` içinde domain tiplerini detaylandır:
  - [x] İlaç modeli
  - [x] Gıda etkileşim kontrolü giriş/çıkış modeli
  - [x] Semptom kaydı modeli
  - [x] Risk seviyesi ve uyarı modeli
- [x] API istek/yanıt doğrulama şemalarını tanımla.
- [x] Tiplerin web ve API tarafında ortak kullanımını doğrula.

## 3) Özellik 1 - Fotoğraf ile İlaç Tanımlama

- [x] Web tarafında kamera veya fotoğraf yükleme bileşeni geliştir.
- [x] API tarafında görsel işleme endpoint'i oluştur.
- [ ] Gemini API ile ilaç adı/dozaj çıkarımı yapan servis katmanını yaz.
- [x] Sonuçları kullanıcıya okunabilir ve büyük fontlu şekilde göster.
- [x] Tanıma başarısız olduğunda kullanıcı dostu geri bildirim ver.

## 4) Özellik 2 - Gıda ve İlaç Etkileşimi Kontrolü

- [x] Kullanıcının yemek içeriği gireceği ekranı oluştur (metin/ses ile genişletilebilir yapı).
- [x] API'de ilaç listesi + gıda listesi alan endpoint'i yaz.
- [ ] Etkileşim kontrol servisini oluştur (Gemini destekli).
- [x] Çıktıda risk derecesi, kısa açıklama ve önerilen aksiyon göster.
- [x] Kritik riskte belirgin uyarı tasarımı ekle.

## 5) Özellik 3 - Semptom Takibi ve Olası İlaç Kaynağı

- [ ] Semptom metin/ses giriş arayüzünü oluştur.
- [ ] API'de semptom analizi endpoint'i geliştir.
- [ ] Semptom-ilaç ilişkisi için analiz akışını tasarla.
- [ ] Sonucu "olasılık" mantığı ile göster (kesin teşhis dili kullanma).
- [ ] Kayıtlı semptom geçmişi ekranını ekle.

## 6) Yasal Uyarılar ve Gizlilik (Zorunlu)

- [ ] Uygulamanın görünür alanında sabit uyarı metnini göster:
  - [ ] "Bu uygulama tıbbi tavsiye vermez."
- [ ] Açık rıza/onay metinlerini ilk kullanım akışına ekle.
- [ ] Veri işleme ve saklama koşullarını dokümante et (`docs/privacy-kvkk-gdpr.md`).
- [ ] Kullanıcı verisi silme talebi akışını planla.

## 7) Yaşlı Dostu UX/UI İyileştirmeleri

- [ ] Büyük yazı tipi, yüksek kontrast ve sade navigasyon uygula.
- [ ] Kritik işlem butonlarını belirginleştir.
- [ ] Hata mesajlarını sade ve yönlendirici yaz.
- [ ] Sesli geri bildirim/erişilebilirlik iyileştirmeleri için temel altyapı hazırla.

## 8) Test ve Kalite

- [ ] Ortak tipler ve servisler için birim testleri yaz.
- [ ] API endpoint'leri için entegrasyon testleri ekle.
- [ ] Ana kullanıcı akışları için uçtan uca test senaryoları tanımla.
- [ ] Riskli etkileşim senaryoları için test veri seti hazırla.
- [ ] Hatalı Gemini yanıtlarına karşı fallback davranışlarını test et.

## 9) Yayınlama Hazırlığı

- [ ] Ortamlara göre yapılandırma ayır (dev/stage/prod).
- [ ] Uygulama izleme ve hata takip altyapısını ekle.
- [ ] Veri yedekleme ve kurtarma adımlarını dokümante et.
- [ ] İlk pilot kullanıcı grubu için geri bildirim toplama planı oluştur.

## 10) MVP Sürüm Kapsamı (Öneri)

- [ ] Fotoğraf ile ilaç tanıma (temel doğrulukta)
- [ ] Gıda-ilaç etkileşim kontrolü (risk seviyeli çıktı)
- [ ] Semptom metin girişi ve olası kaynak analizi
- [ ] Zorunlu yasal uyarı ve temel gizlilik metinleri
- [ ] Yaşlı dostu temel arayüz

## İlk Sprint Önerisi (1-2 Hafta)

- [ ] Ortak tipleri ve veri modelini tamamla.
- [ ] Gıda-ilaç etkileşim endpoint'ini uçtan uca çalışır hale getir.
- [ ] Web'de etkileşim kontrol ekranını yayınla.
- [ ] Yasal uyarıyı tüm sayfalara ekle.
- [ ] Temel testleri ve örnek veriyi tamamla.
