from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from .models import Post, Project, Category, Tag
from .forms import PostForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

@method_decorator(cache_page(60 * 15), name='dispatch') # 15 minute cache
class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(is_published=True, featured=True)[:3]
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) |
                Q(content__icontains=query)
            )
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return ['blog/partials/post_list_partial.html']
        return [self.template_name]

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prev/Next posts (Senior Navigation)
        context['next_post'] = Post.objects.filter(is_published=True, created_at__gt=self.object.created_at).order_by('created_at').first()
        context['prev_post'] = Post.objects.filter(is_published=True, created_at__lt=self.object.created_at).order_by('-created_at').first()
        
        # Git History (Senior Feature)
        try:
            import git
            repo = git.Repo(search_parent_directories=True)
            commits = list(repo.iter_commits(max_count=5))
            context['git_history'] = [{
                'hash': c.hexsha[:7],
                'message': c.message.strip(),
                'date': c.committed_datetime,
            } for c in commits]
        except Exception:
            context['git_history'] = []
            
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'blog/project_list.html'
    context_object_name = 'projects'

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'slug': self.object.slug})

from django.http import JsonResponse

import time
import os
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def lab_input_request(request):
    session_id = request.GET.get('session_id', 'default')
    cache_key = f"lab_input_{session_id}"
    start_time = time.time()
    while time.time() - start_time < 60:
        data = cache.get(cache_key)
        if data is not None:
            cache.delete(cache_key)
            return JsonResponse({'data': data})
        time.sleep(0.2)
    return JsonResponse({'data': ''}, status=204)

@csrf_exempt
def lab_input_provide(request):
    session_id = request.POST.get('session_id', 'default')
    data = request.POST.get('data', '')
    cache_key = f"lab_input_{session_id}"
    cache.set(cache_key, data, timeout=60)
    return JsonResponse({'status': 'ok'})

def stackframe_root(request):
    path = os.path.join(settings.BASE_DIR, 'static', 'vendor', 'monaco', 'stackframe.js')
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='application/javascript')
    return JsonResponse({'error': 'Not found'}, status=404)

def search_api(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    posts = Post.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))[:5]
    results = []
    for post in posts:
        results.append({
            'title': post.title,
            'url': post.get_absolute_url(),
            'type': 'Maqola',
            'icon': '📝'
        })
    
    projects = Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:3]
    for proj in projects:
        results.append({
            'title': proj.title,
            'url': '/projects/', # Simplified
            'type': 'Loyiha',
            'icon': '🚀'
        })
        
    return JsonResponse({'results': results})
