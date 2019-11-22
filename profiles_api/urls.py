from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

# this is for the ViewSet
# create the router and register the new viewset. It figures out the urls needed
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name = 'hello-viewset')

urlpatterns = [
    #.as_view --> it will render the url to the function call in the view
    path('hello-view/', views.HelloApiView.as_view()),
    #this is for the viewset
    path('',include(router.urls))
]
