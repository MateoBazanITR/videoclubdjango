"""
URLs raíz del proyecto "messi".
Redirige /admin/ al admin de Django e incluye todas las rutas
de la aplicación "core" en la raíz del sitio.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administración de Django
    path('', include('core.urls')),   # Todas las rutas de la app videoclub
]
