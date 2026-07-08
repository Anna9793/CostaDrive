from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    path(
        "eliminar/<int:deptno>/",
        views.eliminar_departamento,
        name="eliminar"
    ),

    path(
        "editar/<int:deptno>/",
        views.editar_departamento,
        name="editar"
    ),

    path(
        "nuevo/",
        views.nuevo_departamento,
        name="nuevo"
    ),
]