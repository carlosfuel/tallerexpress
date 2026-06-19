from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import OrdenServicio
from .forms import OrdenServicioForm
 
 
def lista_ordenes(request):
    qs = OrdenServicio.objects.select_related(
        'cliente', 'vehiculo', 'mecanico')
    paginator = Paginator(qs, 10)               # 10 órdenes por página
    ordenes = paginator.get_page(request.GET.get('page'))
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes})
 
 
def crear_orden(request):
    if request.method == 'POST':                 # el usuario envió el formulario
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ordenes:lista')
    else:                                        # GET: mostrar el formulario vacío
        form = OrdenServicioForm()
    return render(request, 'ordenes/formulario.html',
                {'form': form, 'titulo': 'Nueva orden'})
 
 
def editar_orden(request, pk):
    orden = get_object_or_404(OrdenServicio, pk=pk)
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('ordenes:lista')
    else:
        form = OrdenServicioForm(instance=orden)
    return render(request, 'ordenes/formulario.html',
                {'form': form, 'titulo': f'Editar orden {orden.numero_orden}'})


def eliminar_orden(request, pk):
    orden = get_object_or_404(OrdenServicio, pk=pk)
    if request.method == 'POST':                 # llega solo si el usuario pulsó "Aceptar"
        orden.delete()
    return redirect('ordenes:lista')

