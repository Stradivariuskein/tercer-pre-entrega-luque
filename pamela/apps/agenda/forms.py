from django import forms
from .models import TypeSession
from apps.login.models import Acount

class SearchForm(forms.Form):
    day_choices = [
        ('', 'Seleccione un día'),
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    
    day_of_week = forms.ChoiceField(label="Dia",choices=day_choices, required=False)
    date = forms.DateField(label="Desde", required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class TypeSessionForm(forms.ModelForm):
    remote = forms.BooleanField(label="Sesión remota")
    in_group = forms.BooleanField(label="En grupo")
    social_rounds = forms.BooleanField(label="Obra social")
    price = forms.IntegerField(label="Precio")
    
    class Meta:
        model = TypeSession
        fields = ['remote', 'in_group', 'social_rounds', 'price']


class AcountSearchForm(forms.Form):
    name = forms.CharField(max_length=50, label="Nombre")


