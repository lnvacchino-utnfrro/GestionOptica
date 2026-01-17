from django.core.paginator import Paginator

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from base.models import *
from trabajos.forms import *
from trabajos.models import TIPO_ANTEOJO, Trabajo, TrabajoLente, TIPO_TRABAJO

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
    context_object_name = "trabajo"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "persona",
                "doctor",
                "obra_social",
            )
            .prefetch_related(
                # LENTES
                "TrabajoLente_trabajo__lente",
                # TRATAMIENTOS
                "TrabajoTratamiento_trabajo__tratamiento",
                # ARMAZONES
                "TrabajoArmazon_trabajo__armazon",
                # MATERIALES
                "TrabajoMaterial_trabajo__material",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Choices (por si los necesitás en el template)
        context["tipos_trabajo"] = TIPO_TRABAJO
        context["tipos_anteojo"] = TIPO_ANTEOJO

        # Alias útiles (opcional, pero mejora legibilidad en template)
        trabajo = self.object

        context["lente_unico"] = trabajo.lente_unico
        context["lente_lejos"] = trabajo.lente_lejos
        context["lente_cerca"] = trabajo.lente_cerca

        context["tratamiento_unico"] = trabajo.tratamiento_unico
        context["tratamiento_lejos"] = trabajo.tratamiento_lejos
        context["tratamiento_cerca"] = trabajo.tratamiento_cerca

        context["armazon_unico"] = trabajo.armazon_unico
        context["armazon_lejos"] = trabajo.armazon_lejos
        context["armazon_cerca"] = trabajo.armazon_cerca

        context["material_unico"] = trabajo.material_unico
        context["material_lejos"] = trabajo.material_lejos
        context["material_cerca"] = trabajo.material_cerca

        return context

    


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

        formset_lente_cerca = TrabajoLenteCercaFormSet(request.POST, prefix='cerca')
        formset_lente_lejos = TrabajoLenteLejosFormSet(request.POST, prefix='lejos')
        formset_lente_unico = TrabajoLenteUnicoFormSet(request.POST, prefix='unico')
        formset_tratamiento_cerca = TrabajoTratamientoCercaFormSet(request.POST, prefix='cerca')
        formset_tratamiento_lejos = TrabajoTratamientoLejosFormSet(request.POST, prefix='lejos')
        formset_tratamiento_unico = TrabajoTratamientoUnicoFormSet(request.POST, prefix='unico')
        formset_armazon_cerca = TrabajoArmazonCercaFormSet(request.POST, prefix='cerca')
        formset_armazon_lejos = TrabajoArmazonLejosFormSet(request.POST, prefix='lejos')
        formset_armazon_unico = TrabajoArmazonUnicoFormSet(request.POST, prefix='unico')
        formset_material_cerca = TrabajoMaterialCercaFormSet(request.POST, prefix='cerca')
        formset_material_lejos = TrabajoMaterialLejosFormSet(request.POST, prefix='lejos')
        formset_material_unico = TrabajoMaterialUnicoFormSet(request.POST, prefix='unico')

        if (
            form.is_valid() and
            formset_lente_cerca.is_valid() and
            formset_lente_lejos.is_valid() and
            formset_lente_unico.is_valid() and
            formset_tratamiento_cerca.is_valid() and
            formset_tratamiento_lejos.is_valid() and
            formset_tratamiento_unico.is_valid() and
            formset_armazon_cerca.is_valid() and
            formset_armazon_lejos.is_valid() and
            formset_armazon_unico.is_valid() and
            formset_material_cerca.is_valid() and
            formset_material_lejos.is_valid() and
            formset_material_unico.is_valid()
        ):
            trabajo = form.save()

            for fs in (formset_lente_cerca, formset_lente_lejos, formset_lente_unico, 
                       formset_tratamiento_cerca, formset_tratamiento_lejos, formset_tratamiento_unico,
                       formset_armazon_cerca, formset_armazon_lejos, formset_armazon_unico,
                       formset_material_cerca, formset_material_lejos, formset_material_unico):
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
                'formset_lente_cerca': formset_lente_cerca,
                'formset_lente_lejos': formset_lente_lejos,
                'formset_lente_unico': formset_lente_unico,
                'formset_tratamiento_cerca': formset_tratamiento_cerca,
                'formset_tratamiento_lejos': formset_tratamiento_lejos,
                'formset_tratamiento_unico': formset_tratamiento_unico,
                'formset_armazon_cerca': formset_armazon_cerca,
                'formset_armazon_lejos': formset_armazon_lejos,
                'formset_armazon_unico': formset_armazon_unico,
                'formset_material_cerca': formset_material_cerca,
                'formset_material_lejos': formset_material_lejos,
                'formset_material_unico': formset_material_unico,
            }
        )
        
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     trabajo = form.save()
        #     return HttpResponseRedirect(reverse("trabajo-detail-view", args=[trabajo.id]))
        # return render(request, self.template_name, {'form':form, 'persona':trabajo.persona})


