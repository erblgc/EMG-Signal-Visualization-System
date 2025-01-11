import requests
import time
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

arduino_ip = '172.20.10.14'  # Enter the IP address of your Arduino
arduino_port = 80  # Port where the Arduino web server is listening

values = []

def fetch_sensor_data():
    try:
        # Send an HTTP GET request to the Arduino web server
        response = requests.get(f'http://{arduino_ip}:{arduino_port}/data')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract sensor data from the response text
            sensor_data = response.text.strip()  # Assuming data is sent as plain text
            
            # Extract all value data using regex
            value_matches = re.findall(r'Value: (\d+)', sensor_data)
            value_data = [int(value) for value in value_matches]
            
            # Convert the most recent value to voltage (0-3.3V range)
            for value in value_data:
                voltage = (10*value / 4095) * 3.3
                values.append(voltage)
                
                # Keep only the last 1000 data points
                if len(values) > 1000:
                    values.pop(0)
            
            # Print the most recent voltage value
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
    
    time.sleep(1)  # Initial stabilization delay
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('Sensor Values Over Time')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Voltage (V)')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    line, = ax.plot([], [], color='b', linewidth=1.0, alpha=0.7)
    
    # Create the animation
    ani = FuncAnimation(fig, update, init_func=init_plot, blit=True, interval=1)  # Update every 1 millisecond
    
    plt.show()

if __name__ == "__main__":
    main()
