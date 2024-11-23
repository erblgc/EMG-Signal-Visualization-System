# EMG Signal Visualization System

---

## Project Overview

This project processes **Electromyography (EMG)** signals collected from the arm, sends the processed data to an **ESP32 microcontroller**, and visualizes the live data on a **Python-based graphical user interface (GUI)**. The ESP32 is configured as a **web server**, transmitting data over WiFi, eliminating the need for a direct connection to the PC.

---

## System Components

### Hardware:
- **EMG sensor**: Captures muscle signals.
- **Signal conditioning circuit**: Processes EMG signals (e.g., filtering, amplification).
- **ESP32 microcontroller**: Handles ADC (Analog-to-Digital Conversion) and data transmission.
- **WiFi network**: Facilitates communication between ESP32 and the PC.

### Software:
- **Arduino Code (`emg.ino`)**: Configures the ESP32 to:
  - Read analog signals from the EMG sensor.
  - Process the data.
  - Send it to a web server over WiFi.
- **Python Code (`UI.py`)**: 
  - Fetches data from the ESP32 web server.
  - Visualizes the data as a live graph using Matplotlib.

---

## How It Works

### Signal Processing:
1. EMG signals are captured using an EMG sensor.
2. Signals are passed through a **conditioning circuit** for:
   - Filtering.
   - Amplification.
3. The conditioned signal is suitable for ADC input on the ESP32.

### ESP32 Functionality:
1. Reads the analog EMG signals via its ADC pin.
2. Converts the signals into readable data (e.g., voltages).
3. Hosts a **web server** to share the data over WiFi.

### Data Visualization:
1. The Python script (`UI.py`) sends **HTTP GET** requests to the ESP32 to fetch live data.
2. Fetched data is:
   - Processed.
   - Converted to voltages.
   - Plotted on a live-updating graph.

---

## Setup and Configuration

### Hardware Setup:
1. Connect the **EMG sensor** to the **signal conditioning circuit**.
2. Attach the circuit's output to an **ADC pin** on the ESP32 (e.g., GPIO34).
3. Ensure the ESP32 is powered and connected to a stable WiFi network.

### ESP32 Configuration:
1. Upload the Arduino code (`emg.ino`) to the ESP32.
2. Update the **WiFi SSID and password** in the Arduino code with your network credentials.
3. Note the ESP32's **IP address** displayed in the serial monitor after upload.

### Python Script:
1. Install the required Python libraries:
   ```bash
   pip install matplotlib requests
   ```
2. Update the following variables in `UI.py`:
   - `arduino_ip`: Set to the ESP32's IP address.
   - `arduino_port`: Set to the ESP32's port number.
3. Run the script to start the live visualization:
   ```bash
   python UI.py
   ```

---

## Usage Instructions

1. Power on the **EMG sensor** and **ESP32**.
2. Ensure the ESP32 is connected to the WiFi network.
3. Run the **Python script** on your PC:
   ```bash
   python UI.py
   ```
4. Observe the real-time EMG signal visualization on the live graph.

---

## Key Features

- **Wireless Communication**: Utilizes WiFi for seamless data transmission from the ESP32 to the PC.
- **Live Visualization**: Displays real-time EMG signals as a graph with adjustable voltage scaling.
- **Scalable**: Easily supports additional sensors with minimal adjustments.

---

## Potential Enhancements

1. **Signal Smoothing**:
   - Add advanced processing or filtering in the Python script for smoother visualizations.
2. **Multi-Channel Visualization**:
   - Implement support for multiple EMG sensors in the Python script.
3. **Extended Web Server Functionality**:
   - Add configurable options (e.g., sampling rate) to the ESP32's web server.

---

This project demonstrates a practical approach to capturing, transmitting, and visualizing EMG signals, providing a scalable platform for real-time signal analysis.
