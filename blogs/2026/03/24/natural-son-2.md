birlar = {1:'bir', 2:'ikki', 3:'uch', 4:"to'rt", 5:'besh', 6:'olti', 7:'yetti', 8:'sakkiz', 9:"to'qqiz",0:''}
onlar = {1:"o'n", 2:'yigirma', 3:"o'ttiz", 4:'qirq', 5:'ellik', 6:'oltmish', 7:'yetmish', 8:'sakson',9:"to'qson", 0:''}
def onlik(a):
if a < 10:
return birlar[a]
else:
o = a // 10
b = a % 10
qiymat = onlar[o] + ' ' + birlar[b]
return qiymat
n = int(input())
if n == 1000:
print("bir ming")
elif n < 100:
print(onlik(n))
else:
y = n // 100
yk = birlar[y] + ' yuz'
if n % 100 == 0:
print(yk)
else:
print(yk + ' ' + onlik(n % 100))

Keling, kodingni "bo'laklab" tushuntiraman:

### 1\. Lug'atlar \(Ma'lumotlar bazasi\)

Python

```
birlar = {1:'bir', 2:'ikki', ... 0:''}
onlar = {1:"o'n", 2:'yigirma', ... 0:''}
```

Bu yerda sen sonlarni so'zga o'giruvchi "lug'at" yaratib olding. `0:''` bo'sh joy bo'lishi juda muhim, chunki masalan "20" sonida birlar xonasi nol bo'lsa, u hech narsa chop etmasligi kerak.

### 2\. O'nliklarni yasovchi funksiya

Python

```
def onlik(a):
    if a < 10:
        return birlar[a]
    else:
        o = a // 10  # O'nlar xonasi (masalan 25 // 10 = 2)
        b = a % 10   # Birlar xonasi (masalan 25 % 10 = 5)
        return onlar[o] + ' ' + birlar[b]
```

Bu funksiya 1 dan 99 gacha bo'lgan ixtiyoriy sonni so'zga aylantiradi. U sonni **butun bo'lish (`//`)** va **qoldiq (`%`)** orqali ikkiga ajratib, lug'atdan mos so'zlarni olib keladi.

### 3\. Asosiy mantiq \(Yuzliklar va Minglik\)

Dasturning pastki qismida iyerarxiya bo'yicha tekshiruv ketadi:

1. **Minglik:** Agar `n == 1000` bo'lsa, tamom, "bir ming" deb chiqadi.
2. **O'nlik:** Agar `n < 100` bo'lsa, boyagi `onlik(n)` funksiyasini chaqiradi.
3. **Yuzlik (Eng qiziq joyi):**
    Python

    ```
    y = n // 100  # Yuzlar xonasi (masalan 345 // 100 = 3)
    yk = birlar[y] + ' yuz' # "uch yuz"
    
    ```

    Keyin qoldig'iga qaraydi:
    * Agar `n % 100 == 0` bo'lsa (masalan 300), faqat "uch yuz"ni o'zi chiqadi.
    * Agar qoldiq bo'lsa (masalan 345), "uch yuz"ga `onlik(45)` natijasini qo'shib qo'yadi.

***

### Nega bu kod optimal?

* **O'qilishi oson:** Har bir qism o'z vazifasini bajaradi.
* **Xotira tejamkor:** Biz ortiqcha massivlar yaratmadik, faqat lug'atdan foydalandik.
* **To'g'rilik:** `n % 100 == 0` sharti "ikki yuz nol" kabi xunuk chiqishlarning oldini oladi.