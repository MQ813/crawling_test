from django.urls import path
from myapp import views
urlpatterns = [
    path('', views.home),
    path('create/', views.create),
    path('read/<title>', views.read),
    path('char_info/', views.char_info),
    path('char_info/<name>', views.char_info),
]
