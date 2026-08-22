from django.test import TestCase

from .models import topic_names


class TopicCreationTests(TestCase):
    def test_create_topic_name_and_show_it_on_home_page(self):
        response = self.client.post('/', {'topic_name': 'Django Community Topic'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(topic_names.objects.filter(topics='Django Community Topic').exists())
        self.assertContains(response, 'Django Community Topic')
