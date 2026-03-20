# Samirbek Lab v3.2 - Senior Offline Python IDE 🚀💎🛡️

Samirbek Lab — bu blog saytingizga integratsiya qilingan, to'liq offline ishlovchi va yuqori darajadagi (Senior Level) interaktiv Python dasturlash muhiti.

## 🌟 Asosiy Imkoniyatlar
- **To'liq Offline**: Brauzerning o'zida Pyodide (WASM) orqali ishlaydi, internet kerak emas.
- **Web Worker Arxitekturasi**: Python kodi alohida oqimda (thread) ishlaydi. Bu sahifa qotib qolishining oldini oladi (hatto cheksiz tsikllarda ham).
- **Real-time REPL Terminal**: Konsol qismi haqiqiy interaktiv terminalga aylantirilgan (`>>>` prompti bilan).
- **Pop-upsiz Input**: `input()` funksiyasi ishlatilganda brauzerning zerikarli oynalari chiqmaydi, ma'lumot to'g'ridan-to'g'ri terminalga yoziladi.
- **Senior Syntax Highlighting**: Monaco Editor uchun maxsus `senior-light` mavzusi yaratilgan bo'lib, barcha Python keywordlari, funksiyalari va raqamlari professional darajada bo'yaladi.
- **IDLE Mode**: `Shift + Enter` orqali faqat tanlangan qatorni yoki kursor turgan qatorni yurgizish imkoniyati (REPL).

## 🛠️ Texnik Arxitektura
Loyiha uchta asosiy komponentdan tashkil topgan:

1.  **`static/js/ide-worker.js`**:
    - Pyodide-ni fonda yuklaydi va sozlaydi.
    - `stdout`, `stderr` va `stdin` oqimlarini boshqaradi.
    - Python kodini `runPythonAsync` orqali xavfsiz ishga tushiradi.
2.  **`templates/base.html`**:
    - Monaco Editor-ni sozlaydi.
    - Terminal interfeysini (`contentEditable`) boshqaradi.
    - Foydalanuvchi klaviatura inputlarini API orqali Worker-ga uzatadi.
3.  **`blog/views.py` (Blocking Sync API)**:
    - `lab_input_request`: Worker-ni kutib turish holatiga (blocking) o'tkazadi.
    - `lab_input_provide`: Foydalanuvchi kiritgan ma'lumotni Worker-ga yetkazadi.

## ⌨️ Shoshilinch Klavishlar
- **`Ctrl + Shift + P`**: Laboratoriyani ochish.
- **`F5`**: Butun kodni yurgizish.
- **`Shift + Enter`**: Tanlangan qatorni yurgizish (REPL).
- **`ESC`**: Laboratoriyani yopish.

## 🔧 O'rnatish va Sozlash
Loyiha Django-ga to'liq integratsiya qilingan. Barcha assetlar (`static/vendor/`) loyiha ichida mavjud bo'lishi kerak. `blog/urls.py` faylida API endpointlar ro'yxatdan o'tgan bo'lishi shart.

---
*Created with ❤️ by Antigravity for Samirbek Blog*
