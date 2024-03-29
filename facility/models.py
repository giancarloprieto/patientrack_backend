from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AbstractAuditModel, SlugModelMixin


class Facility(SlugModelMixin, AbstractAuditModel):
    slug = models.SlugField(unique=True, max_length=100)
    name = models.CharField(_('nombre'), max_length=100)
    address = models.CharField(_('dirección'), max_length=300)
    phone = models.CharField(_('teléfono'), max_length=30)
    email = models.EmailField(_('correo electrónico'))

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.name
