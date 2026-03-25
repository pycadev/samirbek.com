# 🚀 Professional Linux Deployment: Gunicorn & Nginx (Ultra-Senior Guide)

Jigarim, bu daxshatli qo'llanma sizning blogingizni real serverda (Ubuntu/Kali) xuddi she'rdek ravon va chaqmoqdek tez ishlashini ta'minlaydi. 
**DIQQAT:** Loyihangiz `/root/sarim/` papkasida ekanligini inobatga olib, barcha sozlamalarni temir-beton qildim! MinIO hozircha kerak emas.

---

### ⌨️ Nano Tahrirlovchisi (Master Guide)
Serverda fayllarni tahrirlash uchun biz `nano`dan foydalanamiz. Mana eng kerakli qadamlar:
- **Faylni ochish:** `sudo nano /path/to/file`
- **Saqlash (Save):** `Ctrl + O` (Keyin `Enter` bosing)
- **Chiqish (Exit):** `Ctrl + X`
- **Izlash (Find):** `Ctrl + W` (Text yozib e-ter bosing)
- **Undo (Orqaga):** `Alt + U`

---

### 1-qadam: Loyiha O'rnashgan Joy
Loyiha `/root/sarim/` da ekanligini tekshiramiz:

```bash
cd /root/sarim
```
```bash
ls -la
```
> **Tekshirish:** `manage.py`, `config/`, `blog/` va `venv/` ko'rinishi shart.

---

### 2-qadam: Python Muhiti (Venv)
Virtual muhitni faollashtirib, **Gunicorn**ni o'rnatamiz:

```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
pip install gunicorn
```
> **Muhim:** Gunicorn - bu sizning Django ilovangizni 8000 portda dunyoga taqdim qiluvchi asosiy vositadir.

---

### 3-qadam: Gunicorn Systemd Service (Avto-Start)
Gunicorn server o'chib yonganda o'zi avtomatik yonishi uchun:
`sudo nano /etc/systemd/system/gunicorn.service`

**Fayl ichiga quyidagilarni paste qiling:**
```ini
[Unit]
Description=Gunicorn daemon for sarim project
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/sarim
# ExecStart dagi port 8000 bo'lishiga e'tibor bering!
ExecStart=/root/sarim/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application
# Agar biror narsa buzilsa, o'zi qayta ishga tushadi:
Restart=always

[Install]
WantedBy=multi-user.target
```

**Xizmatni faollashtirish:**
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl start gunicorn
```
```bash
sudo systemctl enable gunicorn
```
> **Tekshirish:** `sudo systemctl status gunicorn`. Agar **Active (running)** bo'lsa, demak hammasi daxshat!

---

### 4-qadam: Nginx (Dizayn va Aloqa)
Nginx statik fayllarni (CSS, JS) uchiradi va 8000 portni dunyoga (80 portga) bog'laydi.
`sudo nano /etc/nginx/sites-available/sarim`

**Fayl ichiga quyidagilarni paste qiling:**
```nginx
# --- 💎 Senior Level Nginx Configuration 🚀 ---

upstream django_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name samirbek.com 192.168.209.250; # Domain yoki IP ni bura yozing

    # Statik fayllar (Nginx alias orqali - root/sarim dan)
    location /static/ {
        alias /root/sarim/staticfiles/;
        expires 30d;
    }

    # Media fayllar
    location /media/ {
        alias /root/sarim/media/;
        expires 30d;
    }

    # Asosiy requestlarni Gunicorn (8000 port)ga yuborish
    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 50M;
}
```

**Nginxni yoqish:**
```bash
sudo ln -s /etc/nginx/sites-available/sarim /etc/nginx/sites-enabled
```
```bash
sudo nginx -t
```
```bash
sudo systemctl restart nginx
```

---

### 5-qadam: Yangilash (Deploy Workflow)
Ertaga kodingizni o'zgartirsangiz, faqat mana bularni bajarasiz:

```bash
git pull
```
```bash
source venv/bin/activate
```
```bash
python manage.py collectstatic --noinput
```
```bash
python manage.py migrate
```
```bash
sudo systemctl restart gunicorn
```

---

### 🚀 Bonus: Standalone EXE yaratish (Windows)
Agar saytingizni shunchaki `.exe` qilib ishlatmoqchi bo'lsangiz (D:/sarim papkasida), quyidagilarni bajaring:

**1. Kerakli kutubxonalarni o'rnatish:**
```bash
pip install waitress pyinstaller
```

**2. Loyihani yig'ish (Build):**
```bash
pyinstaller run.spec
```

**3. Natija:**
`dist/` papkasi ichida `sarim_blog.exe` fayli paydo bo'ladi. Uni Desktopga tashlab RUN bersangiz, u o'zi:
- `D:/sarim` papkasini yaratadi.
- Bazani ko'chiradi.
- Statik fayllarni yig'adi.
- Brauzerni avtomatik ochadi.

---

### 💎 Senior Touch (Ruxsatlar)
Nginx `/root/` papkasini bemalol o'qishi uchun ruxsat beramiz:
```bash
sudo chmod -R 755 /root/sarim
```

Jigarim, endi saytingiz ham Linuxda, ham Windowsda eng professional holatda! 🦾🎩🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀   (P.S. Nanodagi `Ctrl+X`ni unutmang!)

```python
print("Loyiha muvaffaqiyatli ishga tushdi!")
print("Sizga omad, buyuk ishlar kutmoqda! 🚀🦾")
```