import requests
import time
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

arduino_ip = '172.20.10.14'  # Arduino'nuzun IP adresini girin
arduino_port = 80  # Arduino web sunucusunun dinlediği port

values = []

def fetch_sensor_data():
    try:
        # Arduino web sunucusuna HTTP GET isteği gönder
        response = requests.get(f'http://{arduino_ip}:{arduino_port}/data')
        
        # İstek başarılı olduysa (durum kodu 200)
        if response.status_code == 200:
            # Sensör verilerini içeren yanıtı al
            sensor_data = response.text.strip()  # Verilerin düz metin olarak gönderildiğini varsayıyoruz
            
            # Tüm değer verilerini düzenli ifadelerle çıkar
            value_matches = re.findall(r'Value: (\d+)', sensor_data)
            value_data = [int(value) for value in value_matches]
            
            # En son değeri voltaj (0-3.3V) olarak dönüştür
            for value in value_data:
                voltage = (10*value / 4095) * 3.3
                values.append(voltage)
                
                # Maksimum 1000 veri noktası sakla
                if len(values) > 1000:
                    values.pop(0)
            
            # En son değeri yazdır
            print("Sensor Data (V):", voltage)
        else:
            print("Failed to fetch sensor data:", response.status_code)
    except Exception as e:
        print("Error:", e)

def init_plot():
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 3.3)
    return line,

def update(frame):
    fetch_sensor_data()
    line.set_data(range(len(values)), values)
    return line,

def main():
    global ax, line
    
    time.sleep(1)  # Başlangıçta stabilizasyon için bekle
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('Sensor Values Over Time')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Voltage (V)')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    line, = ax.plot([], [], color='b', linewidth=1.0, alpha=0.7)
    
    # Animasyonu oluştur
    ani = FuncAnimation(fig, update, init_func=init_plot, blit=True, interval=1)  # Her 1 milisaniyede güncelle
    
    plt.show()

if __name__ == "__main__":
    main()
