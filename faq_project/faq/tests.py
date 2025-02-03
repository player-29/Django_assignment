from django.test import TestCase
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(question="How do we start the development server?", answer="python manage.py runserver", language="en")

    def test_translation(self):
        self.assertEqual(self.faq.get_translation('hi'), self.faq.question_hi)

    def test_api_get_faqs(self):
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)

