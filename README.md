# 🚗 Araç Kiralama Sistemi

Basit ve kullanışlı bir araç kiralama yönetim uygulaması. Python ve Tkinter ile geliştirilmiştir.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Özellikler

- 📋 Araç ekleme, düzenleme ve silme
- 🔑 Kiralama işlemleri (başlatma/iade)
- 📊 Anlık istatistikler (müsait, kirada, bakımda)
- 💾 JSON tabanlı veri saklama
- 🎨 Modern ve kullanıcı dostu arayüz
- 🔍 Durum bazlı filtreleme

## 📦 Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/bilalyazicioglu/Car-Rental-py.git
cd Car-Rental-py
```

2. Python 3.8 veya üzeri yüklü olduğundan emin olun:
```bash
python --version
```

3. Uygulamayı çalıştırın:
```bash
python main.py
```

> **Not:** Bu proje sadece Python standart kütüphanelerini kullanır. Ekstra kurulum gerekmez!

## 🚀 Kullanım

### Araç Eklemek
1. Sol paneldeki form alanlarını doldurun
2. "➕ Araç Ekle" butonuna tıklayın

### Kiralama Başlatmak
1. Listeden müsait bir araç seçin
2. "🔑 Kiralama Başlat" butonuna tıklayın
3. Müşteri adı ve tarihleri girin

### Araç İade Almak
1. Kirada olan aracı seçin
2. "↩️ Aracı İade Et" butonuna tıklayın

## 📁 Proje Yapısı

```
Car-Rental-py/
├── main.py           # Ana giriş noktası
├── gui.py            # Tkinter arayüzü
├── rental_service.py # İş mantığı
├── data_manager.py   # Veri yönetimi
├── vehicles.json     # Araç verileri
└── README.md
```

## 🛠️ Teknolojiler

- **Python 3** - Programlama dili
- **Tkinter** - GUI framework
- **JSON** - Veri depolama

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 👤 Geliştirici

**Bilal Yazıcıoğlu**

- GitHub: [@bilalyazicioglu](https://github.com/bilalyazicioglu)

---

⭐ Beğendiyseniz yıldız vermeyi unutmayın!
