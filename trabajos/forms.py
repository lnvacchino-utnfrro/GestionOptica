from django.forms import ModelForm
from .models import Trabajo

class TrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        fields = '__all__'