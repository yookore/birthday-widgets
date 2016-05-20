from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from birthdaywidget_app import views
from birthdaywidget_app.views import BirthdayListViewSet,DateBirthdayListViewSet,MonthBirthdayListViewSet
from birthdaywidget import settings

class BirthdayWidgetTestCase(TestCase):

    def setUp(self):
        pass

    def testListingTodayBirthdays(self):
        """>>>test listing friend who are birthdaying today"""

        APIRequestFactory().get('/api/v1/birthdays/')

        request1 	= APIRequestFactory().get("/api/v1/birthdays/buhlen/")
        get_detail  = BirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)

    def testListingDateBirthdays(self):

        request1 	= APIRequestFactory().get('/api/v1/birthdays/buhlen/10/1/')
        get_detail  = DateBirthdayListViewSet.as_view({'get': 'list'})
        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)
