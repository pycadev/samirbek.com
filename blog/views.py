from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from .models import Post, Project, Category, Tag, Snippet
from .forms import PostForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
import os
import subprocess

# --- Virtual Cloud Terminal (Senior Feature) ---
@user_passes_test(lambda u: u.is_superuser)
def cloud_terminal_view(request):
    return render(request, 'cloud/terminal.html')

@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def cloud_execute_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command', '').strip()
            cwd = data.get('cwd', os.getcwd()) # Track state
            
            if not command:
                return JsonResponse({'output': '', 'cwd': cwd})

            # Handle internal 'cd' command since subprocess spawn doesn't persist cwd
            if command.startswith('cd '):
                target_dir = command[3:].strip()
                new_cwd = os.path.abspath(os.path.join(cwd, target_dir))
                if os.path.isdir(new_cwd):
                    return JsonResponse({'output': '', 'cwd': new_cwd})
                else:
                    return JsonResponse({'output': f"cd: {target_dir}: No such file or directory\n", 'cwd': cwd})
            
            # --- Pure Python Emulation for Kali Linux Commands (Bypass WinError 1260) ---
            if command == 'clear':
                return JsonResponse({'output': '__CLEAR__', 'cwd': cwd})
                
            parts = command.split()
            base_cmd = parts[0].lower()
            
            try:
                # 1. 'ls' (List directory)
                if base_cmd in ['ls', 'dir']:
                    entries = os.listdir(cwd)
                    out = ""
                    for e in entries:
                        p = os.path.join(cwd, e)
                        if os.path.isdir(p): out += f"[DIR]  {e}\n"
                        else: out += f"       {e}\n"
                    return JsonResponse({'output': out if out else "Empty directory\n", 'cwd': cwd})
                
                # 2. 'mkdir' (Make directory)
                elif base_cmd == 'mkdir':
                    if len(parts) > 1:
                        target = os.path.join(cwd, parts[1])
                        os.makedirs(target, exist_ok=True)
                        return JsonResponse({'output': '', 'cwd': cwd})
                    return JsonResponse({'output': "mkdir: missing operand\n", 'cwd': cwd})
                
                # 3. 'touch' (Create empty file)
                elif base_cmd == 'touch':
                    if len(parts) > 1:
                        target = os.path.join(cwd, parts[1])
                        open(target, 'a').close()
                        return JsonResponse({'output': '', 'cwd': cwd})
                    return JsonResponse({'output': "touch: missing file operand\n", 'cwd': cwd})
                
                # 4. 'rm' (Remove file/dir)
                elif base_cmd == 'rm':
                    if len(parts) > 1:
                        target = os.path.join(cwd, parts[-1])
                        if os.path.isdir(target):
                            import shutil
                            shutil.rmtree(target)
                        elif os.path.exists(target):
                            os.remove(target)
                        else:
                            return JsonResponse({'output': f"rm: cannot remove '{parts[-1]}': No such file or directory\n", 'cwd': cwd})
                        return JsonResponse({'output': '', 'cwd': cwd})
                    return JsonResponse({'output': "rm: missing operand\n", 'cwd': cwd})
                
                # 5. 'cat' (Read file)
                elif base_cmd == 'cat':
                    if len(parts) > 1:
                        target = os.path.join(cwd, parts[1])
                        if os.path.exists(target) and os.path.isfile(target):
                            with open(target, 'r', encoding='utf-8') as f:
                                return JsonResponse({'output': f.read() + '\n', 'cwd': cwd})
                        return JsonResponse({'output': f"cat: {parts[1]}: No such file or directory\n", 'cwd': cwd})
                    return JsonResponse({'output': "cat: missing file operand\n", 'cwd': cwd})

                # 6. 'pwd' (Print Working Directory)
                elif base_cmd == 'pwd':
                    return JsonResponse({'output': f"{cwd}\n", 'cwd': cwd})
                
                # 7. 'echo' (Print text / Write to file)
                elif base_cmd == 'echo':
                    text_content = command[5:].strip()
                    # simplistic detect of > redirection
                    if '>' in text_content:
                        text_parts = text_content.split('>', 1)
                        content = text_parts[0].strip()
                        file_target = os.path.join(cwd, text_parts[1].strip())
                        
                        # Remove quotes if they exist around string
                        if content.startswith(("'", '"')) and content.endswith(("'", '"')):
                            content = content[1:-1]
                            
                        with open(file_target, 'w', encoding='utf-8') as f:
                            f.write(content)
                        return JsonResponse({'output': '', 'cwd': cwd})
                    else:
                        out = text_content
                        if out.startswith(("'", '"')) and out.endswith(("'", '"')): out = out[1:-1]
                        return JsonResponse({'output': out + '\n', 'cwd': cwd})
                
                # 8. 'chmod' (Change mode/permissions - dummy mock on windows)
                elif base_cmd == 'chmod':
                    if os.name == 'nt':
                        return JsonResponse({'output': f"chmod {parts[1]} applied to {parts[2]} (Emulated on Windows)\n", 'cwd': cwd})
                    
                # 9. Direct Python Exec (Bypasses Subprocess constraints)
                elif base_cmd == 'python' or base_cmd == 'python3':
                    if '-c' in command:
                        code = command.split('-c')[1].strip()
                        if code.startswith(("'", '"')) and code.endswith(("'", '"')): code = code[1:-1]
                        
                        import sys, io
                        # Capture STDOUT
                        old_stdout = sys.stdout
                        new_stdout = io.StringIO()
                        sys.stdout = new_stdout
                        try:
                            exec(code)
                            output = new_stdout.getvalue()
                        except Exception as e:
                            output = f"Error: {e}"
                        finally:
                            sys.stdout = old_stdout
                        return JsonResponse({'output': output if output else '\n', 'cwd': cwd})

            except Exception as e:
                return JsonResponse({'output': f"Internal Command Error: {e}\n", 'cwd': cwd})

            # For anything else (like pip, nmap), try subprocess but without shell=True to avoid CMD.exe group policy block
            try:
                import shlex
                process = subprocess.Popen(
                    shlex.split(command),
                    shell=False, # <-- Bypass CMD.exe block
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(timeout=15)
                
                output = stdout
                if stderr:
                    output += f"\nError: {stderr}"
                    
                return JsonResponse({'output': output, 'cwd': cwd})
                
            except FileNotFoundError:
                 return JsonResponse({'output': f"bash: {base_cmd}: command not found\n", 'cwd': cwd})
            except subprocess.TimeoutExpired:
                process.kill()
                return JsonResponse({'output': "Execution Timeout (15s limit)\n", 'cwd': cwd})
            except Exception as e:
                if "WinError 1260" in str(e) or "Access is denied" in str(e):
                    return JsonResponse({'output': f"Windows Security Blocked '{base_cmd}'. Please use emulated commands (ls, mkdir, echo...)\n", 'cwd': cwd})
                return JsonResponse({'output': f"System Error: {str(e)}\n", 'cwd': cwd})
        except Exception as e:
            return JsonResponse({'output': f"Critical Server Error: {str(e)}\n", 'cwd': cwd})
            
    return JsonResponse({'error': 'Invalid method'}, status=405)

@method_decorator(cache_page(60 * 15), name='dispatch') # 15 minute cache
class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(is_published=True, featured=True)[:3]
        return context

class AboutView(TemplateView):
    template_name = 'blog/about.html'

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

class SpecialPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=False)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) |
                Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_special_section'] = True
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['blog/partials/post_list_partial.html']
        return [self.template_name]

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
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
        return self.request.user.is_superuser

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def test_func(self):
        return self.request.user.is_superuser

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

