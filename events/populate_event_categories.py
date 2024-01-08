from events.models import EventCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populates EventCategory model with initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Geral', 'description': 'Eventos gerais'},
            {'name': 'Jovens', 'description': 'Eventos para jovens'},
            {'name': 'Crianças', 'description': 'Eventos para crianças'},
            {'name': 'Casais', 'description': 'Eventos para casais'},
            {'name': 'Famílias', 'description': 'Eventos para famílias'},
        ]

        for category_data in categories:
            category, created = EventCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Categoria '{category.name}' criada com sucesso..."))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Categoria '{category.name}' já existe..."))
