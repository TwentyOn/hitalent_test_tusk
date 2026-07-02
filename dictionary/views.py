from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .models import Status, Type, Category
from .forms import CreateTypeForm, CreateStatusForm, CreateCategoryForm


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, "dictionary/index.html", context={
            'types': Type.objects.all(),
            'statuses': Status.objects.all(),
            'categories': Category.objects.all(),
            'title': 'Управление справочником'
        })


class StatusCreateView(CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'создать статус'
        return context

class TypeCreateView(CreateView):
    model = Type
    form_class = CreateTypeForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'создать тип'
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'создать категорию'
        return context