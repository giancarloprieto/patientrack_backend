from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication import utils


# Create your models here.

class User(AbstractUser):
    picture = models.ImageField(_('picture'), null=True, blank=True, upload_to=utils.upload_to)
    is_patient = models.BooleanField(_('is patient'), default=False)
    facility = models.ForeignKey('facility.Facility', related_name='facility_user_set', verbose_name=_('facility'),
                                 null=True, on_delete=models.SET_NULL)
    email_checked = models.BooleanField(null=True)

    def __str__(self):
        return str(self.email)
