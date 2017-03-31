from django.views.generic import DetailView

from contrib.admin import celery_call

class DashboardView(DetailView):
    template_name = "dashboard.html"
    celery_error = None

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        #if self.celery_error:
        #    context['celery_error'] = self.celery_error
        context['celery_error'] = "celery error"
        return context

    def get_object(self, queryset=None):
        object = celery_call('api.media.get_perm_count')
        return object