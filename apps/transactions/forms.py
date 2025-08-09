from django import forms
from django.forms import inlineformset_factory
from .models import Transaction, TransactionAttachment
from apps.entities.models import Entity

class TransactionForm(forms.ModelForm):
    # Helper field to live-filter the entity autocomplete (not saved to DB)
    entity_type = forms.ChoiceField(
        choices=[("donor", "Donor"), ("recipient", "Recipient")],
        initial="donor",
        required=False,
        label="Entity Type"
    )

    class Meta:
        model = Transaction
        fields = [
            "date", "entity", "entity_type", "currency", "amount",
            "exchange_rate", "designated_purpose", "notes"
        ]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"}),
            "entity": forms.Select(attrs={"class": "form-select", "id": "entity-select"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "exchange_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001", "value": "1"}),
            "designated_purpose": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "entity_type": forms.Select(attrs={"class": "form-select", "id": "entity-type"}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = TransactionAttachment
        fields = ["file"]

AttachmentFormSet = inlineformset_factory(
    parent_model=Transaction,
    model=TransactionAttachment,
    form=AttachmentForm,
    extra=2,
    can_delete=True
)