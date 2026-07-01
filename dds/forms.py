from django import forms
from django.core.exceptions import ValidationError

from dds.models import Dds, Status, Type


class CreateDdsRecordForm(forms.ModelForm):
    class Meta:
        model = Dds
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class MyForm(forms.Form):
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='Начиная с даты'
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='Заканчивая датой'
    )
    status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(s.name, s.name) for s in Status.objects.all()],
        label='Статус'
    )