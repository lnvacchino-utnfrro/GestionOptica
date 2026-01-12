from typing import Any
from django.core.paginator import Paginator

from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.shortcuts import render
from django.urls import reverse_lazy

from trabajos.models import Trabajo

from .models import ObraSocial, Persona, Doctor, Lente

class DatosGeneralesHomeView(View):
    template_name = "datos_generales_home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# CRUD - OBRAS SOCIALES
class ObraSocialListView(ListView):
    model = ObraSocial
    template_name = "obra_social_list.html"


class ObraSocialCreateView(CreateView):
    model = ObraSocial
    fields = '__all__'
    template_name = 'obra_social_create_form.html'
    success_url = reverse_lazy('obra-social-list-view')


class ObraSocialUpdateView(UpdateView):
    model = ObraSocial
    fields = '__all__'
    template_name = "obra_social_update_form.html"
    success_url = reverse_lazy('obra-social-list-view')


class ObraSocialDeleteView(DeleteView):
    model = ObraSocial
    template_name = "obra_social_confirm_delete.html"
    success_url = reverse_lazy('obra-social-list-view')


# CRUD - PERSONAS
class PersonaListView(ListView):
    model = Persona
    template_name = "persona_list.html"
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET:
            context = self.request.GET
            if 'apellido' in context:
                apellido = context['apellido']
                queryset = Persona.objects.filter(apellido__contains=apellido)
            else:
                queryset = Persona.objects.all()
        else:
            queryset = Persona.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        # Llama primero a la implementación para traer un contexto
        context = super(PersonaListView, self).get_context_data(**kwargs)

        if self.request.GET:
            get_context = self.request.GET
            # Si se buscó el apellido, entonces agrego en el contexto el apellido
            if 'apellido' in get_context:
                context['buscar_apellido'] = get_context['apellido']

            # Genero el Paginator para devolver la página y los valores asociados
            if 'page' in get_context:
                queryset = self.get_queryset()
                paginator = Paginator(queryset, self.paginate_by)
                page_number = get_context.get('page')
                page_obj = paginator.get_page(page_number)
                context['page_obj'] = page_obj
                context['page_range'] = paginator.page_range

        return context


class PersonaDetailView(DetailView):
    model = Persona
    template_name = "persona_detail.html"
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super(PersonaDetailView, self).get_context_data(**kwargs)

        # Devuelvo el listado de trabajos de la persona
        persona = kwargs['object']
        trabajos = Trabajo.objects.filter(persona=persona).order_by('-fecha')
        context['trabajos'] = trabajos

        return context


class PersonaCreateView(CreateView):
    model = Persona
    fields = '__all__'
    template_name = 'persona_create_form.html'


class PersonaUpdateView(UpdateView):
    model = Persona
    fields = '__all__'
    template_name = "persona_update_form.html"


class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = "persona_confirm_delete.html"
    success_url = reverse_lazy('persona-list-view')


# CRUD - DOCTORES
class DoctorListView(ListView):
    model = Doctor
    template_name = "doctor_list.html"


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctor_detail.html"
    context_object_name = 'doctor'


class DoctorCreateView(CreateView):
    model = Doctor
    fields = '__all__'
    template_name = 'doctor_create_form.html'


class DoctorUpdateView(UpdateView):
    model = Doctor
    fields = '__all__'
    template_name = "doctor_update_form.html"


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = "doctor_confirm_delete.html"
    success_url = reverse_lazy('doctor-list-view')


# CRUD - LENTES
class LenteListView(ListView):
    model = Lente
    template_name = "lente_list.html"


class LenteCreateView(CreateView):
    model = Lente
    fields = '__all__'
    template_name = 'lente_create_form.html'
    success_url = reverse_lazy('lente-list-view')


class LenteUpdateView(UpdateView):
    model = Lente
    fields = '__all__'
    template_name = "lente_update_form.html"
    success_url = reverse_lazy('lente-list-view')


class LenteDeleteView(DeleteView):
    model = Lente
    template_name = "lente_confirm_delete.html"
    success_url = reverse_lazy('lente-list-view')

