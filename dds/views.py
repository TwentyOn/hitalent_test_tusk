from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .models import Dds
from .forms import CreateDdsRecordForm

class DdsCreateView(CreateView):
    model = Dds
    form_class = CreateDdsRecordForm
    template_name = 'dds/create.html'

# Create your views here.
class DdsListView(ListView):
    model = Dds
    context_object_name = 'item'
    template_name = 'dds/list.html'

class DdsDetailView(DetailView):
    model = Dds
    template_name = 'dds/detail.html'
    slug_url_kwarg = 'id'
    slug_field = 'id'
