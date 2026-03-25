1. **CINDER -** bu **CPYTHON** yani kuchaytirilgan python tezlashtirilgan hamda boyitilgan **PYTHON** 

bitta narsani bilishing kerak: **Cinder asosan Linux (x86\_64) uchun mo'ljallangan** va uni `pip install  ` qilib bo'lmaydi. Uni ishlatish uchun manba kodidan yig'ish (build) kerak

* [ ] yuklash uchun GITBASH dan
* [ ] [`git clone https://github.com/facebookincubator/cinder.git`](git clone https://github.com/facebookincubator/cinder.git)

***

> **Eslatma:** Cinder - bu alohida dasturiy til emas, balki Python'ning "shishirilgan" varianti. Agar sen oddiy web-sayt yoki bot yozayotgan bo'lsang, senga oddiy Python yetarli. Cinder — bu milliardlab foydalanuvchisi bor "gigantlar" uchun.

***

####  **Proxygen**

> *(Bu Meta tomonidan yaratilgan yuqori samarali HTTP server/freymvork. U sekundiga millionlab so‘rovlarni qabul qilib, ularni ichki "ishchi" serverlarga tarqatadi)*

####  TLS Termination

> *(Xavfsiz ulanish (HTTPS) shu yerda shifrdan yechiladi, bu esa ichki serverlarning yukini yengillatadi.)*


####  ASOS


##### **1.LOGIN MIKROSERVISI.** 

* [ ] **Login tugmasini bosganingda, backendda quyidagi jarayonlar zanjiri ishga tushadi:**
* **Auth Service:** Bu alohida mikroservis. U sening login/parolingni tekshiradi.
* **Password Hashing:** Paroling ochiq holda saqlanmaydi. U **Argon2** yoki **Bcrypt** kabi algoritmlar bilan shifrlangan bo'ladi.
* **Database Sharding (Milliardlab odamlar siri):** Instagram bitta bazaga hamma ma'lumotni sig'dira olmaydi. Ular ma'lumotlarni \*\*"Shard"\*\*larga (bo'laklarga) bo'lishadi. Masalan, foydalanuvchi ID raqamiga qarab, ma'lumotlar turli serverlarda saqlanadi.
    * *ID 1-1,000,000* -> 1-serverda.
    * *ID 1,000,001-2,000,000* -> 2-serverda.
    * *ID 2,000,001-3,000,000* -> 3-serverda. va hk.....


* **4\. Tezlikning Asosiy Siri: Kesh \(Caching\)** Instagram hamma narsani har safar ma'lumotlar bazasidan (HDD/SSD) so'rab o'tirmaydi.
* **Memcached va Redis:** Foydalanuvchi sessiyalari va login ma'lumotlari RAM (operativ xotira)da saqlanadi. RAM bazadan ko'ra **100-1000 marta tezroq** javob beradi.
* Agar sen kirsang, tizim seni "issiq" keshdan topadi va bazaga tushmasdanoq ichkariga kiritib yuboradi.

##### 2.Login jarayonining sxemasi

* **Siz:** `POST /login` so'rovini yuborasiz.
* **Edge Server:** So'rovni qabul qiladi va eng bo'sh Backend serverga uzatadi.
* **Django (Cinder):** Login logikasini ishga tushiradi.
* **Redis:** "Bu foydalanuvchi yaqinda kirganmidi?" deb tekshiradi.
* **PostgreSQL (Shard):** Agar keshda bo'lmasa, asosiy bazadan parolni tekshiradi.
* **Session Token:** Senga maxsus "kalit" (JWT yoki Session ID) beriladi va brauzeringga saqlanadi.

### Nima uchun qotib qolmaydi?

Milliardlab odamlar bir vaqtda kirsa ham, Instagram **Horizantal Scaling** (gorizontal kengayish) yordamida ishlaydi. Ya'ni, odam ko'paysa, yangi serverlar avtomatik qo'shiladi (Auto-scaling).

* **Vertical Scaling (Vertikal kengayish):** Sotuvchiga kuchliroq kompyuter berish yoki uning miyasini kuchaytirish. Lekin buni chegarasi bor. Bitta odam baribir million kishiga xizmat qila olmaydi.
* **Horizontal Scaling (Gorizontal kengayish):** Bu Instagram’ning siri. Ular bitta kuchli server o‘rniga, minglab o‘rtacha serverlarni parallel qo‘yib tashlashadi. Mijoz ko‘paydimi? Darrov yoniga yana 100 ta sotuvchi (server) qo‘shishadi.


