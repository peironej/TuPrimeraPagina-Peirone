
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import MODELOS_POR_MARCA, NOMBRES_POR_MARCA, MonitorForm, EspecificacionesTecnicasForm
from .models import Marca, Monitor
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

def inicio(request):
    monitores = Monitor.objects.all()
    return render(request, "instrumentos/inicio.html", {"monitores": monitores})

@user_passes_test(lambda u: u.is_superuser)
def agregar_monitor(request):
    if request.method == "POST":
        form_especificaciones = EspecificacionesTecnicasForm(request.POST)
        form_monitor = MonitorForm(request.POST, request.FILES)  # Agregar request.FILES

        if form_especificaciones.is_valid() and form_monitor.is_valid():
            especificaciones = form_especificaciones.save()
            monitor = form_monitor.save(commit=False)
            monitor.especificaciones = especificaciones
            monitor.creado_por = request.user
            monitor.save()
            return redirect("inicio")
    else:
        form_especificaciones = EspecificacionesTecnicasForm()
        form_monitor = MonitorForm()

    nombres_por_marca_id = {}
    modelos_por_marca_id = {}

    for marca in Marca.objects.all():
        if marca.nombre in NOMBRES_POR_MARCA:
            nombres_por_marca_id[str(marca.id)] = NOMBRES_POR_MARCA[marca.nombre]
        if marca.nombre in MODELOS_POR_MARCA:
            modelos_por_marca_id[str(marca.id)] = MODELOS_POR_MARCA[marca.nombre]

    nombres_json = json.dumps(nombres_por_marca_id)
    modelos_json = json.dumps(modelos_por_marca_id)

    return render(
        request,
        "instrumentos/agregar_monitor.html",
        {
            "monitor_form": form_monitor,
            "especificaciones_form": form_especificaciones,
            "nombres_json": nombres_json,
            "modelos_json": modelos_json,
        },
    )

def buscar_monitor(request):
    query = request.GET.get("q")
    resultados = []
    if query:
        resultados = Monitor.objects.filter(
            Q(modelo__icontains=query) | Q(marca__nombre__icontains=query)
        )
    return render(request, "instrumentos/buscar_monitor.html", {"resultados": resultados, "query": query})

def comparar_monitores(request):
    monitores = Monitor.objects.all()
    monitor1_id = request.GET.get("m1")
    monitor2_id = request.GET.get("m2")
    monitor1 = Monitor.objects.filter(id=monitor1_id).first()
    monitor2 = Monitor.objects.filter(id=monitor2_id).first()
    return render(request, "instrumentos/comparar.html", {
        "monitores": monitores,
        "monitor1": monitor1,
        "monitor2": monitor2,
    })

@login_required
def comprar_monitor(request, monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    return render(request, "instrumentos/compra_exitosa.html", {"monitor": monitor})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'instrumentos/registro.html', {'form': form})

@login_required
def detalle_monitor(request, monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    return render(request, 'instrumentos/detalle_monitor.html', {'monitor': monitor})