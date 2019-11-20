from django.urls import path
from profiles_api import views

urlpatterns = [
    #.as_view --> it will render the url to the function call in the view
    path('hello-view/', views.HelloApiView.as_view()),
]
