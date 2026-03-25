# Loyihani O'rnatish va Ishga Tushirish Qadamlari (Steps)

Ushbu qadamlar yordamida loyiha noldan senior darajasida quriladi.

## 1. Ma'lumotlar Bazasi (PostgreSQL) Sozlash
Foydalanuvchi tizimida PostgreSQL o'rnatilmaganligi sababli, `./pgsql` papkasidan foydalanamiz:
1.  **Baza yaratish**: `bin\initdb -D ./data`
2.  **Serverni yoqish**: `bin\pg_ctl -D ./data -l logfile start`
3.  **DB va User yaratish**:
    ```sql
    CREATE DATABASE insta_db;
    CREATE USER admin WITH PASSWORD 'admin123';
    GRANT ALL PRIVILEGES ON DATABASE insta_db TO admin;
    ```

## 2. Django Muhitini Tayyorlash
1.  **Venv yaratish**: `python -m venv venv`
2.  **Kutubxonalarni o'rnatish**:
    ```bash
    pip install django psycopg2 redis django-redis gunicorn uvicorn
    ```
3.  **Loyiha yaratish**: `django-admin startproject config .`
4.  **App yaratish**: `python manage.py startapp accounts`

## 3. Optimallashtirish (Optimization)
1.  **Indexing**: `accounts/models.py` da `db_index=True` qilib `username` ni belgilash.
2.  **Redis Cache**: `settings.py` da `CACHES` ni Redisga yo'naltirish.
3.  **Session Management**: `SESSION_ENGINE = "django.contrib.sessions.backends.cache"`

## 4. Kodlash (Implementation)
1.  **RegisterView**: Parollarni `make_password` bilan hashlab saqlash.
2.  **LoginView**:
    -   Redisdan `login_attempts` ni tekshirish (Security).
    -   Muvaffaqiyatli lo'gindan so'ng user ma'lumotlarini Redisga yozish.
3.  **HomeView**: `cache.get()` orqali ma'lumotni RAMdan olish.

## 5. UI/UX (Senior Level)
-   `index.css`: Glassmorphism va dark mode.
-   `htmx`: Login/Register formalarini sahifani yangilamasdan (SPA style) yuborish.