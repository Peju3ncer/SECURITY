import os
import json
import requests
import time
import smtplib
from flask import Flask, request
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

# Inisialisasi Colorama
init()

# Konfigurasi Email
EMAIL_SENDER = "agusornanda@gmail.com"  # Ganti dengan email pengirim
EMAIL_PASSWORD = "lhon hqlb uifq ztvl"  # Masukkan App Password Gmail
EMAIL_RECEIVER = "agusornanda@gmail.com"  # Email penerima notifikasi

# Konfigurasi File Log
LOG_FILE = "attack_log.json"
BLOCKED_IPS = "blocked_ips.txt"

# Inisialisasi Flask
app = Flask(__name__)

# Animasi Loading
def loading_animation():
    print(Fore.CYAN + "\n[ SYSTEM STARTING ]")
    loading_text = "LOADING..."
    for _ in range(3):
        for char in loading_text:
            print(Fore.YELLOW + char, end="", flush=True)
            time.sleep(0.1)
        print("\r" + " " * len(loading_text), end="\r", flush=True)
    print(Fore.GREEN + "[ READY TO OPERATE ]\n" + Style.RESET_ALL)

# Header Keren
def show_banner():
    os.system("clear" if os.name == "posix" else "cls")
    banner = f"""{Fore.RED}
  >=>>=>   >=======>     >=>    >=>     >=> >======>     >=> >===>>=====>
>=>    >=> >=>        >=>   >=> >=>     >=> >=>    >=>   >=>      >=>    
 >=>       >=>       >=>        >=>     >=> >=>    >=>   >=>      >=>    
   >=>     >=====>   >=>        >=>     >=> >> >==>      >=>      >=>    
      >=>  >=>       >=>        >=>     >=> >=>  >=>     >=>      >=>    
>=>    >=> >=>        >=>   >=> >=>     >=> >=>    >=>   >=>      >=>    
  >=>>=>   >=======>    >===>     >====>    >=>      >=> >=>      >=>    
                                                                         
>=>      >=>                                                             
 >=>    >=>                                                              
  >=> >=>                                                                
    >=>                                                                  
    >=>                                                                  
    >=>                                                                  
    >=>                                                                  

•𝕄𝕒𝕕𝕖 𝕓𝕪: 𝑃𝑒𝑗𝑢 3𝑛𝑐𝑒𝑟
    {Style.RESET_ALL}
    """
    print(banner)
    print(Fore.MAGENTA + "[SECURITY SYSTEM INITIALIZED]" + Style.RESET_ALL)

# Fungsi untuk mengirim email notifikasi
def send_email(ip, reason):
    try:
        subject = f"[ALERT] Aktivitas mencurigakan dari {ip}"
        body = f"IP: {ip}\nAlasan: {reason}\nWaktu: {datetime.now()}"

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print(Fore.CYAN + f"[EMAIL] Notifikasi dikirim ke {EMAIL_RECEIVER}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal mengirim email: {e}" + Style.RESET_ALL)

# Fungsi untuk mencatat aktivitas mencurigakan
def log_attempt(ip, reason):
    log_data = {"ip": ip, "reason": reason, "time": str(datetime.now())}

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_data)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

    print(Fore.YELLOW + f"[ALERT] Aktivitas mencurigakan dari {ip}: {reason}" + Style.RESET_ALL)
    send_email(ip, reason)  # Kirim notifikasi email

# Fungsi untuk memblokir IP manual
def block_ip(ip):
    with open(BLOCKED_IPS, "a") as file:
        file.write(ip + "\n")
    os.system(f"iptables -A INPUT -s {ip} -j DROP")
    print(Fore.RED + f"[SECURITY] IP {ip} telah diblokir." + Style.RESET_ALL)

# Endpoint untuk deteksi serangan
@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    ip = data.get("ip")
    reason = data.get("reason")

    log_attempt(ip, reason)
    return {"status": "logged"}, 200

# Endpoint untuk memblokir IP secara manual
@app.route('/block', methods=['POST'])
def manual_block():
    data = request.get_json()
    ip = data.get("ip")

    if ip:
        block_ip(ip)
        return {"status": f"IP {ip} telah diblokir"}, 200
    return {"error": "IP tidak valid"}, 400

# Jalankan program
if __name__ == '__main__':
    show_banner()
    loading_animation()
    app.run(host="0.0.0.0", port=5000)