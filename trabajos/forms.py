from django.forms import Form, ModelForm, ModelMultipleChoiceField, ModelChoiceField, inlineformset_factory, Select
from base.models import Doctor, Lente, Tratamiento, Armazon, ObraSocial
from .models import Trabajo, TrabajoArmazon, TrabajoLente, TrabajoMaterial, TrabajoTratamiento

class TrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        exclude = [
            'lentes',
            'tratamientos',
            'armazones',
            'materiales',
        ]


class TrabajoFilterForm(Form):
    doctor = ModelChoiceField(queryset=Doctor.objects.all())
    lente = ModelMultipleChoiceField(queryset=Lente.objects.all())
    armazon = ModelMultipleChoiceField(queryset=Armazon.objects.all())
    tratamiento = ModelMultipleChoiceField(queryset=Tratamiento.objects.all())
    obraSocial = ModelMultipleChoiceField(queryset=ObraSocial.objects.all())


class TrabajoLenteForm(ModelForm):
    class Meta:
        model = TrabajoLente
        fields = ['lente']
        widgets = {
            'lente': Select(attrs={'class': 'form-select'}),
        }

    tipo_fijo = None  # se define en subclases

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = self.tipo_fijo
        if commit:
            obj.save()
        return obj


class TrabajoLenteCercaForm(TrabajoLenteForm):
    tipo_fijo = 'CERCA'


class TrabajoLenteLejosForm(TrabajoLenteForm):
    tipo_fijo = 'LEJOS'


class TrabajoLenteUnicoForm(TrabajoLenteForm):
    tipo_fijo = 'UNICO'


class TrabajoTratamientoForm(ModelForm):
    class Meta:
        model = TrabajoTratamiento
        fields = ['tratamiento']
        widgets = {
            'tratamiento': Select(attrs={'class': 'form-select'}),
        }

    tipo_fijo = None  # se define en subclases

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = self.tipo_fijo
        if commit:
            obj.save()
        return obj


class TrabajoTratamientoCercaForm(TrabajoTratamientoForm):
    tipo_fijo = 'CERCA'


class TrabajoTratamientoLejosForm(TrabajoTratamientoForm):
    tipo_fijo = 'LEJOS'


class TrabajoTratamientoUnicoForm(TrabajoTratamientoForm):
    tipo_fijo = 'UNICO'


class TrabajoArmazonForm(ModelForm):
    class Meta:
        model = TrabajoArmazon
        fields = ['armazon']
        widgets = {
            'armazon': Select(attrs={'class': 'form-select'}),
        }

    tipo_fijo = None  # se define en subclases

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = self.tipo_fijo
        if commit:
            obj.save()
        return obj


class TrabajoArmazonCercaForm(TrabajoArmazonForm):
    tipo_fijo = 'CERCA'


class TrabajoArmazonLejosForm(TrabajoArmazonForm):
    tipo_fijo = 'LEJOS'


class TrabajoArmazonUnicoForm(TrabajoArmazonForm):
    tipo_fijo = 'UNICO'


class TrabajoMaterialForm(ModelForm):
    class Meta:
        model = TrabajoMaterial
        fields = ['material']
        widgets = {
            'material': Select(attrs={'class': 'form-select'}),
        }

    tipo_fijo = None  # se define en subclases

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = self.tipo_fijo
        if commit:
            obj.save()
        return obj


class TrabajoMaterialCercaForm(TrabajoMaterialForm):
    tipo_fijo = 'CERCA'


class TrabajoMaterialLejosForm(TrabajoMaterialForm):
    tipo_fijo = 'LEJOS'


class TrabajoMaterialUnicoForm(TrabajoMaterialForm):
    tipo_fijo = 'UNICO'


TrabajoLenteCercaFormSet = inlineformset_factory(
    Trabajo,
    TrabajoLente,
    form=TrabajoLenteCercaForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoLenteLejosFormSet = inlineformset_factory(
    Trabajo,
    TrabajoLente,
    form=TrabajoLenteLejosForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoLenteUnicoFormSet = inlineformset_factory(
    Trabajo,
    TrabajoLente,
    form=TrabajoLenteUnicoForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoTratamientoCercaFormSet = inlineformset_factory(
    Trabajo,
    TrabajoTratamiento,
    form=TrabajoTratamientoCercaForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoTratamientoLejosFormSet = inlineformset_factory(
    Trabajo,
    TrabajoTratamiento,
    form=TrabajoTratamientoLejosForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoTratamientoUnicoFormSet = inlineformset_factory(
    Trabajo,
    TrabajoTratamiento,
    form=TrabajoTratamientoUnicoForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoArmazonCercaFormSet = inlineformset_factory(
    Trabajo,
    TrabajoArmazon,
    form=TrabajoArmazonCercaForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoArmazonLejosFormSet = inlineformset_factory(
    Trabajo,
    TrabajoArmazon,
    form=TrabajoArmazonLejosForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoArmazonUnicoFormSet = inlineformset_factory(
    Trabajo,
    TrabajoArmazon,
    form=TrabajoArmazonUnicoForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoMaterialCercaFormSet = inlineformset_factory(
    Trabajo,
    TrabajoMaterial,
    form=TrabajoMaterialCercaForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoMaterialLejosFormSet = inlineformset_factory(
    Trabajo,
    TrabajoMaterial,
    form=TrabajoMaterialLejosForm,
    extra=1,
    max_num=1,
    can_delete=True
)

TrabajoMaterialUnicoFormSet = inlineformset_factory(
    Trabajo,
    TrabajoMaterial,
    form=TrabajoMaterialUnicoForm,
    extra=1,
    max_num=1,
    can_delete=True
)
