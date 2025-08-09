from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("", RedirectView.as_view(pattern_name="dashboard:index", permanent=False)),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("entities/", include("apps.entities.urls", namespace="entities")),
    path("transactions/", include("apps.transactions.urls", namespace="transactions")),
    path("reports/", include("apps.reports.urls", namespace="reports")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)