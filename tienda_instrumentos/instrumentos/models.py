from django.db import models
from django.contrib.auth.models import User

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class EspecificacionesTecnicas(models.Model):
    POTENCIA_MAX = 5000
    MATERIAL_TWEETER_CHOICES = [
        ("Seda", "Seda"),
        ("Aluminio", "Aluminio"),
        ("Berilio", "Berilio"),
        ("Titanio", "Titanio"),
        ("Fibra de carbono", "Fibra de carbono"),
    ]

    potencia_w = models.PositiveIntegerField("Potencia (W)")
    rango_frecuencia_min = models.PositiveIntegerField("Rango frecuencia mínima (Hz)")
    rango_frecuencia_max = models.PositiveIntegerField("Rango frecuencia máxima (Hz)")
    material_cono = models.CharField(max_length=50)
    material_tweeter = models.CharField(max_length=50, choices=MATERIAL_TWEETER_CHOICES)
    cantidad_entradas = models.PositiveIntegerField()
    peso_kg = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.potencia_w}W - {self.material_tweeter}"


class Monitor(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    modelo = models.CharField(max_length=100)
    precio_usd = models.PositiveIntegerField("Precio (USD)")
    especificaciones = models.OneToOneField(EspecificacionesTecnicas, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='monitores/', null=True, blank=True, verbose_name="Imagen del Monitor")
    def __str__(self):
        return f"{self.marca} {self.modelo}"