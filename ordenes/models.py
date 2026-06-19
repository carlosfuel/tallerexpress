from django.db import models 
from django.core.validators import RegexValidator 


class Cliente(models.Model): 
    cedula = models.CharField( 
        max_length=10, unique=True, 
        validators=[RegexValidator(r'^\d{6,10}$', 
                    'La cédula debe tener entre 6 y 10 dígitos.')]) 
    nombre = models.CharField(max_length=120) 
    telefono = models.CharField( 
        max_length=15, 
        validators=[RegexValidator(r'^\d{7,10}$', 
                    'El teléfono debe tener entre 7 y 10 dígitos.')]) 

    class Meta: 
        db_table = 'cliente' 

    def __str__(self): 
        return f"{self.nombre} ({self.cedula})" 
    

class Vehiculo(models.Model): 
    placa = models.CharField( 
        max_length=6, unique=True, 
        validators=[RegexValidator(r'^[A-Z]{3}\d{3}$', 
                    'Formato de placa inválido. Ejemplo: ABC123.')]) 
    marca = models.CharField(max_length=50) 
    modelo = models.CharField(max_length=50) 
    kilometraje = models.PositiveIntegerField(default=0)
    cliente = models.ForeignKey( 
        Cliente, on_delete=models.PROTECT, related_name='vehiculos') 
  
    class Meta: 
        db_table = 'vehiculo' 
  
    def __str__(self): 
        return f"{self.placa} - {self.marca} {self.modelo}" 
    
class Mecanico(models.Model): 
    nombre = models.CharField(max_length=120) 
    especialidad = models.CharField(max_length=60, blank=True) 
    activo = models.BooleanField(default=True) 
  
    class Meta: 
        db_table = 'mecanico' 
  
    def __str__(self): 
        return self.nombre
    
class OrdenServicio(models.Model): 
    class Estado(models.TextChoices): 
        RECIBIDA = 'RECIBIDA', 'Recibida' 
        EN_DIAGNOSTICO = 'EN_DIAGNOSTICO', 'En diagnóstico' 
        COTIZADA = 'COTIZADA', 'Cotizada' 
        EN_EJECUCION = 'EN_EJECUCION', 'En ejecución' 
        LISTA = 'LISTA', 'Lista' 
        ENTREGADA = 'ENTREGADA', 'Entregada' 
        CERRADA_SIN_SERVICIO = 'CERRADA_SIN_SERVICIO', 'Cerrada sin servicio' 
  
    numero_orden = models.CharField(max_length=10, unique=True, editable=False) 
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT) 
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT) 
    mecanico = models.ForeignKey( 
        Mecanico, on_delete=models.SET_NULL, null=True, blank=True) 
    descripcion_problema = models.TextField() 
    estado = models.CharField( 
        max_length=25, choices=Estado.choices, default=Estado.RECIBIDA) 
    fecha_ingreso = models.DateTimeField(auto_now_add=True) 
    fecha_actualizacion = models.DateTimeField(auto_now=True) 
  
    class Meta: 
        ordering = ['-fecha_actualizacion'] 
        db_table = 'orden_servicio'

    def save(self, *args, **kwargs): 
        # Genera el consecutivo OS-001, OS-002... la primera vez (RF-03). 
        # Lee la última orden, le suma 1 y reformatea con relleno a 3 dígitos. 
        if not self.numero_orden: 
            ultima = OrdenServicio.objects.order_by('-id').first() 
            n = (int(ultima.numero_orden.split('-')[1]) + 1) if ultima else 1
            self.numero_orden = f"OS-{n:03d}" 
        super().save(*args, **kwargs) 
  
    def __str__(self): 
        return f"{self.numero_orden} - {self.vehiculo.placa}" 

