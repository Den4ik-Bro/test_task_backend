from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'app'

router = DefaultRouter()
router.register('account', viewset=views.AccountViewSet, basename='account')


urlpatterns = [
    path('', include(router.urls))
]