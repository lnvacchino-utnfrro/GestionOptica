from django.forms import Form, ModelForm, ModelMultipleChoiceField
from base.models import Doctor, Lente, Tratamiento, Armazon, ObraSocial
from .models import Trabajo


class TrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        fields = '__all__'


class TrabajoFilterForm(Form):
    doctor = ModelMultipleChoiceField(queryset=Doctor.objects.all())
    lente = ModelMultipleChoiceField(queryset=Lente.objects.all())
    armazon = ModelMultipleChoiceField(queryset=Armazon.objects.all())
    tratamiento = ModelMultipleChoiceField(queryset=Tratamiento.objects.all())
    obraSocial = ModelMultipleChoiceField(queryset=ObraSocial.objects.all())
