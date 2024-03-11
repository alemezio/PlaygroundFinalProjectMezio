from django.urls import path
from AppProyecto import views

urlpatterns = [
    path('', views.inicio,name="Inicio"),
    path('about/', views.about, name='About'),
    path('accounts/login/', views.iniciar_sesion, name='Login'),
    path('accounts/signup/', views.registrar_cuenta, name='Registrar'),
    path('accounts/logout/', views.cerrar_sesion, name='Logout'),
    path('accounts/profile/', views.ver_perfil, name='Ver_perfil'),
    path('accounts/editar/', views.editar_perfil, name='Editar_perfil'),
    path('accounts/cambiar-password/', views.cambiar_password, name='Cambiar_password'),

    path('pages/', views.ver_posts, name='Ver_posts'),
    path('pages/<int:pk>', views.VerPostView.as_view(), name='Ver_post'),
    path('pages/buscar/', views.buscar_posts, name='Buscar_posts'),
    path('pages/nuevo/', views.NuevoPostView.as_view(), name='Nuevo_post'),
    path('pages/<int:pk>/editar/', views.EditarPostView.as_view(), name='Editar_post'),
    path('pages/<int:pk>/eliminar/', views.EliminarPostView.as_view(), name='Borrar_post'),

    path('messages/', views.ver_chats, name='Ver_chats'),
    path('messages/nuevo/', views.iniciar_chat, name='Nuevo_chat'),
    path('messages/<int:id>/', views.ver_chat, name='Ver_chat'),
    path('messages/<int:pk>/eliminar/', views.EliminarChatView.as_view(), name='Borrar_chat'),

]