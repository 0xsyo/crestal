# Crestal Network Bot Automation Script
This script automates interactions with the Crestal platform, including session initiation, authentication, quest completion, and referral code claiming. It is designed to be user-friendly and compatible with all major operating systems (Linux, macOS, and Windows).

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- **Automated Session Management**: Initiates and manages sessions with exponential backoff for retries.
- **Secure Authentication**: Uses Ethereum wallets for secure authentication.
- **Quest Automation**: Automatically retrieves and completes quests.
- **Referral Code Claiming**: Automatically claims referral codes.
- **User-Friendly Logging**: Colorful and informative logging for a user-friendly experience.

## Requirements

- Python 3.10 or higher
- Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/0xsya/crestal.git
   cd crestal
   ```

2. **Create a virtual environment**:
   - **Windows**:
     ```sh
     python -m venv venv
     ```
   - **Linux/macOS**:
     ```sh
     python3 -m venv venv
     ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```sh
     venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```sh
     source venv/bin/activate
     ```

4. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Create and populate the necessary files**:
   - `privatekeys.txt`: List of private keys, one per line.
   - `ua.txt`: JSON file containing User-Agent strings.
   - `session_data.json`: JSON file to store session data.
   - `code.txt`: List of referral codes, one per line.

## Usage

1. **Run the script**:
   - **Windows**:
   ```sh
   python main.py
   ```
   - **Linux/macOS**:   
   ```sh
   python3 main.py
   ``` 

3. **Follow the on-screen instructions**.

## License

This project is licensed under the MIT License.

## Disclaimer

This script is intended for educational purposes only. The use of this script is at your own risk. The authors are not responsible for any misuse or damage caused by this script. By using this script, you agree to comply with all applicable laws and regulations.

---

# Script Otomatisasi Crestal

## Daftar Isi
- [Pengenalan](#pengenalan)
- [Fitur](#fitur)
- [Kebutuhan](#kebutuhan)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Penggunaan](#penggunaan)
- [Lisensi](#lisensi)
- [Penafian](#penafian)

## Pengenalan

Script ini mengotomatisasi interaksi dengan platform Crestal, termasuk inisiasi sesi, autentikasi, penyelesaian quest, dan klaim kode referral. Script ini dirancang agar mudah digunakan dan kompatibel dengan semua sistem operasi utama (Linux, macOS, dan Windows).

## Fitur

- **Manajemen Sesi Otomatis**: Menginisiasi dan mengelola sesi dengan backoff eksponensial untuk percobaan ulang.
- **Autentikasi Aman**: Menggunakan dompet Ethereum untuk autentikasi yang aman.
- **Otomatisasi Quest**: Secara otomatis mengambil dan menyelesaikan quest.
- **Klaim Kode Referral**: Secara otomatis mengklaim kode referral.
- **Logging Ramah Pengguna**: Logging berwarna dan informatif untuk pengalaman pengguna yang ramah.

## Kebutuhan

- Python 3.10 atau lebih tinggi
- Paket Python yang diperlukan (tercantum di `requirements.txt`)

## Instalasi

1. **Clone repositori**:
   ```sh
   git clone https://github.com/0xsya/crestal.git
   cd crestal
   ```

2. **Buat virtual environment**:
   - **Windows**:
     ```sh
     python -m venv venv
     ```
   - **Linux/macOS**:
     ```sh
     python3 -m venv venv
     ```

3. **Aktifkan virtual environment**:
   - **Windows**:
     ```sh
     venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```sh
     source venv/bin/activate
     ```

4. **Install paket yang diperlukan**:
   ```sh
   pip install -r requirements.txt
   ```

## Konfigurasi

1. **Buat dan isi file yang diperlukan**:
   - `privatekeys.txt`: Daftar private key, satu per baris.
   - `ua.txt`: File JSON berisi string User-Agent.
   - `session_data.json`: File JSON untuk menyimpan data sesi.
   - `code.txt`: Daftar kode referral, satu per baris.

## Penggunaan

1. **Run the script**:
   - **Windows**:
   ```sh
   python main.py
   ```
   - **Linux/macOS**:   
   ```sh
   python3 main.py
   ```  

2. **Ikuti instruksi di layar**.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.

## Penafian

Script ini ditujukan hanya untuk tujuan pendidikan. Penggunaan script ini adalah risiko Anda sendiri. Penulis tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh script ini. Dengan menggunakan script ini, Anda setuju untuk mematuhi semua hukum dan peraturan yang berlaku.
