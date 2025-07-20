from django.urls import path
from . import views
# Define la ruta principal del formulario
urlpatterns = [
    path('', views.formulario_view, name='formulario_view'),
]
