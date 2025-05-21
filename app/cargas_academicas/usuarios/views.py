from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.views.generic import TemplateView


from .token import token_activacion

from .forms import FormAlumno, FormUser
from materias.models import UnidadAcademica, ProgramaAcademico


class ActivarCuenta(TemplateView):

    def get(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)

        try:
            uid = urlsafe_base64_decode(kwargs['uidb64'])
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None

        if user is not None and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Cuenta activada, ingresar datos')
        else:
            messages.error(
                request, 'Token inválido, contacta al administrador')

        return render(request, 'login.html')


def nuevo_usuario(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False
            usuario.save()
            dominio = get_current_site(request)
            mensaje = render_to_string('confirmar_cuenta.html',
                                       {
                                           'user': usuario,
                                           'dominio': dominio,
                                           'uid': urlsafe_base64_encode(force_bytes(usuario.id)),
                                           'token': token_activacion.make_token(usuario)
                                       }
                                       )

            email = EmailMessage(
                'Activar cuenta ',
                mensaje,
                to=[usuario.email]
            )
            email.content_subtype = "html"
            email.send()
            messages.success(
                request, 'Se creo con éxito el usuario, verifica tu correo')
        else:
            messages.error(request, 'Verifica tu información')
    else:
        form = FormUser()
    context = {'form': form}
    return render(request, 'nuevo_usuario.html', context)


def lista_usuarios(request):
    usuarios = User.objects.all()
    grupos = Group.objects.all()
    if request.method == 'POST':
        print(request.POST)
        grupo = Group.objects.get(id=int(request.POST.get('grupos')))

        for item in request.POST:
            print(request.POST.get(item))
            if request.POST.get(item) == 'on':
                user = User.objects.get(id=item)
                user.groups.add(grupo)

    context = {
        'usuarios': usuarios,
        'grupos': grupos
    }
    return render(request, 'usuarios.html', context)


def obtener_programas(request, id):
    # unidad_academica = UnidadAcademica.object.get(id=id)
    # programas = ProgramaAcademico.objects.filter(unidad_academica=unidad_academica)
    try:
        programas = ProgramaAcademico.objects.filter(unidad_academica__id=id)
        data = [{'id': prog.id, 'nombre': prog.nombre} for prog in programas]
        return JsonResponse({'datos': data}, safe=False)
    except ProgramaAcademico.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron prorgramas'}, save=False)


class Login(LoginView):
    template_name = 'login.html'


def nuevo_alumno(request):
    unidades = UnidadAcademica.objects.all()
    form = FormAlumno()

    context = {
        'form': form,
        'unidades': unidades
    }
    return render(request, 'datos_alumno.html', context)
