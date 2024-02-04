from django.urls import path
from trabajos import views

urlpatterns = [
    path('<int:pk>/', views.TrabajoDetailView.as_view(), name='trabajo-detail-view'),
    path('<int:pk>/editar/', views.TrabajoUpdateView.as_view(), name='trabajo-update-view'),
    path('crear-trabajo/', views.TrabajoCreateView.as_view(), name='trabajo-create-view'),
    path('crear-trabajo/buscar-persona/', views.PersonaDesdeTrabajoListView.as_view(), name='persona-trabajo-list-view'),
    path('', views.TrabajoListView.as_view(), name='trabajo-list-view'),
    path('<int:pk>/borrar/', views.TrabajoDeleteView.as_view(), name='trabajo-delete-view'),
]
