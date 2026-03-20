import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post, Category, Tag

def populate():
    # 1. Category
    cat, _ = Category.objects.get_or_create(name="Personal", defaults={'slug': 'personal'})
    
    # 2. Tags
    tags_list = ["CV", "Backend", "Senior", "AI", "Story"]
    tags = []
    for t_name in tags_list:
        tag, _ = Tag.objects.get_or_create(name=t_name, defaults={'slug': slugify(t_name)})
        tags.append(tag)
        
    # 3. Content
    content = """# Samirbek | Senior Backend Engineer & AI Researcher

Salom! Men Samirbek, yuqori yuklamali tizimlar (High-load) va AI integratsiyasi bo'yicha Backend muhandisiman. Ushbu maqola mening professional tajribam, ko'nikmalarim va qiziqishlarim haqida qisqacha ma'lumot beradi.

---

## 🚀 Professional Xulosa
5 yildan ortiq tajribaga ega bo'lgan Backend muhandisi sifatida men murakkab tizimlar arxitekturasini loyihalash, ma'lumotlar bazasini optimallashtirish va sun'iy intellekt modellarini real vaqt rejimida integratsiya qilishga ixtisoslashganman. Mening falsafam: **"Kodni shunchaki yozish emas, balki uni san'at darajasida optimallashtirish."**

## 🛠 Texnik Stack
- **Languages**: Python (Expert), JavaScript/Node.js, Go (Learning).
- **Frameworks**: Django (Best practice), FastAPI, Flask, HTMX.
- **Databases**: PostgreSQL (Optimization), Redis (Caching), SQLite.
- **Infrastructure**: Docker, Nginx, GitHub Actions, Linux/VPS.
- **Frontend**: Tailwind CSS (Senior UI/UX), Modern HTML5.

## 💼 Tajriba va Loyihalar

### 1. PyGen AI - Advanced AI Platform
- Murakkab AI generator algoritmlarini optimallashtirish.
- Tizim unumdorligini 40% ga oshirish va kesh tizimini joriy qilish.

### 2. High-Performance Portfolio & Blog
- HTMX va Django orqali "SPA-like" tajribani SSR (Server Side Rendering) bilan birlashtirish.
- Barcha static fayllarni offline rejimga o'tkazish va rasm optimallashtirish tizimini yaratish.

## 📈 Yutuqlar
- **DB Optimization**: So'rovlar vaqtini 70% gacha qisqartirish (Indexing & Caching).
- **Architecture**: Monolitdan microservice-ga o'tish tajribasi.
- **Community**: O'zbek dasturlash hamjamiyatida aktiv mentorlik.

## 🎓 Ta'lim va Kurslar
- Kompyuter fanlari va muhandisligi bo'yicha oliy ma'lumot.
- "Senior Software Architecture" - xalqaro sertifikatsiyasi.

---

### Meni ijtimoiy tarmoqlarda toping:
- [GitHub](https://github.com/samirbek)
- [LinkedIn](https://linkedin.com/in/samirbek)
- [Telegram](https://t.me/samirbek_blog)

> **"Eng yaxshi kod — bu yozilmagan, lekin vazifani bajaradigan koddir."**
"""
    
    # 4. Create Post
    post, created = Post.objects.get_or_create(
        title="Samirbek | Senior Backend Engineer & AI Researcher (CV)",
        defaults={
            'slug': 'samirbek-senior-backend-cv',
            'summary': "Samirbekning professional tajribasi, texnik stack va portfoliosi jamlangan Senior darajadagi CV maqolasi.",
            'content': content,
            'category': cat,
            'is_published': True,
            'featured': True,
            'featured_image': 'blog_images/cv_hero.png'
        }
    )
    
    if created:
        post.tags.set(tags)
        print("Success: CV post created!")
    else:
        print("Note: CV post already exists.")

if __name__ == "__main__":
    populate()
