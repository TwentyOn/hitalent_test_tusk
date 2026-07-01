from django import forms

from dds.models import Dds


class CreateDdsRecordForm(forms.ModelForm):
    class Meta:
        model = Dds
        fields = '__all__'