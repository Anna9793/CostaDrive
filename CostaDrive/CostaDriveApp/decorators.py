from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def group_required(*group_names):
    """
    Decorador para proteger vistas basado en el grupo de pertenencia del usuario.
    El rol de Manager siempre tiene acceso completo.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # El grupo Manager o los superusuarios siempre tienen acceso a todo
            if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            # Verificar si pertenece a alguno de los grupos permitidos
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
                
            # Redireccionar según los accesos disponibles si el usuario no tiene permisos
            messages.error(request, "Acceso denegado: no dispones de los permisos necesarios para realizar esta acción.")
            
            if request.user.groups.filter(name='Client').exists():
                return redirect('client_dashboard')
            elif request.user.groups.filter(name='Maintenance').exists():
                return redirect('listar_vehiculos')
            else:
                return redirect('dashboard')
                
        return _wrapped_view
    return decorator

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

def db_action(success_message=None, fallback_url=None):
    """
    Decorador para simplificar try/except en operaciones de base de datos
    dentro de vistas Django, mostrando alertas de éxito y error y gestionando redirecciones.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                response = view_func(request, *args, **kwargs)
                if success_message and isinstance(response, (HttpResponseRedirect, HttpResponsePermanentRedirect)):
                    messages.success(request, success_message)
                return response
            except Exception as e:
                messages.error(request, f"Error en la operación: {e}")
                if fallback_url:
                    return redirect(fallback_url)
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return redirect(referer)
                return redirect('dashboard')
        return wrapper
    return decorator
