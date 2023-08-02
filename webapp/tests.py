from django.urls import reverse
from django.utils import timezone
from .models import Events, TypeEvents, News, Cities, ChatRequest, AdminRequest
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from accounts.models import Account, Role


class EventDetailViewTest(TestCase):
    def setUp(self):
        type_events = TypeEvents.objects.create(events_name='Test Type Event')
        self.event = Events.objects.create(
            name='Test Event',
            number_of_seats=50,
            description='Test event description',
            events_at=timezone.now(),
            price=10.00,
            type_events=type_events
        )

    def test_get_context_data(self):
        url = reverse('events_detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

        total_seats = self.event.number_of_seats
        booked_seats = self.event.resident_booked.count()
        available_seats = total_seats - booked_seats

        self.assertEqual(response.context['available_seats'], available_seats)

    def test_template_used(self):
        url = reverse('events_detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'event_detail.html')


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser@example.com', email='testuser@example.com',
                                                         password='12345')
        self.account = Account.objects.create(first_name='John', last_name='Doe')

    def test_profile_detail_view(self):
        url = reverse('account_detail', kwargs={'pk': self.account.pk})
        self.client.login(email=self.user.email, password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_detail.html')
        self.assertContains(response, self.account.first_name)
        self.assertContains(response, self.account.last_name)


class NewslineViewTestCase(TestCase):
    def test_auth_required(self):
        response = self.client.get(reverse('newsline'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class EventsUpdateTest(TestCase):
    def setUp(self):
        type_events = TypeEvents.objects.create(events_name='Test Type Event')
        self.events = Events.objects.create(
            name='Test Event',
            number_of_seats=50,
            description='Test event description',
            events_at=timezone.now(),
            price=10.00,
            type_events=type_events
        )

    def test_update_events(self):
        url = reverse('events_update', kwargs={'pk': self.events.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.events.refresh_from_db()

        self.assertEqual(self.events.name, 'Test Event')
        self.assertEqual(self.events.number_of_seats, 50)
        self.assertEqual(self.events.description, 'Test event description')
        self.assertEqual(self.events.price, 10)
        self.assertEqual(response.context['events'].pk, 3)
        self.assertTrue('events' in response.context)
        self.assertTemplateUsed(response, 'events_update.html')

        url = reverse('news_update', kwargs={'pk': 9})
        null_response = self.client.get(url)
        self.assertEqual(null_response.status_code, 404)


class NewsUpdateTest(TestCase):
    def setUp(self):
        cities = Cities.objects.create(citi_name='Test citi name')
        self.user = Account.objects.create_user(username='testuser', password='testpass')

        self.news = News.objects.create(
            name='Test News',
            user=self.user,
            description='Test news description',
            cities=cities
        )

    def test_update_news(self):
        url = reverse('news_update', kwargs={'pk': self.news.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.news.refresh_from_db()

        self.assertEqual(response.context['news'].pk, 2)
        self.assertEqual(self.news.name, 'Test News')
        self.assertEqual(self.news.description, 'Test news description')
        self.assertTemplateUsed(response, 'news_update.html')
        self.assertTrue('news' in response.context)

        url = reverse('news_update', kwargs={'pk': 9})
        null_response = self.client.get(url)
        self.assertEqual(null_response.status_code, 404)


class NewsDeleteTest(TestCase):
    def setUp(self):
        cities = Cities.objects.create(citi_name='Test citi name')
        self.user = get_user_model().objects.create_user(username='testuser@example.com', email='testuser@example.com',
                                                         password='12345')
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()
        self.assertEqual(self.user.is_superuser, True)
        login = self.client.login(email=self.user.email, password='12345')
        self.failUnless(login, 'Could not log in')

        self.news = News.objects.create(
            name='Test News',
            user=self.user,
            description='Test news description',
            cities=cities
        )

    def test_delete_news(self):
        url = reverse('news_confirm_delete', kwargs={'pk': self.news.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.news.refresh_from_db()

        self.assertEqual(response.context['news'].pk, 1)
        self.assertEqual(response.context['news'].name, 'Test News')
        self.assertTrue('news' in response.context)
        self.assertContains(response, self.news.name)
        self.assertTemplateUsed(response, 'news_confirm_delete.html')

        url = reverse('news_confirm_delete', kwargs={'pk': 9})
        null_response = self.client.get(url)
        self.assertEqual(null_response.status_code, 404)


class AdminRequestDetailViewTest(TestCase):
    def setUp(self):
        role_test = Role.objects.create(
            name='test role',
            privileges=['ALLOW_REQUEST_FROM_ALL_RESIDENT_READ']
        )
        self.user = Account.objects.create_user(
            username='test_user_request',
            email='test_user_request@example.com',
            password='12345',
            role=role_test
        )
        cities_test = Cities.objects.create(citi_name="Test City")
        user_sender = Account.objects.create_user(
            username='test_user_sender',
            email='test_user_sender@example.com',
            password='12345'
        )
        second_user_chat = Account.objects.create_user(
            username='test_second_user_chat',
            email='test_second_user_chat@example.com',
            password='12345'
        )
        user_reviewer = Account.objects.create_user(
            username='test_user_reviewer',
            email='test_user_reviewer@example.com',
            password='12345'
        )
        chat_request = ChatRequest.objects.create(
            chat_name='Test chat name',
            cities=cities_test,
            second_user=second_user_chat,
            description='Test chat description',
            rules='Test chat rules'
        )
        self.reqeust_test = AdminRequest.objects.create(
            user_reviewer=user_reviewer,
            user_sender=user_sender,
            approved=True,
            closed_at=timezone.now(),
            request_text='Test request text',
            response_text='Test response text',
            chat_request=chat_request
        )

    def test_get_context_data(self):
        self.client.force_login(self.user)
        url = reverse('request_detail', kwargs={'pk': self.reqeust_test.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['request_detail'], self.reqeust_test)

    def test_template_used(self):
        self.client.force_login(self.user)
        url = reverse('request_detail', kwargs={'pk': self.reqeust_test.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'request_detail.html')


class AdminRequestUpdateViewTest(TestCase):
    def setUp(self):
        role_test = Role.objects.create(
            name='test role',
            privileges=['ALLOW_REQUEST_UPDATE']
        )
        self.user = Account.objects.create_user(
            username='test_user_request',
            email='test_user_request@example.com',
            password='12345',
            role=role_test
        )
        cities_test = Cities.objects.create(citi_name="Test City")
        user_sender = Account.objects.create_user(
            username='test_user_sender',
            email='test_user_sender@example.com',
            password='12345'
        )
        second_user_chat = Account.objects.create_user(
            username='test_second_user_chat',
            email='test_second_user_chat@example.com',
            password='12345'
        )
        user_reviewer = Account.objects.create_user(
            username='test_user_reviewer',
            email='test_user_reviewer@example.com',
            password='12345'
        )
        chat_request = ChatRequest.objects.create(
            chat_name='Test chat name',
            cities=cities_test,
            second_user=second_user_chat,
            description='Test chat description',
            rules='Test chat rules'
        )
        self.reqeust_test = AdminRequest.objects.create(
            user_reviewer=user_reviewer,
            user_sender=user_sender,
            closed_at=timezone.now(),
            approved=True,
            request_text='Test request text',
            response_text='Test response text',
            chat_request=chat_request
        )

    def test_update_request(self):
        self.client.force_login(self.user)
        url = reverse('request_update', kwargs={'pk': self.reqeust_test.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.reqeust_test.refresh_from_db()

        self.assertEqual(response.context['request_detail'].pk, self.reqeust_test.pk)
        self.assertEqual(self.reqeust_test.request_text, 'Test request text')
        self.assertEqual(self.reqeust_test.response_text, 'Test response text')
        self.assertTemplateUsed(response, 'request_update.html')
        self.assertTrue('request_detail' in response.context)

        url = reverse('request_update', kwargs={'pk': self.reqeust_test.pk + 1})
        null_response = self.client.get(url)
        self.assertEqual(null_response.status_code, 404)


class AdminRequestDeleteViewTest(TestCase):
    def setUp(self):
        role_test = Role.objects.create(
            name='test role',
            privileges=['ALLOW_REQUEST_DELETE']
        )
        self.user = Account.objects.create_user(
            username='test_user_request',
            email='test_user_request@example.com',
            password='12345',
            role=role_test
        )
        cities_test = Cities.objects.create(citi_name="Test City")
        user_sender = Account.objects.create_user(
            username='test_user_sender',
            email='test_user_sender@example.com',
            password='12345'
        )
        second_user_chat = Account.objects.create_user(
            username='test_second_user_chat',
            email='test_second_user_chat@example.com',
            password='12345'
        )
        user_reviewer = Account.objects.create_user(
            username='test_user_reviewer',
            email='test_user_reviewer@example.com',
            password='12345'
        )
        chat_request = ChatRequest.objects.create(
            chat_name='Test chat name',
            cities=cities_test,
            second_user=second_user_chat,
            description='Test chat description',
            rules='Test chat rules'
        )
        self.reqeust_test = AdminRequest.objects.create(
            user_reviewer=user_reviewer,
            user_sender=user_sender,
            approved=True,
            closed_at=timezone.now(),
            request_text='Test request text',
            response_text='Test response text',
            chat_request=chat_request
        )

    def test_delete_request(self):
        self.client.force_login(self.user)
        url = reverse('request_delete', kwargs={'pk': self.reqeust_test.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.reqeust_test.refresh_from_db()

        self.assertEqual(response.context['request_detail'].pk, self.reqeust_test.pk)
        self.assertEqual(response.context['request_detail'].request_text, 'Test request text')
        self.assertTrue('request_detail' in response.context)
        self.assertContains(response, self.reqeust_test.response_text)
        self.assertTemplateUsed(response, 'request_delete.html')

        url = reverse('request_delete', kwargs={'pk': self.reqeust_test.pk + 1})
        null_response = self.client.get(url)
        self.assertEqual(null_response.status_code, 404)
