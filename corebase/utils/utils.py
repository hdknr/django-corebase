from django.template import engines, loader
from django.utils.safestring import mark_safe
import markdown
from mimetypes import guess_type


def render(src, request=None, engine_name='django', safe=True, **ctx):
    text = engines[engine_name].from_string(src).render(ctx, request=request)
    return safe and mark_safe(text) or text


def render_by(name, request=None, safe=True, **ctx):
    t = loader.get_template(name)
    if is_filetype(name, 'text/markdown'):
        t = engines['django'].from_string(to_gfm(t.template.source)) 
    text = t.render(ctx, request=request)
    return safe and mark_safe(text) or text


def is_filetype(path, typename):
    return guess_type (path)[0] == typename


def to_gfm(text, safe=True):
    '''Github Favored Markdown'''
    if not text:
        return ''
    md = markdown.Markdown(extensions=['markdown.extensions.tables'])
    return mark_safe(md.convert(text)) if safe else md.convert(text)
