# Araç Kiralama Sistemi

Modern ve kullanıcı dostu bir araç kiralama yönetim uygulaması. Python ve Tkinter ile geliştirilmiştir.

## Özellikler

- **Kullanıcı Yetkilendirme** - Giriş/Kayıt sistemi (Admin & User rolleri)
- **Araç Yönetimi** - Araç ekleme, düzenleme ve silme
- **Kiralama İşlemleri** - Kiralama başlatma ve iade alma
- **Anlık İstatistikler** - Toplam, müsait, kirada araç sayısı ve gelir
- **Kiralama Geçmişi** - Tüm kiralama kayıtlarını görüntüleme
- **Durum Filtreleme** - Müsait, kirada, bakımda filtreleri
- **SQLite Veritabanı** - Kalıcı veri saklama
- **Modern Arayüz** - Koyu tema, responsive tasarım

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/bilalyazicioglu/Car-Rental-py.git
cd Car-Rental-py
```

2. Python 3.10 veya üzeri yüklü olduğundan emin olun:
```bash
python3 --version
```

3. Uygulamayı çalıştırın:
```bash
python3 main.py
```

> **Not:** Bu proje sadece Python standart kütüphanelerini kullanır. Ekstra kurulum gerekmez!

## Varsayılan Giriş

| Kullanıcı | Şifre | Rol |
|-----------|-------|-----|
| admin | admin | Admin |

> Yeni kullanıcılar "Kayıt Ol" ile oluşturulabilir (User rolü ile).

## Kullanım

### Araç Eklemek (Sadece Admin)
1. Sol paneldeki form alanlarını doldurun (Plaka, Marka, Model, Ücret)
2. "➕ EKLE" butonuna tıklayın

### Kiralama Başlatmak
1. Listeden müsait bir araç seçin
2. "KIRALA" butonuna tıklayın
3. Müşteri adı ve tarihleri girin

### Araç İade Almak
1. Kirada olan aracı seçin
2. "İADE" butonuna tıklayın

### Kiralama Geçmişi
1. Sağ üstteki "Geçmiş" butonuna tıklayın
2. Tüm kiralama kayıtlarını görüntüleyin

## Proje Yapısı

```
Car-Rental-py/
├── main.py             # Ana giriş noktası
├── gui.py              # Tkinter arayüzü (Ana uygulama, Dialoglar)
├── auth_gui.py         # Giriş/Kayıt penceresi
├── rental_service.py   # İş mantığı ve validasyonlar
├── data_manager.py     # SQLite veri yönetimi
├── car_rental.db       # Veritabanı dosyası
├── requirements.txt    # Bağımlılıklar
├── LICENSE             # MIT Lisansı
└── README.md
```

## Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| **Python 3.10+** | Programlama dili |
| **Tkinter** | GUI framework |
| **SQLite3** | Veritabanı |

## Kullanıcı Rolleri

| Rol | Yetkiler |
|-----|----------|
| **Admin** | Araç ekleme, düzenleme, silme, kiralama, iade, geçmiş görüntüleme |
| **User** | Kiralama, iade, geçmiş görüntüleme |

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## Geliştiriciler

**Bilal Yazıcıoğlu** - [@bilalyazicioglu](https://github.com/bilalyazicioglu)

**Ali Talha Yurtseven** - [@alitalhq](https://github.com/alitalhq)

---