### Avtomatik kengayish (Auto-scaling) qanday ishlaydi?

Instagram infratuzilmasida **"Metric Monitoring"** degan narsa bor. U har soniyada serverlarning "yurak urishini" (CPU yuklamasi, RAM ishlatilishi) kuzatib turadi.

1. **Trigger (Signal):** Masalan, bitta serverning protsessori 70% ga yuklanganda, tizimga "Hov, odam ko'payib ketdi, yordam kerak!" degan signal boradi.
2. **Spinning up (Yangi serverni uyg'otish):** **Kubernetes** yoki shunga o'xshash texnologiya yordamida soniyalar ichida yangi "Docker Container" (tayyor server nusxasi) ishga tushadi.
3. **Load Balancer (Navbat boshqaruvchisi):** Yangi server tayyor bo'lishi bilan, tepada turgan **Load Balancer** (masalan, Facebook'ning **Katran** dasturi) yangi kelayotgan foydalanuvchilarni o'sha bo'sh serverga yo'naltiradi.

***

### Nima uchun foydalanuvchi buni sezmaydi?

Buning bir necha texnik hiylalari bor:

* **Stateless Backend:** Instagram serverlari sening ma'lumotingni o'zida saqlamaydi. Sen 1-serverga so'rov yubordingmi yoki 100-servergami, ular uchun farqi yo'q. Hamma ma'lumot markaziy "Kesh" (Redis) va "Baza" (PostgreSQL) da turadi. Shuning uchun sen bir serverdan ikkinchisiga "sakrab o'tsang" ham, sessiyang uzilib qolmaydi.
* **Database Sharding:** Faqat serverlarni emas, ma'lumotlar bazasini ham bo'laklab tashlashgan. Agar hamma milliardlab odam bitta bazaga yopirilsa, baza "portlab" ketadi. Shuning uchun har bir foydalanuvchi o'zining alohida "bo'lagiga" (Shard) murojaat qiladi.
* **Microservices:** Instagram bitta katta dastur emas. Masalan, "Layk bosish" xizmati alohida serverlarda, "Rasm yuklash" xizmati alohida serverlarda ishlaydi. Agar hamma rasm yuklashga tushib ketsa ham, faqat rasm yuklash serverlari ko'payadi, boshqa funksiyalarga xalaqit bermaydi.

***

###Xulosa

Instagram "qotmaydi", chunki u bitta ulkan kompyuter emas, balki bir-biri bilan kelishib ishlaydigan millionlab kichik kompyuterlar to'dasi (cluster). Odam ko'paygan sari, bu "qo'shin" ham avtomatik kattalashib boradi.

                  **BLOK SXEMASI**

graph TD
    %% Foydalanuvchi harakati
    Start((Foydalanuvchi)) -->|Login/Parol yuboradi| Edge[Edge Server: Proxygen]
    
    %% Xavfsizlik va Filtrlash
    Edge -->|DDoS tekshiruvi| RateLimit{Rate Limiter}
    RateLimit -- Blok --> Reject[429 Too Many Requests]
    RateLimit -- Toza --> AuthSvc[Auth Microservice: Django/Cinder]

    %% Mantiqiy jarayon
    subgraph Backend_Process[Backend Tahlili]
        AuthSvc --> CacheCheck{Keshda bormi?}
        CacheCheck -- Ha --> Validate[Sessiyani tasdiqlash]
        CacheCheck -- Yo'q --> DB[(PostgreSQL Shard)]
        DB --> Verify[Parol Hashini tekshirish]
    end

    %% Natija
    Verify --> Result{To'g'rimi?}
    Result -- Xato --> Error[Xato xabari yuborish]
    Result -- To'g'ri --> Success[JWT Token yaratish]

    %% Yakuniy qadam
    Success --> Redis[(Redis: Session Store)]
    Redis --> Final((Muvaffaqiyatli kirish))

    %% Styles
    style Start fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#00f,stroke:#fff,color:#fff
    style Redis fill:#f00,stroke:#fff,color:#fff
    style AuthSvc fill:#ffa500,stroke:#333