from django.views.generic import TemplateView


class MinutesEditorView(TemplateView):
    template_name = 'secretarial/minutes_editor.html'
