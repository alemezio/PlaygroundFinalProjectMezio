from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from AppProyecto.models import UserExtension, Blog, Chat, Mensaje
from AppProyecto.forms import FormularioRegistro, FormularioEditarPerfil, FormularioCambiarPassword, FormularioBuscarPosts, FormularioIniciarConversacion, FormularioEnvioMensaje

# Create your views here.

def inicio(request):
    return render(request, 'AppProyecto/index.html')

def about(request):
    return render(request, 'AppProyecto/about.html')


# --------------------------------
# VISTAS DE USUARIOS

def iniciar_sesion(request):
# Sólo permite el ingreso si NO se está logueado. Caso contrario, redirige a 'Inicio'
# Esta validación es útil cuando se intenta ingresar forzando la URL
    if request.user.is_authenticated:
        return redirect('Inicio')

    if request.method == 'POST':
        formulario_login = AuthenticationForm(request, data=request.POST)
        if formulario_login.is_valid():
            user = formulario_login.get_user()
            login(request, user)
            user_extension, es_nuevo_userextension = UserExtension.objects.get_or_create(user=request.user)
            return redirect('Inicio')
    else:
        formulario_login = AuthenticationForm()

    return render(request, 'AppProyecto/login.html', { 'formulario_login' : formulario_login })

def registrar_cuenta(request):
# Sólo permite el ingreso si NO se está logueado. Caso contrario, redirige a 'Inicio'
# Esta validación es útil cuando se intenta ingresar forzando la URL
    if request.user.is_authenticated:
        return redirect('Inicio')

    if request.method == 'POST':
        formulario_registro = FormularioRegistro(request.POST)
        if formulario_registro.is_valid():
            formulario_registro.save()
            return redirect('Inicio')
    else:
        formulario_registro = FormularioRegistro()

    return render(request, 'AppProyecto/registrar.html', { 'formulario_registro' : formulario_registro })

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('Inicio')