class TrabajoUpdateView(View):
    template_name = "trabajo_update.html"
    form_class = TrabajoForm

    def get(self, request, pk):
        trabajo = get_object_or_404(Trabajo, pk=pk)
        form = self.form_class(instance=trabajo)

        context = {
            "form": form,
            "trabajo": trabajo,
            "persona": trabajo.persona,
            "tipos_trabajo": TIPO_TRABAJO,

            "formset_lente_cerca": TrabajoLenteCercaFormSet(
                instance=trabajo,
                prefix="lente_cerca",
                queryset=TrabajoLente.objects.filter(trabajo=trabajo, tipo="CERCA"),
            ),
            "formset_lente_lejos": TrabajoLenteLejosFormSet(
                instance=trabajo,
                prefix="lente_lejos",
                queryset=TrabajoLente.objects.filter(trabajo=trabajo, tipo="LEJOS"),
            ),
            "formset_lente_unico": TrabajoLenteUnicoFormSet(
                instance=trabajo,
                prefix="lente_unico",
                queryset=TrabajoLente.objects.filter(trabajo=trabajo, tipo="UNICO"),
            ),

            "formset_tratamiento_cerca": TrabajoTratamientoCercaFormSet(
                instance=trabajo,
                prefix="tratamiento_cerca",
                queryset=TrabajoTratamiento.objects.filter(trabajo=trabajo, tipo="CERCA"),
            ),
            "formset_tratamiento_lejos": TrabajoTratamientoLejosFormSet(
                instance=trabajo,
                prefix="tratamiento_lejos",
                queryset=TrabajoTratamiento.objects.filter(trabajo=trabajo, tipo="LEJOS"),
            ),
            "formset_tratamiento_unico": TrabajoTratamientoUnicoFormSet(
                instance=trabajo,
                prefix="tratamiento_unico",
                queryset=TrabajoTratamiento.objects.filter(trabajo=trabajo, tipo="UNICO"),
            ),

            "formset_armazon_cerca": TrabajoArmazonCercaFormSet(
                instance=trabajo,
                prefix="armazon_cerca",
                queryset=TrabajoArmazon.objects.filter(trabajo=trabajo, tipo="CERCA"),
            ),
            "formset_armazon_lejos": TrabajoArmazonLejosFormSet(
                instance=trabajo,
                prefix="armazon_lejos",
                queryset=TrabajoArmazon.objects.filter(trabajo=trabajo, tipo="LEJOS"),
            ),
            "formset_armazon_unico": TrabajoArmazonUnicoFormSet(
                instance=trabajo,
                prefix="armazon_unico",
                queryset=TrabajoArmazon.objects.filter(trabajo=trabajo, tipo="UNICO"),
            ),

            "formset_material_cerca": TrabajoMaterialCercaFormSet(
                instance=trabajo,
                prefix="material_cerca",
                queryset=TrabajoMaterial.objects.filter(trabajo=trabajo, tipo="CERCA"),
            ),
            "formset_material_lejos": TrabajoMaterialLejosFormSet(
                instance=trabajo,
                prefix="material_lejos",
                queryset=TrabajoMaterial.objects.filter(trabajo=trabajo, tipo="LEJOS"),
            ),
            "formset_material_unico": TrabajoMaterialUnicoFormSet(
                instance=trabajo,
                prefix="material_unico",
                queryset=TrabajoMaterial.objects.filter(trabajo=trabajo, tipo="UNICO"),
            ),
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        trabajo = get_object_or_404(Trabajo, pk=pk)

        form = self.form_class(request.POST, instance=trabajo)

        formsets = [
            TrabajoLenteCercaFormSet(request.POST, instance=trabajo, prefix="lente_cerca"),
            TrabajoLenteLejosFormSet(request.POST, instance=trabajo, prefix="lente_lejos"),
            TrabajoLenteUnicoFormSet(request.POST, instance=trabajo, prefix="lente_unico"),

            TrabajoTratamientoCercaFormSet(request.POST, instance=trabajo, prefix="tratamiento_cerca"),
            TrabajoTratamientoLejosFormSet(request.POST, instance=trabajo, prefix="tratamiento_lejos"),
            TrabajoTratamientoUnicoFormSet(request.POST, instance=trabajo, prefix="tratamiento_unico"),

            TrabajoArmazonCercaFormSet(request.POST, instance=trabajo, prefix="armazon_cerca"),
            TrabajoArmazonLejosFormSet(request.POST, instance=trabajo, prefix="armazon_lejos"),
            TrabajoArmazonUnicoFormSet(request.POST, instance=trabajo, prefix="armazon_unico"),

            TrabajoMaterialCercaFormSet(request.POST, instance=trabajo, prefix="material_cerca"),
            TrabajoMaterialLejosFormSet(request.POST, instance=trabajo, prefix="material_lejos"),
            TrabajoMaterialUnicoFormSet(request.POST, instance=trabajo, prefix="material_unico"),
        ]

        if form.is_valid() and all(fs.is_valid() for fs in formsets):
            trabajo = form.save()

            for fs in formsets:
                fs.save()

            return HttpResponseRedirect(
                reverse("trabajo-detail-view", args=[trabajo.id])
            )

        # si algo falla, vuelve al update
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "trabajo": trabajo,
                "persona": trabajo.persona,
                "tipos_trabajo": TIPO_TRABAJO,
                "formset_lente_cerca": formsets[0],
                "formset_lente_lejos": formsets[1],
                "formset_lente_unico": formsets[2],
                "formset_tratamiento_cerca": formsets[3],
                "formset_tratamiento_lejos": formsets[4],
                "formset_tratamiento_unico": formsets[5],
                "formset_armazon_cerca": formsets[6],
                "formset_armazon_lejos": formsets[7],
                "formset_armazon_unico": formsets[8],
                "formset_material_cerca": formsets[9],
                "formset_material_lejos": formsets[10],
                "formset_material_unico": formsets[11],
            }
        )



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