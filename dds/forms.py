from django import forms
from django.core.exceptions import ValidationError

from dds.models import Dds, Status, Type, Category


class CreateDdsRecordForm(forms.ModelForm):
    class Meta:
        model = Dds
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'type':
                self.fields[field].widget.attrs.update({'id': 'typeField'})
            elif field == 'category':
                self.fields[field].widget.attrs.update({'id': 'categoryField'})

            self.fields[field].widget.attrs.update({'class': 'form-control'})



class FilterForm(forms.Form):
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
        label='Статус'
    )

    type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Тип'
    )

    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Категория'
    )

    def __init__(self, *args, **kwargs):
        disabled = kwargs.pop('disabled', False)
        super().__init__(*args, **kwargs)

        self.fields['status'].choices = [(s.name, s.name) for s in Status.objects.all()]
        self.fields['type'].choices = [(t.name, t.name) for t in Type.objects.all()]
        self.fields['category'].choices = [(c.name, c.name) for c in Category.objects.all()]

        if disabled:
            for field in self.fields:
                self.fields[field].widget.attrs.update({'disabled': True})