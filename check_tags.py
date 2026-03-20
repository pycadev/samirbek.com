import os
import django
from django.template import engines

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_tags():
    try:
        engine = engines['django']
        print("Available libraries:")
        for name in sorted(engine.engine.libraries.keys()):
            print(f"- {name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_tags()
