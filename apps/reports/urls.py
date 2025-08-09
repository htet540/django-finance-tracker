from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.index, name="index"),
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/xlsx/", views.export_xlsx, name="export_xlsx"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),
]