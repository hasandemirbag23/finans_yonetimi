# Kişisel Finans Yönetimi Uygulaması

Bu uygulama, kullanıcıların gelir ve giderlerini takip etmelerine, bütçe oluşturmalarına ve finansal durumlarını görselleştirmelerine olanak tanıyan bir web tabanlı finans yönetim aracıdır.

## Özellikler

- Kullanıcı kaydı ve kimlik doğrulama sistemi
- Gelir ve gider takibi
- Kategori bazlı harcama sınıflandırma
- Bütçe oluşturma ve takip etme
- Gelir/gider raporları ve görselleştirmeler
- CSV formatında veri dışa/içe aktarma

## Teknolojiler

- **Backend**: Python Flask framework
- **Veritabanı**: SQLite
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Bootstrap 5
- **Grafikler**: Chart.js

## Kurulum

1. Gerekli bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```
   python run.py
   ```

3. Web tarayıcınızda şu adrese gidin:
   ```
   http://localhost:5000
   ```

## Kullanım

1. Kayıt olun veya varsayılan admin hesabı ile giriş yapın:
   - Kullanıcı adı: admin
   - Şifre: password

2. Dashboard üzerinden gelir ve giderlerinizi ekleyin.

3. Bütçe oluşturun ve harcamalarınızı takip edin.

4. Raporlar bölümünden finansal durumunuzun detaylı analizini görüntüleyin.

## Proje Yapısı

```
finance_app/
├── models/            # Veritabanı modelleri
├── static/            # Statik dosyalar (CSS, JS, resimler)
├── templates/         # HTML şablonları
├── __init__.py        # Uygulama konfigürasyonu
├── forms.py           # Form sınıfları
├── routes.py          # Uygulama rotaları
├── requirements.txt   # Bağımlılıklar
├── run.py             # Uygulama başlatma script'i
└── README.md          # Bu dosya
```

## Ekran Görüntüleri

*Uygulama çalıştırıldıktan sonra ekran görüntüleri buraya eklenecek.*

## Katkıda Bulunma

1. Bu repo'yu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## İletişim

- Proje Linki: [https://github.com/yourusername/finance_app](https://github.com/yourusername/finance_app) 