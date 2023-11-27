from django.views.generic import DetailView
from treasury.models import MonthlyReportModel
from dateutil.relativedelta import relativedelta
from datetime import date


class MonthlyAnalyticalReportDetailView(DetailView):
    template_name = 'treasury/detailed_analytical_report.html'
    model = MonthlyReportModel
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_value = self.kwargs['pk']

        context['pk_value'] = pk_value
        return context