import shutil
import tempfile
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def download_markdown_backup(request):
    """
    Zips the entire 'blogs/' directory and returns it as a download.
    Senior Level Backup Implementation using in-memory BytesIO to avoid Windows PermissionError.
    """
    import zipfile
    import io
    import time
    
    blogs_dir = os.path.join(settings.BASE_DIR, 'blogs')
    if not os.path.exists(blogs_dir):
        return JsonResponse({'error': 'Blogs directory not found'}, status=404)
        
    # Create an in-memory zip file
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(blogs_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the arcname (relative path inside the zip)
                arcname = os.path.relpath(file_path, settings.BASE_DIR)
                zipf.write(file_path, arcname)
                
    # Reset buffer position to start
    buffer.seek(0)
    
    response = FileResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="blogs_backup_{time.strftime("%Y%m%d")}.zip"'
    return response

def stackframe_root(request):

    path = os.path.join(settings.BASE_DIR, 'static', 'vendor', 'monaco', 'stackframe.js')
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='application/javascript')
    return JsonResponse({'error': 'Not found'}, status=404)

from django.shortcuts import render, redirect
import json

@csrf_exempt
def save_snippet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            if code:
                snippet = Snippet.objects.create(code=code)
                # Return the absolute URL relative to the domain
                return JsonResponse({'url': f'/lab/{snippet.id}/'})
            return JsonResponse({'error': 'No code provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def lab_shared_view(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        # Re-using the home view context but injecting the shared code
        featured_posts = Post.objects.filter(is_published=True, featured=True)[:3]
        return render(request, 'blog/home.html', {
            'featured_posts': featured_posts, 
            'shared_code': snippet.code
        })
    except Snippet.DoesNotExist:
        return redirect('blog:home')


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
