from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify


class AbstractAuditModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    created_by = models.EmailField(_('created by'), blank=True, null=True, )
    last_updated_at = models.DateTimeField(_('last updated'), auto_now=True)
    last_updated_by = models.EmailField(_('created by'), blank=True, null=True, )

    class Meta:
        abstract = True


class SlugModelMixin(object):
    def get_slug(self):
        raise NotImplemented

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_slug())
        super(SlugModelMixin, self).save(*args, **kwargs)
