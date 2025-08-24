import cv2
import numpy as np
import os
from stop_sign_detector import StopSignDetector

def demo_single_image():
    """Tek bir görüntü üzerinde demo yapar"""
    detector = StopSignDetector()
    
    # img klasöründeki dosyaları listele
    img_folder = 'img'
    if not os.path.exists(img_folder):
        print(f"'{img_folder}' klasörü bulunamadı.")
        return
    
    image_files = [f for f in os.listdir(img_folder) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    if not image_files:
        print("Görüntü dosyası bulunamadı.")
        return
    
    print("Mevcut görüntüler:")
    for i, filename in enumerate(image_files, 1):
        print(f"{i}. {filename}")
    
    try:
        choice = int(input("\nHangi görüntüyü test etmek istiyorsunuz? (numara girin): ")) - 1
        if 0 <= choice < len(image_files):
            selected_file = image_files[choice]
            image_path = os.path.join(img_folder, selected_file)
            
            print(f"\nSeçilen görüntü: {selected_file}")
            result_image = detector.process_image(image_path)
            
            if result_image is not None:
                # Sonucu göster
                cv2.imshow('STOP İşareti Tespiti', result_image)
                print("\nGörüntüyü kapatmak için herhangi bir tuşa basın...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                # Sonucu kaydet
                result_path = f'demo_result_{selected_file}'
                cv2.imwrite(result_path, result_image)
                print(f"Sonuç kaydedildi: {result_path}")
        else:
            print("Geçersiz seçim!")
    except ValueError:
        print("Lütfen geçerli bir numara girin!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def demo_webcam():
    """Webcam ile canlı tespit yapar"""
    detector = StopSignDetector()
    
    # Webcam'i başlat
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Webcam açılamadı!")
        return
    
    print("Webcam başlatıldı. Çıkmak için 'q' tuşuna basın.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # STOP işaretlerini tespit et
        stop_signs = detector.find_stop_signs(frame)
        
        if stop_signs:
            # Tespit edilen işaretleri çiz
            frame = detector.draw_detections(frame, stop_signs)
        
        # Görüntüyü göster
        cv2.imshow('Canlı STOP İşareti Tespiti', frame)
        
        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam kapatıldı.")

def show_detection_parameters():
    """Tespit parametrelerini gösterir"""
    detector = StopSignDetector()
    
    print("\n=== STOP İşareti Tespit Parametreleri ===")
    print(f"Kırmızı Renk Aralığı 1 (HSV): {detector.lower_red1} - {detector.upper_red1}")
    print(f"Kırmızı Renk Aralığı 2 (HSV): {detector.lower_red2} - {detector.upper_red2}")
    print("Minimum Alan: 500 piksel")
    print("En-Boy Oranı: 0.7 - 1.3 (kare/sekizgen şekiller)")
    print("Morfolojik İşlem: 5x5 kernel ile açma/kapama")

def main():
    print("=== STOP Trafik İşareti Tespit Sistemi Demo ===")
    print("1. Tek görüntü testi")
    print("2. Tüm görüntüleri işle")
    print("3. Webcam ile canlı tespit")
    print("4. Tespit parametrelerini göster")
    print("5. Çıkış")
    
    while True:
        try:
            choice = input("\nSeçiminizi yapın (1-5): ")
            
            if choice == '1':
                demo_single_image()
            elif choice == '2':
                detector = StopSignDetector()
                detector.process_all_images('img')
            elif choice == '3':
                demo_webcam()
            elif choice == '4':
                show_detection_parameters()
            elif choice == '5':
                print("Çıkılıyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 1-5 arası bir numara girin.")
                
        except KeyboardInterrupt:
            print("\nProgram sonlandırıldı.")
            break
        except Exception as e:
            print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()