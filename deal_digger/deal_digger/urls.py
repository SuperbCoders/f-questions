"""deal_digger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from deal_api import api_views as api_views
from deal_api import views


urlpatterns = [
    path('', views.DocumentListView.as_view(), name='document-list'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('document/<int:pk>/ask/', views.ask_model, name='document-ask'),
    path('document/<int:pk>/extract-text/', views.ask_ocr, name='document-ocr'),
    path('document/<int:pk>/delete/', views.delete_document, name='document-delete'),
    path('form/', views.get_deal_form),
    path('api/extract', api_views.ExtractEntitiesApi.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
