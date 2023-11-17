from django.contrib.auth import get_user_model
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from user.forms import UserCreateForm


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = datetime.now()
        return context



class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
