from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charts/<int:birth_chart_id>/', views.varga_charts, name='varga_charts'),
    path('interpretation/<str:chart_type>/', views.chart_interpretation, name='chart_interpretation'),
    path('interpretation/<int:birth_chart_id>/<str:chart_type>/', views.chart_interpretation, name='chart_interpretation'),
]
