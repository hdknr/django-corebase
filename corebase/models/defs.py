from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey


class Timestamp(models.Model):
    created_at = models.DateTimeField(
        _("Created At"), help_text=_("Created At Help"), default=now
    )
    updated_at = models.DateTimeField(
        _("Updated At"), help_text=_("Updated At Help"), auto_now=True
    )

    class Meta:
        abstract = True


class BaseTreeModel(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent Node"),
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class BaseSuperModel(Timestamp):
    subclass_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Subclass Type"),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._meta.parents:
            self.subclass_type = ContentType.objects.get_for_model(self)
        super().save(*args, **kwargs)

    @property
    def instance(self):
        return (
            self.subclass_type
            and self.subclass_type.get_object_for_this_type(id=self.id)
            or self
        )

    @property
    def model(self):
        return self.subclass_type and self.subclass_type.model


class SuperModel(BaseTreeModel, BaseSuperModel):
    class Meta:
        abstract = True


class BaseModel(Timestamp):
    class Meta:
        abstract = True
