from treasury.models import MonthlyReportModel
from django.template.loader import render_to_string
import weasyprint
from datetime import datetime
from django.http import HttpResponse
import tempfile
import locale
from treasury.utils import get_aggregate_transactions_by_category
from decimal import Decimal


def GenerateMonthlyPDFAnReportView(request, pk):
    locale.setlocale(locale.LC_ALL, "pt_BR")

    an_report = MonthlyReportModel.objects.get(pk=pk)
    reports_month = an_report.month.month
    reports_year = an_report.month.year
    positive_transactions_dict = get_aggregate_transactions_by_category(
        reports_year, reports_month, True
    )
    negative_transactions_dict = get_aggregate_transactions_by_category(
        reports_year, reports_month, False
    )

    m_result = (
        an_report.total_positive_transactions + an_report.total_negative_transactions
    )

    context = {
        "year": reports_year,
        "month": reports_month,
        "pm_balance": an_report.previous_month_balance,
        "report": an_report,
        "p_transactions": positive_transactions_dict,
        "n_transactions": negative_transactions_dict,
        "total_p": "{:.2f}".format(an_report.total_positive_transactions),
        "total_n": "{:.2f}".format(an_report.total_negative_transactions),
        "m_result": m_result,
        "balance": Decimal(an_report.total_balance),
    }
    print("CONTEXTO PARA PDF: ", context)
    html_index = render_to_string("treasury/export_analytical_report.html", context)

    weasyprint_html = weasyprint.HTML(
        string=html_index, base_url="http://127.0.0.1:8000/media"
    )
    pdf = weasyprint_html.write_pdf(
        stylesheets=[
            weasyprint.CSS(
                string="body { font-family: serif} img {margin: 10px; width: 40px;}"
            )
        ]
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "attachment; filename=analytical_report" + str(datetime.now()) + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response
