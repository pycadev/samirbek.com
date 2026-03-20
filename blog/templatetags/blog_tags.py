import markdown
import bleach
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def youtube_embed_callback(match):
    video_id = match.group(2)
    return (
        f'<div class="relative aspect-video my-10 rounded-3xl overflow-hidden shadow-2xl border border-gray-100 dark:border-gray-800">'
        f'<iframe class="absolute inset-0 w-full h-full" '
        f'src="https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" '
        f'frameborder="0" '
        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'referrerpolicy="strict-origin-when-cross-origin" '
        f'allowfullscreen></iframe>'
        f'</div>'
    )

@register.filter(name='markdownify')
def markdownify(value):
    if value is None:
        return ""
    
    # 1. YouTube Auto-Embed (Senior Level UX)
    # Patters for: youtube.com/watch?v=ID and youtu.be/ID
    yt_regex = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11}))'
    value = re.sub(yt_regex, youtube_embed_callback, str(value))

    # 2. Convert to HTML
    html_content = markdown.markdown(value, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    
    # 3. Sanitize HTML
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS | {
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr', 'pre', 'code',
        'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span', 'blockquote', 'iframe'
    }
    allowed_attrs = bleach.sanitizer.ALLOWED_ATTRIBUTES | {
        'img': ['src', 'alt', 'title', 'class', 'style'],
        'pre': ['class'],
        'code': ['class'],
        'div': ['class'],
        'span': ['class'],
        'iframe': ['src', 'class', 'frameborder', 'allow', 'allowfullscreen', 'width', 'height', 'style', 'referrerpolicy'],
    }
    
    clean_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs)
    
    return mark_safe(clean_html)
