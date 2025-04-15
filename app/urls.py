from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/new/', views.note_new, name='note_new'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/toggle-pin/', views.toggle_pin_note, name='toggle_pin_note'),
]
