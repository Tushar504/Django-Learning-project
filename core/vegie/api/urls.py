from django.urls import path
from .views import *

urlpatterns = [
    path("receipes/", ReceipeList.as_view(), name="api_receipes"),
    path("receipes/<int:pk>/", ReceipeDetail.as_view(), name="api_detail_receipes")
]