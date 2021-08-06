from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from . import views

api_doc_view = get_swagger_view(title='Knowledge Base API')

urlpatterns = format_suffix_patterns([
    path('foodon/<str:id>/', views.ingredient_from_foodon),
    path('foodon_ids', views.ingredients_with_foodons),
    path('ingredient', views.ingredient_data),
    path('density', views.density),
    path('portions', views.portion_data),
    path('ghg', views.ghg_mass),
    path('upload', views.upload, name='upload'),
    path('upload_foodon', views.upload_foodon, name='upload_foodon'),
    path('upload_portion', views.upload_portion, name='upload_portion'),
    url(r'^$', api_doc_view)
])