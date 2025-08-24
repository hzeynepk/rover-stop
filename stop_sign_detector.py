import cv2
import numpy as np
import os
import glob

class StopSignDetector:
    def __init__(self):
        # Kırmızı renk için HSV aralıkları
        # İki farklı kırmızı aralığı (0-10 ve 170-180)
        self.lower_red1 = np.array([0, 50, 50])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 50, 50])
        self.upper_red2 = np.array([180, 255, 255])
        
    def detect_red_regions(self, image):
        """Görüntüde kırmızı bölgeleri tespit eder"""
        # BGR'den HSV'ye dönüştür
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # İki kırmızı aralığı için maske oluştur
        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        
        # İki maskeyi birleştir
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # Gürültüyü azaltmak için morfolojik işlemler
        kernel = np.ones((5,5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        
        return red_mask
    
    def find_stop_signs(self, image):
        """STOP trafik işaretlerini tespit eder"""
        # Kırmızı bölgeleri tespit et
        red_mask = self.detect_red_regions(image)
        
        # Konturları bul
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        stop_signs = []
        
        for contour in contours:
            # Kontur alanını hesapla
            area = cv2.contourArea(contour)
            
            # Çok küçük alanları filtrele
            if area < 500:
                continue
                
            # Bounding rectangle hesapla
            x, y, w, h = cv2.boundingRect(contour)
            
            # En boy oranını kontrol et (STOP işareti genellikle kare/sekizgen)
            aspect_ratio = w / h
            if 0.7 <= aspect_ratio <= 1.3:  # Yaklaşık kare şekli
                # Merkez noktasını hesapla
                center_x = x + w // 2
                center_y = y + h // 2
                
                stop_signs.append({
                    'bbox': (x, y, w, h),
                    'center': (center_x, center_y),
                    'area': area
                })
        
        return stop_signs
    
    def draw_detections(self, image, stop_signs):
        """Tespit edilen STOP işaretlerini görüntü üzerinde gösterir"""
        result_image = image.copy()
        
        for sign in stop_signs:
            x, y, w, h = sign['bbox']
            center_x, center_y = sign['center']
            
            # Kırmızı kare çiz
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 3)
            
            # Merkez noktasını işaretle
            cv2.circle(result_image, (center_x, center_y), 5, (0, 255, 0), -1)
            
            # Koordinatları yazdır
            cv2.putText(result_image, f'Center: ({center_x}, {center_y})', 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            print(f"STOP işareti tespit edildi! Merkez koordinatları: ({center_x}, {center_y})")
        
        return result_image
    
    def process_image(self, image_path):
        """Tek bir görüntüyü işler"""
        # Görüntüyü yükle
        image = cv2.imread(image_path)
        if image is None:
            print(f"Görüntü yüklenemedi: {image_path}")
            return None
            
        print(f"\nİşleniyor: {os.path.basename(image_path)}")
        
        # STOP işaretlerini tespit et
        stop_signs = self.find_stop_signs(image)
        
        if stop_signs:
            print(f"{len(stop_signs)} adet STOP işareti tespit edildi.")
            # Tespit edilen işaretleri çiz
            result_image = self.draw_detections(image, stop_signs)
            return result_image
        else:
            print("STOP işareti tespit edilemedi.")
            return image
    
    def process_all_images(self, img_folder):
        """img klasöründeki tüm görüntüleri işler"""
        # Desteklenen görüntü formatları
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        image_files = []
        
        for extension in image_extensions:
            image_files.extend(glob.glob(os.path.join(img_folder, extension)))
            image_files.extend(glob.glob(os.path.join(img_folder, extension.upper())))
        
        if not image_files:
            print(f"'{img_folder}' klasöründe görüntü dosyası bulunamadı.")
            return
        
        print(f"{len(image_files)} adet görüntü dosyası bulundu.")
        
        # Sonuçlar için klasör oluştur
        results_folder = os.path.join(os.path.dirname(img_folder), 'results')
        os.makedirs(results_folder, exist_ok=True)
        
        for image_path in image_files:
            result_image = self.process_image(image_path)
            
            if result_image is not None:
                # Sonucu kaydet
                filename = os.path.basename(image_path)
                result_path = os.path.join(results_folder, f'result_{filename}')
                cv2.imwrite(result_path, result_image)
                print(f"Sonuç kaydedildi: {result_path}")

def main():
    # STOP işareti tespit edici oluştur
    detector = StopSignDetector()
    
    # img klasörünü işle
    img_folder = 'img'
    if os.path.exists(img_folder):
        detector.process_all_images(img_folder)
    else:
        print(f"'{img_folder}' klasörü bulunamadı.")
        print("Lütfen 'img' klasörünün mevcut olduğundan emin olun.")

if __name__ == "__main__":
    main()