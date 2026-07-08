from django.shortcuts import render, redirect
from .models import ModelDepartamentos

def index(request):
    model = ModelDepartamentos()
    departamentos = model.get_departamentos_db()

    return render(
        request,
        "index.html",
        {"departamentos": departamentos}
    )

def eliminar_departamento(request, deptno):
    
    model = ModelDepartamentos()
    model.eliminar_departamento_db(deptno)

    return redirect("index")

def editar_departamento(request, deptno):

    model = ModelDepartamentos()

    if request.method == "POST":

        nombre = request.POST["nombre"]
        loc = request.POST["loc"]

        model.modificar_departamento_db(
            deptno,
            nombre,
            loc
        )

        return redirect("index")

    departamento = model.get_departamento_db(deptno)

    return render(
        request,
        "editar.html",
        {"departamento": departamento}
    )

def nuevo_departamento(request):

    model = ModelDepartamentos()

    if request.method == "POST":

        deptno = request.POST["deptno"]
        nombre = request.POST["nombre"]
        loc = request.POST["loc"]

        model.insertar_departamento_db(
            deptno,
            nombre,
            loc
        )

        return redirect("index")

    return render(request, 'nuevo.html')