@login_required
def ver_perfil(request):
    return render(request, 'AppProyecto/perfil.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        formulario_editar_perfil = FormularioEditarPerfil(request.POST, request.FILES)
        if formulario_editar_perfil.is_valid():
            datos_perfil = formulario_editar_perfil.cleaned_data
            request.user.email = datos_perfil['email']
            request.user.first_name = datos_perfil['first_name']
            request.user.last_name = datos_perfil['last_name']
# En caso de blanquearse el avatar, el mismo se guardará vacío.
# En caso de cambiarlo, este será actualizado. De lo contrario, se mantendrá la imagen anterior
            if datos_perfil['avatar'] == False:
                request.user.userextension.avatar = None
            elif datos_perfil['avatar'] != None:
                request.user.userextension.avatar = datos_perfil['avatar']

            request.user.userextension.descripcion = datos_perfil['descripcion']
            request.user.userextension.link = datos_perfil['link']

            request.user.save()
            request.user.userextension.save()

            return redirect('Ver_perfil')
    else:
        formulario_editar_perfil = FormularioEditarPerfil(
            initial={
                'email' : request.user.email,
                'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'avatar' : request.user.userextension.avatar,
                'descripcion' : request.user.userextension.descripcion,
                'link' : request.user.userextension.link,
            }
        )

    return render(request, 'AppProyecto/editar_perfil.html', { 'formulario_editar_perfil' : formulario_editar_perfil })

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        formulario_cambio_password = FormularioCambiarPassword(user=request.user, data=request.POST)

        if formulario_cambio_password.is_valid():
            formulario_cambio_password.save()
            update_session_auth_hash(request, request.user)
            return redirect('Ver_perfil')
    else:
        formulario_cambio_password = FormularioCambiarPassword(user=request.user)

    return render(request, 'AppProyecto/cambiar_password.html', { 'formulario_cambio_password' : formulario_cambio_password })


# --------------------------------
# VISTAS DE POSTEOS

'''
    VISTAS BASADAS EN FUNCIONES:
    -    Ver posts: Muestro TODOS las paginas creadas por los usuarios
    - Buscar posts: Filtro paginas por titulo
'''
def ver_posts(request):
    posts = Blog.objects.all().order_by('id')
    return render(request, 'AppProyecto/ver_posts.html', { 'posts' : posts })


def buscar_posts(request):
    titulo = request.GET.get('titulo', None)

    if titulo:
        posts = Blog.objects.filter(titulo__icontains=titulo)
    else:
        posts = Blog.objects.all()

    posts = posts.order_by('id')

    formulario_buscar_posts = FormularioBuscarPosts()

    return render(request, 'AppProyecto/buscar_posts.html', { 'formulario_buscar_posts' : formulario_buscar_posts, 'posts' : posts })

'''
    CLASES BASADAS EN VISTAS (CBV):
    -    Ver: VerPostView
    -  Crear: NuevoPostView
    - Editar: EditarPostView
    - Borrar: EliminarPostView
'''
class VerPostView(DetailView):
    model         = Blog
    template_name = 'AppProyecto/ver_post.html'


class NuevoPostView(LoginRequiredMixin, CreateView):
    model         = Blog
    template_name = 'AppProyecto/crear_post.html'
    success_url   = reverse_lazy('Ver_posts')
    fields        = ['titulo', 'subtitulo', 'cuerpo', 'imagen']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarPostView(LoginRequiredMixin, UpdateView):
    model         = Blog
    template_name = 'AppProyecto/editar_post.html'
    success_url   = reverse_lazy('Ver_posts')
    fields        = ['titulo', 'subtitulo', 'cuerpo', 'imagen']


class EliminarPostView(LoginRequiredMixin, DeleteView):
    model         = Blog
    template_name = 'AppProyecto/borrar_post.html'
    success_url   = reverse_lazy('Ver_posts')


# ---------------------------
# VISTAS DE MENSAJERIA ENTRE USUARIOS

'''
    VISTAS BASADAS EN FUNCIONES:
    -    Ver chats: Muestro TODAS las conversaciones iniciadas con usuarios
    -     Ver chat: Muestro la conversacion iniciada con un usuario
    - Iniciar chat: Inicia una nueva conversacion con el usuario seleccionado
    - Eliminar chat: Elimina un chat determinado
'''
@login_required
def ver_chats(request):
# Búsqueda de TODAS las conversaciones recibidas e iniciadas por el usuario
    chats = Chat.objects.all().filter(user_chat_2=request.user).union(
            Chat.objects.all().filter(user_chat_1=request.user)
    ).order_by('id')

    return render(request, 'AppProyecto/ver_chats.html', { 'chats' : chats })


@login_required
def iniciar_chat(request):

# Esta vista permite el inicio de una nueva conversación con el usuario seleccionado
    if request.method == 'POST':
        formulario_iniciar_chat = FormularioIniciarConversacion(request.POST)

        chat_user = formulario_iniciar_chat.data.get('user_chat_2')

        nuevo_chat = Chat(
            user_chat_1 = request.user,
            user_chat_2 = User.objects.get(username=chat_user)
        )

        nuevo_chat.save()

        return redirect('Ver_chat', nuevo_chat.id)
    else:
# Búsqueda de TODAS las conversaciones recibidas e iniciadas por el usuario
# Obtengo un QuerySet más pequeño, con los usuarios con chats activos
        try:
            qs_chats = Chat.objects.all().filter(user_chat_2=request.user).values_list('user_chat_1', flat=True).union(
                        Chat.objects.all().filter(user_chat_1=request.user).values_list('user_chat_2', flat=True)
            )

# Filtro usuarios 'staff' y con chats activos
# Disponibiliza SÓLO aquellos usuarios con los que puedo iniciar una conversación
            qs_users = User.objects.all().filter(is_staff=False).exclude(username=request.user.username).exclude(pk__in=qs_chats)

            qs_users = qs_users.order_by('username')
        except:
            qs_users = User.objects.none()

        formulario_iniciar_chat = FormularioIniciarConversacion()

        formulario_iniciar_chat.fields['user_chat_2'].queryset = qs_users

    return render(request, 'AppProyecto/iniciar_chat.html', { 'formulario_iniciar_chat' : formulario_iniciar_chat })


@login_required
def ver_chat(request, id):

# Búsqueda de los datos de la conversación
    chat = Chat.objects.get(id=id)

    mensajes = None

# Esta vista disponibiliza la conversación con el usuario, y permite enviar un nuevo mensaje
    if request.method == 'POST':
        formulario_envio_mensaje = FormularioEnvioMensaje(request.POST)

        if formulario_envio_mensaje.is_valid():
            datos_mensaje = formulario_envio_mensaje.cleaned_data

            nuevo_mensaje = Mensaje(
                chat = chat,
                de_user = request.user,
                contenido = datos_mensaje['contenido']
            )

            nuevo_mensaje.save()
            return redirect('Ver_chat', chat.id)
    else:
        mensajes = Mensaje.objects.filter(chat=chat).order_by('id')

        formulario_envio_mensaje = FormularioEnvioMensaje()

    return render(request, 'AppProyecto/ver_chat.html', { 'formulario_envio_mensaje' : formulario_envio_mensaje, 'chat' : chat, 'mensajes' : mensajes })

'''
    CLASES BASADAS EN VISTAS (CBV):
    - Borrar: EliminarChatView
'''
class EliminarChatView(LoginRequiredMixin, DeleteView):
    model         = Chat
    template_name = 'AppProyecto/borrar_chat.html'
    success_url   = reverse_lazy('Ver_chats')
