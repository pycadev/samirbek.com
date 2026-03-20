from django import forms
from .models import Post, Category, Tag
from markdownx.widgets import MarkdownxWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'summary', 'content', 'featured_image', 'is_published', 'featured']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'easymde-editor', 'class': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-4 text-2xl font-bold border-none bg-transparent outline-none placeholder-gray-400', 'placeholder': 'Sarlavha...'}),
            'summary': forms.Textarea(attrs={'class': 'w-full p-4 border border-gray-200 dark:border-gray-800 rounded-xl bg-gray-50 dark:bg-gray-800/50 outline-none focus:ring-2 focus:ring-blue-500', 'rows': 3, 'placeholder': 'Qisqacha mazmun...'}),
        }
