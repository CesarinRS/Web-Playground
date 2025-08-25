from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    if instance.pk:  # Si ya existe, borra el anterior
        old_instance = Profile.objects.get(pk=instance.pk)
        if old_instance.avatar:
            old_instance.avatar.delete()
    return f'profiles/{instance.user.username}/{filename}'

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['user__username']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance,**kwargs):
    if kwargs.get('created'):
        Profile.objects.get_or_create(user=instance)
        #print("Se creo un usuario con su perfil enlazado correctamente")
