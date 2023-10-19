
from django.contrib import admin
from django.urls import path
from API import views

urlpatterns = [
    # path('mymodel/<str:pk>', views.MyModelList.as_view(), name='my-model-list'),

    # for teacher
    path('tecAPI/', views.LCTeacherAPI.as_view()),
    path('tecAPI2/<str:search>/', views.LCTeacherAPI2.as_view()),
    path('tecAPI/<int:pk>', views.RUDTeacherAPI.as_view()),
]

