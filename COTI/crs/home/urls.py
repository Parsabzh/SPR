from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("hello/", views.hello.as_view()),
    # path("hi/", views.hi,name="hi"),
    path('input/', views.input_view, name='input_view'),
    path('result/', views.result_view, name='result_view'),
]