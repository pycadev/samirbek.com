from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from django.utils.text import slugify
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.core.cache import cache

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(max_length=500)
    content = MarkdownxField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    markdown_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Markdown file synchronization (Senior Level Logic)
        from django.conf import settings
        import os
        from django.utils import timezone
        
        # Ensure we have a date (for new posts)
        save_date = self.created_at or timezone.now()
        
        relative_path = os.path.join(
            'blogs', 
            str(save_date.year), 
            f"{save_date.month:02d}", 
            f"{save_date.day:02d}", 
            f"{self.slug}.md"
        )
        full_path = os.path.join(settings.BASE_DIR, relative_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write content to file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self.content or "")
            
        self.markdown_path = relative_path

        if self.featured_image:
            try:
                img = Image.open(self.featured_image)
                if img.height > 1080 or img.width > 1920:
                    img.thumbnail((1920, 1080))
                    img_io = io.BytesIO()
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(img_io, format='JPEG', quality=85)
                    self.featured_image.save(self.featured_image.name, ContentFile(img_io.getvalue()), save=False)
            except Exception as e:
                print(f"Image error: {e}")
        
        # Clear cache on save (Senior Level)
        cache.clear()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        """Hesoblaydi o'rtacha o'qish vaqtini (minutlarda)"""
        words = len(str(self.content).split())
        read_time_mins = max(1, words // 200) # 200 words per minute average
        return read_time_mins

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    context = models.TextField(help_text="Qanday muammo bor edi?")
    tech_stack = models.CharField(max_length=500, help_text="Texnologiyalar steki (vergul bilan ajrating)")
    result = models.TextField(help_text="Qanday natijaga erishildi?")
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        if self.image:
            try:
                img = Image.open(self.image)
                if img.height > 1080 or img.width > 1920:
                    img.thumbnail((1920, 1080))
                    img_io = io.BytesIO()
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(img_io, format='JPEG', quality=85)
                    self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
            except Exception as e:
                print(f"Project image error: {e}")
        
        # Clear cache on save (Senior Level)
        cache.clear()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

import uuid

class Snippet(models.Model):
    id = models.CharField(max_length=10, primary_key=True, editable=False)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate short 6-char unique ID
            self.id = uuid.uuid4().hex[:6]
            # Ensure uniqueness
            while Snippet.objects.filter(id=self.id).exists():
                self.id = uuid.uuid4().hex[:6]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Snippet {self.id}"

