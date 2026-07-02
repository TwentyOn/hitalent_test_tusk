from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

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

class StatusUpdateView(UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'обновить статус'
        return context

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'dds/confirm_delete.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'удалить статус'
        context['object_name'] = f'статус "{self.object.name}"'
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

class TypeUpdateView(UpdateView):
    model = Type
    form_class = CreateStatusForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'обновить тип'
        return context

class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'dds/confirm_delete.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'удалить тип'
        context['object_name'] = f'тип "{self.object.name}"'
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

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'dictionary/create_form.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'обновить категорию'
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'dds/confirm_delete.html'
    success_url = reverse_lazy("dictionary:manage")
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'удалить категорию'
        context['object_name'] = f'категорию "{self.object.name}"'
        return context