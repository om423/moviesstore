from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),

    # NEW
    path('feedback/create/', views.create_feedback, name='cart.create_feedback'),
    path('feedbacks/', views.feedback_list, name='cart.feedback_list'),
] 