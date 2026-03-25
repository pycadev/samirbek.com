### 1\. Palindromning siri: Markazda nima bor?

Palindrom — bu markazdan qaraganda chap va o'ng tomoni ko'zgudagidek bir xil bo'lgan so'z.
Lekin bitta nozik joyi bor:

1. **Toq uzunlikdagi palindrom:** Markaz bitta harf (masalan, `aba` -> markaz `b`).
2. **Juft uzunlikdagi palindrom:** Markaz ikkita harf orasida (masalan, `abba` -> markaz `bb` ning o'rtasi).

***

### 2\. Senior darajadagi Algoritm \(Expand Around Center\)

Biz satrning har bir harfini "markaz" deb tasavvur qilamiz va undan tashqariga qarab kengayamiz.
Python

```
def longestPalindrome(s: str) -> str:
    """
    Berilgan matndagi eng uzun palindrom qismni topadi.
    Complexity: Time O(n^2) | Space O(1)
    """
    if not s:
        return ""
    
    res = ""
    
    def expand(left: int, right: int) -> str:
        # Markazdan chapga va o'ngga kengayamiz, toki harflar bir xil bo'lguncha
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # To'xtagan joyimizdan bitta ichkaridagi qismni qaytaramiz
        return s[left + 1:right]

    for i in range(len(s)):
        # 1. Toq palindromni tekshiramiz (markaz - i)
        p1 = expand(i, i)
        # 2. Juft palindromni tekshiramiz (markaz - i va i+1)
        p2 = expand(i, i + 1)
        
        # Eng uzunini tanlaymiz
        current_max = p1 if len(p1) >= len(p2) else p2
        
        # Agar yangi rekord bo'lsa, natijani yangilaymiz
        # Shartda: Agar 2ta bo'lsa birinchisini qaytaring deyilgan, 
        # shuning uchun faqat qat'iy kattasini olamiz.
        if len(current_max) > len(res):
            res = current_max
            
    return res
```

***

### 3\. Kodni "yoyib\-sochib" tushuntirish

#### **Qadam 1: Markazni tanlash**

Biz satrning har bir harfiga (indeksiga) boramiz. Masalan, `babad` so'zida `i=1` (ya'ni `a` harfi) ustida turibmiz.

#### **Qadam 2: Kengayish (The Expansion)**

Biz `expand` funksiyasini chaqiramiz. U xuddi antenna kabi:

* Chap tomonga bitta qadam tashlaydi (`left -= 1`).
* O'ng tomonga bitta qadam tashlaydi (`right += 1`).
* Agar ikkala tomondagi harf bir xil bo'lsa, yana kengayadi. Bo'lmasa — to'xtaydi.

#### **Qadam 3: Toq va Juft holati**

* `expand(i, i)` — bu `a` harfini markaz qilib, `b-a-b` ni topadi.
* `expand(i, i+1)` — bu `a` va uning yonidagi `b` ni markaz qilib, `ba` ni tekshiradi (bu yerda o'xshamaydi).

***

### 4\. Nima uchun bu yechim "Google Level"?

1. **Vaqt ($O(n^2)$):** Satrda $n$ ta markaz bor va har biridan kengayish ko'pi bilan $n$ qadam oladi. Bu juda tez.
2. **Xotira ($O(1)$):** Biz qo'shimcha massiv yoki jadval (DP table) yaratmadik. Faqat ko'rsatkichlar (`left`, `right`) bilan ishladik. Bu xotirani tejashning eng cho'qqisi.
3. **Birinchisini qaytarish:** Masala shartida `"bab"` va `"aba"` bo'lsa birinchisini qaytarish so'ralgan. Bizning kodda `if len(current_max) > len(res)` sharti yangi kelgan xuddi shunaqa uzunlikdagi palindromni olmaydi, faqat birinchisini saqlab qoladi.