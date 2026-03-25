import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post

def sync_posts():
    posts = Post.objects.all()
    count = 0
    for post in posts:
        post.save() # This triggers the markdown file creation
        count += 1
    print(f"Successfully synced {count} posts to Markdown files.")

if __name__ == "__main__":
    sync_posts()
