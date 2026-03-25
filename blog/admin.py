from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category', 'is_published', 'featured', 'created_at')
    list_filter = ('is_published', 'featured', 'category')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    
    # Senior Backup Button Integration
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['backup_url'] = '/api/lab/backup/'
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
