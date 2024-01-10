from django.test import TestCase
from django.urls import reverse
from events.models import Event, EventCategory, Venue
from events.forms import EventForm
from events.views import EventCreateView
from users.models import CustomUser
from django.test import Client
from django.contrib.auth.models import Permission
from model_mommy import mommy


class EventCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.permission = Permission.objects.get(name='Can add event')  # Assuming the permission name
        self.user.user_permissions.add(self.permission)
        self.client.login(username='testuser', password='testpassword')
        self.create_url = reverse('events:create-event')
        self.category = mommy.make(EventCategory, _quantity=5)
        self.venue = mommy.make(Venue, _quantity=5)

    def test_event_create_view(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/form.html')
        self.assertIsInstance(response.context['view'], EventCreateView)
        self.assertIsInstance(response.context['form'], EventForm)

    def test_event_create_success(self):
        contact_user = mommy.make(CustomUser, _quantity=5)
        event_data = {
            "user": self.user,
            "title": "Sunset Serenade Concert",
            "description": "An evening of mesmerizing melodies as the sun sets!",
            "start_date": "2024-04-20T17:30:00Z",
            "end_date": "2024-04-20T21:30:00Z",
            "price": "75.00",
            "location": 2,
            "contact_name": "Emily Watson",
            "contact_user": 3,
            "category": 2,
        }
        initial_event_count = Event.objects.count()
        response = self.client.post(self.create_url, event_data)
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Event.objects.count(), initial_event_count + 1)

    def test_event_create_permission(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        non_permitted_user = CustomUser.objects.create_user(username='non_permitted', password='testpassword')
        self.client.login(username='non_permitted', password='testpassword')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403) 
