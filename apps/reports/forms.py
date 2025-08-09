from django import forms
from apps.common.models import Currency
from apps.entities.models import Entity

ENTITY_TYPE_CHOICES = [
    ("", "All"),
    ("donor", "Donor"),
    ("recipient", "Recipient"),
]

class ReportFilterForm(forms.Form):
    # Entity fields
    custom_id = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Entity custom_id"}))
    entity_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Entity name contains"}))
    entity_type = forms.ChoiceField(choices=ENTITY_TYPE_CHOICES, required=False, widget=forms.Select(attrs={"class": "form-select"}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Location contains"}))

    # Transaction fields
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True).order_by("code"),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"}))
    min_amount = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))
    max_amount = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))
    min_converted_mmk = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))
    max_converted_mmk = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))

    # Sorting
    order_by = forms.ChoiceField(
        required=False,
        choices=[
            ("-date", "Date ↓"), ("date", "Date ↑"),
            ("entity__custom_id", "Entity ID ↑"), ("-entity__custom_id", "Entity ID ↓"),
            ("amount", "Amount ↑"), ("-amount", "Amount ↓"),
            ("converted_amount_mmk", "MMK ↑"), ("-converted_amount_mmk", "MMK ↓"),
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )