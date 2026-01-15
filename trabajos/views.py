from django.core.paginator import Paginator

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from base.models import *
from trabajos.forms import *
from trabajos.models import Trabajo, TrabajoLente, TIPO_TRABAJO

class TrabajosHomeView(View):
    template_name = "trabajos_home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# CRUD - TRABAJOS
class TrabajoListView(View):
    form_class = TrabajoFilterForm
    template_name = "trabajo_list.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={})
        trabajos = Trabajo.objects.all()
        filtro_avanzado = False
        context = {'form':form}
        if request.GET.get('fecha_desde'):
            trabajos = Trabajo.objects.filter(fecha_receta__gt=request.GET.get('fecha_desde'))
            context['filtro_fecha_desde'] = request.GET.get('fecha_desde')
        if request.GET.get('fecha_hasta'):
            trabajos = Trabajo.objects.filter(fecha_receta__lt=request.GET.get('fecha_hasta'))
            context['filtro_fecha_hasta'] = request.GET.get('fecha_hasta')
        if request.GET.get('apellido'):
            trabajos = Trabajo.objects.filter(persona__in=Persona.objects.filter(apellido__icontains=request.GET.get('apellido')))
            context['filtro_apellido'] = request.GET.get('apellido')
            filtro_avanzado = True
        if request.GET.get('nombre'):
            inner_personas = Persona.objects.filter(nombre__icontains=request.GET.get('nombre')).values('id')
            trabajos = Trabajo.objects.filter(persona__in=inner_personas)
            context['filtro_nombre'] = request.GET.get('nombre')
            filtro_avanzado = True
        if request.GET.get('doctor'):
            inner_doctores = Doctor.objects.filter(apellido__icontains=request.GET.get('doctor')).union(
                Doctor.objects.filter(nombre__icontains=request.GET.get('doctor'))
            ).values('id')
            trabajos = Trabajo.objects.filter(doctor__in=inner_doctores)
            context['filtro_doctor'] = request.GET.get('doctor')
            filtro_avanzado = True
        """
        if request.GET.get('lente'):
            trabajos = trabajos.objects.filter(lente__icontains=request.GET.get('lente'))
            context['filtro_lente'] = request.GET.get('lente')
            filtro_avanzado = True
        if request.GET.get('tratamiento'):
            trabajos = trabajos.objects.filter(tratamiento__icontains=request.GET.get('tratamiento'))
            context['filtro_tratamiento'] = request.GET.get('tratamiento')
            filtro_avanzado = True
        if request.GET.get('armazon'):
            trabajos = trabajos.objects.filter(armazon__icontains=request.GET.get('armazon'))
            context['filtro_armazon'] = request.GET.get('armazon')
            filtro_avanzado = True
        if request.GET.get('obra_social'):
            trabajos = trabajos.objects.filter(obra_social__icontains=request.GET.get('obra_social'))
            context['filtro_obra_social'] = request.GET.get('obra_social')
            filtro_avanzado = True
        """

        context['object_list'] = trabajos
        context['filtro_avanzado'] = filtro_avanzado

        return render(request, self.template_name, context)


class TrabajoDetailView(DetailView):
    model = Trabajo
    template_name = "trabajo_detail.html"
    context_object_name = 'trabajo'


# class TrabajoCreateView(CreateView):
#     model = Trabajo
#     fields = '__all__'
#     template_name = 'trabajo_create.html'

#     def get_context_data(self, **kwargs):
#         context = super(TrabajoCreateView, self).get_context_data(**kwargs)
#         try:
#             context['persona'] = Persona.objects.get(id=self.request.GET.get('id_persona', None))
#         except Persona.DoesNotExist:
#             print("La persona no existe.")
#         except Exception as e:
#             print(f"Error: {e}")
#         return context
    
#     def post(request, *args, **kwargs):
#         print('ENTRO')
#         print('---------------------')
#         print(request)
#         print('---------------------')
        
class TrabajoCreateView(View):
    form_class = TrabajoForm
    template_name = "trabajo_create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'fecha': datetime.now()})
        
        context = {
            'form': form,
            'tipos_trabajo': TIPO_TRABAJO,
            'formset_lente_cerca': TrabajoLenteCercaFormSet(prefix='cerca'),
            'formset_lente_lejos': TrabajoLenteLejosFormSet(prefix='lejos'),
            'formset_lente_unico': TrabajoLenteUnicoFormSet(prefix='unico'),
            'formset_tratamiento_cerca': TrabajoTratamientoCercaFormSet(prefix='cerca'),
            'formset_tratamiento_lejos': TrabajoTratamientoLejosFormSet(prefix='lejos'),
            'formset_tratamiento_unico': TrabajoTratamientoUnicoFormSet(prefix='unico'),
            'formset_armazon_cerca': TrabajoArmazonCercaFormSet(prefix='cerca'),
            'formset_armazon_lejos': TrabajoArmazonLejosFormSet(prefix='lejos'),
            'formset_armazon_unico': TrabajoArmazonUnicoFormSet(prefix='unico'),
            'formset_material_cerca': TrabajoMaterialCercaFormSet(prefix='cerca'),
            'formset_material_lejos': TrabajoMaterialLejosFormSet(prefix='lejos'),
            'formset_material_unico': TrabajoMaterialUnicoFormSet(prefix='unico'),
        }

        persona = None
        if request.GET.get('id_persona'):
            # raise (form.errors)
            persona = Persona.objects.get(id=request.GET.get('id_persona'))
            context['persona'] = persona
        
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        formset_cerca = TrabajoLenteCercaFormSet(request.POST, prefix='cerca')
        formset_lejos = TrabajoLenteLejosFormSet(request.POST, prefix='lejos')
        formset_unico = TrabajoLenteUnicoFormSet(request.POST, prefix='unico')

        if (
            form.is_valid() and
            formset_cerca.is_valid() and
            formset_lejos.is_valid() and
            formset_unico.is_valid()
        ):
            trabajo = form.save()

            for fs in (formset_cerca, formset_lejos, formset_unico):
                fs.instance = trabajo
                fs.save()

            return HttpResponseRedirect(
                reverse("trabajo-detail-view", args=[trabajo.id])
            )

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'formset_cerca': formset_cerca,
                'formset_lejos': formset_lejos,
                'formset_unico': formset_unico,
            }
        )
        
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     trabajo = form.save()
        #     return HttpResponseRedirect(reverse("trabajo-detail-view", args=[trabajo.id]))
        # return render(request, self.template_name, {'form':form, 'persona':trabajo.persona})


class TrabajoUpdateView(View):
    form_class = TrabajoForm
    template_name = "trabajo_update.html"
    
    def get(self, request, *args, **kwargs):
        trabajo = Trabajo.objects.get(pk=kwargs['pk'])
        form = self.form_class(instance=trabajo)
        return render(request, self.template_name, {'form':form, 'persona':trabajo.persona})

    def post(self, request, *args, **kwargs):
        trabajo = Trabajo.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("trabajo-detail-view", args=[trabajo.id]))
        return render(request, self.template_name, {'form':form, 'persona':trabajo.persona})


class TrabajoDeleteView(DeleteView):
    model = Trabajo
    template_name = "trabajo_confirm_delete.html"
    success_url = reverse_lazy('trabajo-list-view')


class PersonaDesdeTrabajoListView(ListView):
    model = Persona
    template_name = "persona_trabajo_list.html"
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
        context = super(PersonaDesdeTrabajoListView, self).get_context_data(**kwargs)

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

        return context