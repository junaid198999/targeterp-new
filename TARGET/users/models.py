from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ManyToManyField, OneToOneField, PROTECT, Model, ImageField, EmailField, \
    BooleanField, DateField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    email = EmailField(_('email address'), blank=False)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    permissions = ManyToManyField(Permission, related_name='users')
    thumb = ImageField(upload_to='users/', blank=True, null=True)
    picture = ImageField(upload_to='images/', max_length=255, blank=True, null=True)
    notification = BooleanField(default=1, verbose_name =_("Notifications"))
    tour = BooleanField(default=1, verbose_name =_("Tour"))
    darktheme = BooleanField(default=0, verbose_name =_("Dark Theme"))
    color = CharField(max_length=20, default='#0088cc', blank=True, null=True, verbose_name =_("Theme Color"))
    end_date = DateField(blank=True, null=True, verbose_name =_("Expiry Date"))

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def has_permission(self, codename):
        try:
            self.permissions.get(codename=codename)
        except Permission.DoesNotExist:
            return False
        else:
            return True

def get_perm_list(self):
    print(self.content_type.app_label)
    return "%s | %s" % (
        self.content_type,
        self.name,
    )
Permission.add_to_class("__str__", get_perm_list)