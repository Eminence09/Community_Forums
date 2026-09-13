from django.test import TestCase
from django.contrib.auth.models import User

from .models import TopicReply, topic_info


class TopicCreationTests(TestCase):
    def test_documentation_page_lists_resources_for_public_users(self):
        response = self.client.get('/documentation/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Find the documentation for your next fix.')
        self.assertContains(response, 'Django overview')
        self.assertContains(response, 'https://docs.djangoproject.com/en/5.0/topics/testing/')

    def test_technology_and_news_pages_list_resources_for_public_users(self):
        technology_response = self.client.get('/latest-technologies/')
        news_response = self.client.get('/news/')

        self.assertEqual(technology_response.status_code, 200)
        self.assertContains(technology_response, 'Keep your toolkit current.')
        self.assertContains(technology_response, 'Python 3.13')
        self.assertEqual(news_response.status_code, 200)
        self.assertContains(news_response, 'Stay close to what is changing.')
        self.assertContains(news_response, 'Django news')

    def test_create_topic_and_show_it_on_home_page(self):
        user = User.objects.create_user(username='forum-user', password='test-password')
        self.client.force_login(user)

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

    def test_newest_topic_is_first_announcement(self):
        user = User.objects.create_user(username='forum-user', password='test-password')
        self.client.force_login(user)
        topic_info.objects.create(topic_names='Older topic', topic_description='Older description')
        topic_info.objects.create(topic_names='Newest topic', topic_description='Newest description')

        response = self.client.get('/')

        self.assertEqual(response.context['topics'][0].topic_names, 'Newest topic')
        self.assertContains(response, 'Newest topic')

    def test_new_announcements_page_shows_newest_posts(self):
        user = User.objects.create_user(username='forum-user', password='test-password')
        self.client.force_login(user)
        topic_info.objects.create(
            username='forum-user',
            system_name='test-system',
            topic_names='New announcement topic',
            topic_description='New announcement post body.'
        )

        response = self.client.get('/new-announcements/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Announcements')
        self.assertContains(response, 'New announcement topic')
        self.assertContains(response, 'New announcement post body.')

    def test_authenticated_user_can_reply_to_topic(self):
        user = User.objects.create_user(username='reply-user', password='test-password')
        self.client.force_login(user)
        topic = topic_info.objects.create(
            username='topic-owner',
            topic_names='Discussion topic',
            topic_description='Original discussion post.'
        )

        response = self.client.post(
            f'/topics/{topic.id}/',
            {'body': 'This is a public reply.'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(TopicReply.objects.filter(topic=topic, username='reply-user').exists())
        self.assertContains(response, 'This is a public reply.')
