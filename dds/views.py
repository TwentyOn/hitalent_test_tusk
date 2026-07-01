from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

from .models import Dds
from .forms import CreateDdsRecordForm

class DdsCreateView(CreateView):
    model = Dds
    form_class = CreateDdsRecordForm
    template_name = 'dds/create.html'
    success_url = reverse_lazy("dds-list")

# Create your views here.
class DdsListView(ListView):
    model = Dds
    context_object_name = 'records'
    template_name = 'dds/list.html'


class DdsUpdateView(UpdateView):
    model = Dds
    form_class = CreateDdsRecordForm
    template_name = 'dds/update.html'
    context_object_name = 'record'
    slug_field = 'id'
    slug_url_kwarg = 'id'

class DdsDeleteView(DeleteView):
    model = Dds
    success_url = reverse_lazy("dds-list")
    template_name = 'dds/confirm_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'



