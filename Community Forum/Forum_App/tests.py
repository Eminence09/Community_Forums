from django.test import TestCase

from .models import topic_info


class TopicCreationTests(TestCase):
    def test_create_topic_and_show_it_on_home_page(self):
        response = self.client.post(
            '/',
            {
                'topic_names': 'Django Community Topic',
                'topic_description': 'This is a test topic.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(topic_info.objects.filter(topic_names='Django Community Topic').exists())
        self.assertContains(response, 'Django Community Topic')
