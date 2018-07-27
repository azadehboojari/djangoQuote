from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashbord', views.dashbord),
    path('logout', views.logout),
    path('view/<int:addby_id>', views.view),
    path('favorite/<int:quote_id>', views.favorite),
    path('create', views.create),
    path('remove/<int:quote_id>', views.remove)
]