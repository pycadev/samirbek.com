import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post, Category, Tag, Project
from django.contrib.auth.models import User

def populate():
    # Create Superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin / admin123")

    # Categories
    categories = ['Backend', 'AI & Machine Learning', 'Engineering Culture']
    cat_objs = []
    for cat in categories:
        c, _ = Category.objects.get_or_create(name=cat, slug=slugify(cat))
        cat_objs.append(c)

    # Tags
    tags = ['Python', 'Django', 'HTMX', 'PostgreSQL', 'LLM', 'Security']
    tag_objs = []
    for tag in tags:
        t, _ = Tag.objects.get_or_create(name=tag, slug=slugify(tag))
        tag_objs.append(t)

    # Projects
    projects_data = [
        {
            'title': 'PyGen AI: Agentic Workflow System',
            'description': 'PyGen AI - bu LLM modellari asosida ishlaydigan agentik ish jarayonlarini boshqarish platformasi. U murakkab muhandislik vazifalarini avtomatlashtirish uchun mo\'ljallangan.',
            'context': 'AI agentlarini boshqarish va ularni korporativ tizimlarga integratsiya qilishda qiyinchilik bor edi.',
            'tech_stack': 'Django FastAPI Redis PostgreSQL Ollama',
            'result': 'AI agentlarini integratsiya qilish vaqti 5 barobarga qisqardi.',
            'github_url': 'https://github.com/samirbek/pygen-ai',
            'live_url': 'https://pygen.ai'
        },
        {
            'title': 'Aviation Maintenance Control (AMC)',
            'description': 'Aviatsiya texnik xizmati ko\'rsatishni boshqarish tizimi. Hujjatlar aylanishi, ehtiyot qismlar nazorati va texnik xodimlar malakasini baholash modullarini o\'z ichiga oladi.',
            'context': 'Aviatsiya texnik xizmati va hujjat aylanishini avtomatlashtirish kerak edi.',
            'tech_stack': 'Django HTMX Tailwind PostgreSQL',
            'result': 'Hujjatlarni qayta ishlash xatolari 30% ga kamaydi.',
            'github_url': 'https://github.com/samirbek/amc-system',
            'live_url': '#'
        },
        {
            'title': 'Real-time Analytics Engine',
            'description': 'Katta hajmdagi ma\'lumotlarni real vaqt rejimida qayta ishlash va vizualizatsiya qilish tizimi. HTMX orqali sahifani yangilamasdan dinamik chartlar taqdim etadi.',
            'context': 'Ma\'lumotlar tahlili uchun og\'ir JS kutubxonalaridan voz kechish kerak edi.',
            'tech_stack': 'Django HTMX Redis D3.js',
            'result': 'Sahifa yuklanish tezligi 3 barobar oshdi.',
            'github_url': 'https://github.com/samirbek/realtime-analytics',
            'live_url': '#'
        }
    ]

    for proj in projects_data:
        p, created = Project.objects.update_or_create(
            title=proj['title'],
            defaults={
                'description': proj['description'],
                'context': proj['context'],
                'tech_stack': proj['tech_stack'],
                'result': proj['result'],
                'github_url': proj['github_url'],
                'live_url': proj['live_url']
            }
        )

    print("Populating projects complete!")

if __name__ == '__main__':
    populate()
