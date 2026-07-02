from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

from .models import Dds
from .forms import CreateDdsRecordForm, FilterForm


class DdsCreateView(CreateView):
    model = Dds
    success_url = reverse_lazy("dds:dds-list")
    form_class = CreateDdsRecordForm
    template_name = 'dds/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новой записи'

        return context


# Create your views here.
class DdsListView(ListView):
    model = Dds
    context_object_name = 'records'
    template_name = 'dds/list.html'
    filtered = False

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filtered = False

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        statuses = self.request.GET.getlist('status')
        types = self.request.GET.getlist('type')
        categories = self.request.GET.getlist('category')

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
            self.filtered = True

        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
            self.filtered = True

        if statuses:
            queryset = queryset.filter(status__name__in=statuses)
            self.filtered = True

        if types:
            queryset = queryset.filter(type__name__in=types)
            self.filtered = True

        if categories:
            queryset = queryset.filter(category__name__in=categories)
            self.filtered = True



        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = FilterForm(disabled=self.filtered)
        context['title'] = 'Список записей'
        context['filtered'] = self.filtered

        return context




class DdsUpdateView(UpdateView):
    model = Dds
    form_class = CreateDdsRecordForm
    template_name = 'dds/update.html'
    context_object_name = 'record'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование записи'

        return context


class DdsDeleteView(DeleteView):
    model = Dds
    success_url = reverse_lazy("dds:dds-list")
    template_name = 'dds/confirm_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление записи'

        return context
