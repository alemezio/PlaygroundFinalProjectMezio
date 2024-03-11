from django.contrib import admin
from AppProyecto import models

# Register your models here.
admin.site.register(models.UserExtension)
admin.site.register(models.Blog)
admin.site.register(models.Chat)
admin.site.register(models.Mensaje)