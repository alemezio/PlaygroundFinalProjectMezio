from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

'''
    MODELO 'UserExtension':
    - user: Relación 1 a 1 con modelo 'User'
    - descripcion: str
    - link: str
    - avatar: file
'''
class UserExtension(models.Model):

    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, null=True)
    link        = models.URLField(max_length=100, null=True)
    avatar      = models.ImageField(upload_to='avatares/', null=True, blank=True)

'''
    MODELO 'Blog':
    - titulo: str
    - subtitulo: str
    - cuerpo: RichText (ckeditor)
    - autor: str
    - fecha_creado: date
    - imagen: file
'''
class Blog(models.Model):

    titulo         = models.CharField(max_length=255)
    subtitulo      = models.CharField(max_length=255)
    cuerpo         = RichTextField(null=True)
    # cuerpo         = models.TextField(null=True, blank=True)
    autor          = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creado   = models.DateField(auto_now_add=True, auto_now=False)
    imagen         = models.ImageField(upload_to='galeria/')

'''
    MODELO 'Chat':
    - user_chat_1: str
    - user_chat_2: str
    - fecha_creacion: date
'''
class Chat(models.Model):

    user_chat_1    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user_1')
    user_chat_2    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user_2')
    fecha_creacion = models.DateField(auto_now=False, auto_now_add=True)

'''
    MODELO 'Mensaje'
    - id_chat: int (id -> Chat)
    - contenido: str
    - fecha_hora: datetime
'''
class Mensaje(models.Model):

    chat       = models.ForeignKey(Chat, on_delete=models.CASCADE)
    de_user    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contenido  = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True, auto_now=False)




