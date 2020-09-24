from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin
from ..utils import render


def default_list_display(model, exclude=[]):
    exclude = exclude or ["created_at"]
    return [f.name for f in model._meta.fields if f.name not in exclude]


def admin_link(instance, opt=None):
    opt = opt or instance._meta
    url_name = f"admin:{opt.app_label}_{opt.model_name}_change"
    return render('<a href="{% url u i.id %}">{{i}}</a>', u=url_name, i=instance)


admin_link.short_description = _("Admin Link")


class TreeModelAdmin(MPTTModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        for inline in self.inlines:
            if hasattr(inline, "get_urls"):
                urls = inline.get_urls(self) + urls
        return urls
