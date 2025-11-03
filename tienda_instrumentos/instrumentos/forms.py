from django import forms
from .models import Monitor, EspecificacionesTecnicas, Marca, Categoria

MODELOS_POR_MARCA = {
    'Yamaha': [
        ('HS5', 'HS5'),
        ('HS7', 'HS7'),
        ('HS8', 'HS8'),
        ('HS50M', 'HS50M'),
    ],
    'Genelec': [
        ('8020D', '8020D'),
        ('8030C', '8030C'),
        ('8040B', '8040B'),
        ('8050B', '8050B'),
    ],
    'Focal': [
        ('Alpha 50 Evo', 'Alpha 50 Evo'),
        ('Alpha 65 Evo', 'Alpha 65 Evo'),
        ('Solo6 Be', 'Solo6 Be'),
        ('Twin6 Be', 'Twin6 Be'),
    ],
    'ADAM Audio': [
        ('T5V', 'T5V'),
        ('T7V', 'T7V'),
        ('A7X', 'A7X'),
        ('S2V', 'S2V'),
    ],
    'Neumann': [
        ('KH 80 DSP', 'KH 80 DSP'),
        ('KH 120 II', 'KH 120 II'),
        ('KH 310', 'KH 310'),
    ],
    'KRK': [
        ('Rokit 5 G4', 'Rokit 5 G4'),
        ('Rokit 7 G4', 'Rokit 7 G4'),
        ('Classic 5', 'Classic 5'),
        ('V8 S4', 'V8 S4'),
    ],
    'PreSonus': [
        ('Eris E5 XT', 'Eris E5 XT'),
        ('Eris E8 XT', 'Eris E8 XT'),
        ('R65', 'R65'),
    ],
    'JBL Professional': [
        ('305P MkII', '305P MkII'),
        ('308P MkII', '308P MkII'),
        ('4309', '4309'),
    ],
}

NOMBRES_POR_MARCA = {
    'Yamaha': [
        ('HS Series', 'HS Series'),
        ('MSP Series', 'MSP Series'),
    ],
    'Genelec': [
        ('8000 Series', '8000 Series'),
        ('The Ones', 'The Ones'),
    ],
    'Focal': [
        ('Alpha Evo', 'Alpha Evo'),
        ('Solo/Twin', 'Solo/Twin'),
        ('Shape', 'Shape'),
    ],
    'ADAM Audio': [
        ('T Series', 'T Series'),
        ('A Series', 'A Series'),
        ('S Series', 'S Series'),
    ],
    'Neumann': [
        ('KH Series', 'KH Series'),
    ],
    'KRK': [
        ('Rokit', 'Rokit'),
        ('Classic', 'Classic'),
        ('V Series', 'V Series'),
    ],
    'PreSonus': [
        ('Eris', 'Eris'),
        ('R Series', 'R Series'),
    ],
    'JBL Professional': [
        ('3 Series', '3 Series'),
        ('4 Series', '4 Series'),
    ],
}


class MonitorForm(forms.ModelForm):
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        empty_label="Seleccione una marca",
        widget=forms.Select(attrs={
            'onchange': 'actualizarNombresYModelos()',
            'id': 'id_marca'
        })
    )

    nombre = forms.CharField(
        max_length=100,
        widget=forms.Select(attrs={
            'id': 'id_nombre',
            'onchange': 'actualizarModelos()'
        }),
        label="Nombre/Serie"
    )

    modelo = forms.CharField(
        max_length=100,
        widget=forms.Select(attrs={'id': 'id_modelo'}),
        label="Modelo"
    )

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Seleccione una categoría"
    )

    precio_usd = forms.IntegerField(
        min_value=0,
        label="Precio (USD)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Precio en USD',
            'step': '1'
        })
    )

    class Meta:
        model = Monitor
        fields = ["marca", "nombre", "modelo", "categoria", "precio_usd"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.choices = [('', 'Primero seleccione una marca')]
        self.fields['modelo'].widget.choices = [('', 'Primero seleccione una marca')]

        if self.instance.pk and self.instance.marca:
            marca_nombre = self.instance.marca.nombre
            if marca_nombre in NOMBRES_POR_MARCA:
                self.fields['nombre'].widget.choices = [('', 'Seleccione un nombre')] + NOMBRES_POR_MARCA[marca_nombre]
            if marca_nombre in MODELOS_POR_MARCA:
                self.fields['modelo'].widget.choices = [('', 'Seleccione un modelo')] + MODELOS_POR_MARCA[marca_nombre]

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        marca = self.cleaned_data.get('marca')

        if not nombre:
            raise forms.ValidationError("Debe seleccionar un nombre/serie.")

        if marca and marca.nombre in NOMBRES_POR_MARCA:
            nombres_validos = [n[0] for n in NOMBRES_POR_MARCA[marca.nombre]]
            if nombre not in nombres_validos:
                raise forms.ValidationError(f"El nombre '{nombre}' no es válido para la marca {marca.nombre}.")

        return nombre

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        marca = self.cleaned_data.get('marca')

        if not modelo:
            raise forms.ValidationError("Debe seleccionar un modelo.")

        if marca and marca.nombre in MODELOS_POR_MARCA:
            modelos_validos = [m[0] for m in MODELOS_POR_MARCA[marca.nombre]]
            if modelo not in modelos_validos:
                raise forms.ValidationError(f"El modelo '{modelo}' no es válido para la marca {marca.nombre}.")

        return modelo


class EspecificacionesTecnicasForm(forms.ModelForm):
    potencia_w = forms.IntegerField(
        min_value=0,
        label="Potencia (W)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Potencia en Watts',
            'step': '1'
        })
    )

    rango_frecuencia_min = forms.IntegerField(
        min_value=0,
        label="Rango frecuencia mínima (Hz)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Frecuencia mínima en Hz',
            'step': '1'
        })
    )

    rango_frecuencia_max = forms.IntegerField(
        min_value=0,
        label="Rango frecuencia máxima (Hz)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Frecuencia máxima en Hz',
            'step': '1'
        })
    )

    material_cono = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Kevlar, Polipropileno, etc.'
        })
    )

    cantidad_entradas = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Número de entradas',
            'step': '1'
        })
    )

    peso_kg = forms.IntegerField(
        min_value=0,
        label="Peso (kg)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Peso en kg',
            'step': '1'
        })
    )

    imagen = forms.ImageField(
        required=False,
        label="Imagen del Monitor",
        widget=forms.FileInput(attrs={
            'accept': 'image/*'
        })
    )

    class Meta:
        model = EspecificacionesTecnicas
        fields = [
            'potencia_w',
            'rango_frecuencia_min',
            'rango_frecuencia_max',
            'material_cono',
            'material_tweeter',
            'cantidad_entradas',
            'peso_kg'
        ]

    def clean(self):
        cleaned_data = super().clean()
        min_f = cleaned_data.get("rango_frecuencia_min")
        max_f = cleaned_data.get("rango_frecuencia_max")
        if min_f and max_f and min_f >= max_f:
            raise forms.ValidationError("El rango de frecuencia mínima debe ser menor que la máxima.")
        return cleaned_data