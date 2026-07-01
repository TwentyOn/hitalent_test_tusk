from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .models import Status, Type
from .forms import CreateTypeForm, CreateStatusForm

# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, "dictionary/index.html", context={
            'types': Type.objects.all(),
            'statuses': Status.objects.all(),
            'title': 'Управление справочником'
        })


class StatusCreateView(CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'dictionary/status/create.html'
    success_url = reverse_lazy("dds:dds-list")

class TypeCreateView(CreateView):
    model = Type
    form_class = CreateTypeForm
    template_name = 'dictionary/type/create.html'
    success_url = reverse_lazy("dds:dds-list")