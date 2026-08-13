# TextPact

TextPact, çeviri hizmetleri için hazırladığım bir web uygulaması projesidir. Kullanıcılar yapay zekâ asistanına hizmetlerle ilgili soru sorabilir ve çeviri talebi oluşturabilir. Gönderilen talepler sistemde kaydedilir ve ayrı bir yönetim sayfasında görüntülenebilir.

## Proje İçindekiler

- Çeviri hizmetleri hakkında soruları yanıtlayan AI asistanı
- İsim, telefon, belge türü ve mesaj bilgilerinin girilebildiği talep formu
- Gönderilen taleplerin kaydedilmesi
- Taleplerin görüntülendiği Admin Dashboard

## Kullandığım Araçlar

Projede Python ve Flask ile arka plan sistemi, SQLite ile kayıt sistemi, Groq ile AI asistanı ve Wix ile web sitesi hazırlandı. Site ile arka plan sistemi Wix Velo kullanılarak birbirine bağlandı. Proje Render üzerinden internete açıldı.

## Projeyi Çalıştırma

Projeyi başka bir bilgisayarda çalıştırmak için önce `requirements.txt` dosyasında belirtilen gerekli Python paketlerinin kurulması gerekir.

Daha sonra API anahtarı gibi gizli bilgiler `.env` dosyasına eklenir ve proje:

`python run.py`

komutuyla başlatılır.

## Canlı Backend

https://textpact.onrender.com

## Wix Sitesi

https://ozge604150.wixsite.com/textpact-project

https://ozge604150.wixsite.com/textpact-project/admin-dashboard
