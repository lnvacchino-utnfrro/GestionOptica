from django.core.paginator import Paginator

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from base.models import Persona
from trabajos.forms import TrabajoForm
from trabajos.models import Trabajo

# CRUD - TRABAJOS
class TrabajoListView(ListView):
    model = Trabajo
    template_name = "trabajo_list.html"


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
        if request.GET.get('id_persona'):
            persona = Persona.objects.get(id=request.GET.get('id_persona'))
            return render(request, self.template_name, {'form':form, 'persona':persona})
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            print('ENTRO')
            trabajo = form.save()
            print('SE GRABÓ')
            return HttpResponseRedirect(reverse("trabajo-detail-view", args=[trabajo.id]))
        print(form.errors.as_json())
        return render(request, self.template_name, {'form':form, 'persona':trabajo.persona})
    

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
        print(form.errors.as_json())
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
        print(self.request.GET)
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