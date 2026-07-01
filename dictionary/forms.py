from django import forms

from .models import Status, Type

class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CreateTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})