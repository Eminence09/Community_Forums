from django.test import TestCase
from django.contrib.auth.models import User

from .models import TopicReply, topic_info


class TopicCreationTests(TestCase):
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
