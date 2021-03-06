"""time_keep_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from time_keep_api.schema import schema_view

api_v1_patterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schedules/", include(arg=("time_keep_api.schedules.urls", "schedules"), namespace="schedules"))
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(arg=(api_v1_patterns, "v1_patterns"), namespace="api_v1")),
    path("", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
