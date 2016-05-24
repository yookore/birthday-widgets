from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from birthdaywidget_app import views
from birthdaywidget_app.views import BirthdayListViewSet,DateBirthdayListViewSet,MonthBirthdayListViewSet
from birthdaywidget import settings

class BirthdayWidgetTestCase(TestCase):

    def setUp(self):
        self.username= 'buhlen'

    def testListingTodayBirthdays(self):
        """>>>test listing friend who are birthdaying today"""

        APIRequestFactory().get('/api/v1/birthdays/buhlen/')

        request1 	= APIRequestFactory().get("/api/v1/birthdays/buhlen/")
        get_detail  = BirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)

    def testListingMonthBirthdays(self):
        """>>>test listing friend who are birthdaying on the specific month"""

        APIRequestFactory().get('/api/v1/birthdays/buhlen/1/')

        request1 	= APIRequestFactory().get("/api/v1/birthdays/buhlen/1/")
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)

    def testInvalidMonthBirthdays(self):
        """>>>test use wrong month"""

        APIRequestFactory().get('/api/v1/birthdays/buhlen/13/')

        request1 	= APIRequestFactory().get("/api/v1/birthdays/buhlen/13/")
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

    def testInvalidMonth(self):
        """>>>test use 3 digits for month"""

        APIRequestFactory().get('/api/v1/birthdays/buhlen/133/')

        request1 	= APIRequestFactory().get("/api/v1/birthdays/buhlen/133/")
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

    def testListingDateBirthdays(self):
        """>>>test listing people who are birthdaying on the specific date"""

        request1 	= APIRequestFactory().get('/api/v1/birthdays/buhlen/'+str(10)+'/'+str(1)+'/')
        get_detail  = DateBirthdayListViewSet.as_view({'get': 'list'})
        response1 	= get_detail(request1)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)


