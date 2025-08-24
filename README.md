# STOP Trafik İşareti Tespit Sistemi

Bu proje, OpenCV kullanarak görüntülerde STOP trafik işaretlerini tespit eden bir Python uygulamasıdır. Sistem, renk tespiti (kırmızı renk) kullanarak STOP işaretlerini tanır ve konumlarını belirler.

## Özellikler

- **Renk Tabanlı Tespit**: Kırmızı renk tespiti ile STOP işaretlerini bulur
- **Konum Belirleme**: Tespit edilen işaretin merkez koordinatlarını hesaplar
- **Görsel Çıktı**: Tespit edilen işaretleri kare içerisine alarak vurgular
- **Toplu İşleme**: img klasöründeki tüm görüntüleri otomatik olarak işler
- **Sonuç Kaydetme**: İşlenmiş görüntüleri results klasörüne kaydeder

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Test edilecek görüntüleri `img/` klasörüne yerleştirin
2. Programı çalıştırın:
```bash
python stop_sign_detector.py
```

## Çıktılar

- **Terminal**: Tespit edilen her STOP işareti için merkez koordinatları yazdırılır
- **Görsel**: İşlenmiş görüntüler `results/` klasörüne kaydedilir
- **Tespit Gösterimi**: STOP işaretleri kırmızı kare ile çevrelenir ve merkez noktası yeşil nokta ile işaretlenir

## Algoritma Detayları

### Renk Tespiti
- HSV renk uzayında kırmızı renk aralıkları kullanılır
- İki farklı kırmızı aralığı (0-10° ve 170-180°) birleştirilir
- Morfolojik işlemlerle gürültü azaltılır

### Şekil Analizi
- Kontur analizi ile şekiller tespit edilir
- En boy oranı kontrolü (0.7-1.3 arası) ile kare/sekizgen şekiller filtrelenir
- Minimum alan kontrolü ile küçük nesneler elenir

### Konum Hesaplama
- Bounding rectangle kullanılarak merkez koordinatları hesaplanır
- Koordinatlar hem terminale yazdırılır hem de görüntü üzerine eklenir

## Dosya Yapısı

```
rover-stop/
├── stop_sign_detector.py  # Ana program
├── requirements.txt       # Python gereksinimleri
├── README.md             # Bu dosya
├── img/                  # Test görüntüleri
│   ├── photo-1518749031467-bb37f48aee10.jpg
│   ├── photo-1558626219-fa0c107b5613.jpg
│   ├── photo-1635481585588-2440d43b6747.jpg
│   ├── photo-1727156275339-aad186798856.jpg
│   └── premium_photo-1731192705955-f10a8e7174d2.jpg
└── results/              # İşlenmiş görüntüler (otomatik oluşturulur)
```

## Teknik Detaylar

- **OpenCV**: Görüntü işleme ve bilgisayarlı görü işlemleri
- **NumPy**: Sayısal hesaplamalar ve dizi işlemleri
- **HSV Renk Uzayı**: Renk tespiti için daha kararlı sonuçlar
- **Morfolojik İşlemler**: Gürültü azaltma ve şekil iyileştirme

## Geliştirme Notları

Bu sistem, otonom robotlar için STOP işareti tespiti amacıyla geliştirilmiştir. Tespit edilen işaret koordinatları, robotun navigasyon sistemine entegre edilebilir.