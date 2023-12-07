from django.urls import path
from masteradmin import views


urlpatterns = [
    path('manage_property',views.ManageProperty.as_view(),name='manage_property'),
    path('list_units',views.ManageUnits.as_view(),name='list_units'),

       
    ]
    