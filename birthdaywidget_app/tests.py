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
        username = 'buhlen'

        APIRequestFactory().get('/api/v1/birthdays/' + username + '/')

        request1 	= APIRequestFactory().get('/api/v1/birthdays/' + username + '/')
        get_detail  = BirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1,username=username)

        self.assertEqual(response1.status_code,status.HTTP_200_OK)

    def testListingMonthBirthdays(self):
        """>>>test listing friend who are birthdaying on the specific month"""
        username = 'buhlen'
        month = 1

        APIRequestFactory().get('/api/v1/birthdays/'+username +'/'+ str(month)+'/')

        request1 	= APIRequestFactory().get('/api/v1/birthdays/'+ username +'/'+ str(month)+'/')
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1,username=username, month=unicode(month))

        self.assertEqual(response1.status_code,status.HTTP_200_OK)

    def testInvalidMonthBirthdays(self):
        """>>>test use wrong month"""
        username = 'buhlen'
        month = 13

        APIRequestFactory().get('/api/v1/birthdays/'+ username +'/'+ str(month)+'/')

        request1 	= APIRequestFactory().get('/api/v1/birthdays/'+ username +'/'+ str(month)+'/')
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1,username=username, month=unicode(month))

        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

    def testInvalidMonth(self):
        """>>>test use 3 digits for month"""
        username = 'buhlen'
        month= 123
        APIRequestFactory().get('/api/v1/birthdays/'+ username +'/'+ str(month)+'/')

        request1 	= APIRequestFactory().get('/api/v1/birthdays/'+ username +'/'+ str(month)+'/')
        get_detail  = MonthBirthdayListViewSet.as_view({'get': 'list'})

        response1 	= get_detail(request1,username=username, month=unicode(month))

        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

    def testListingDateBirthdays(self):
        """>>>test listing people who are birthdaying on the specific date"""
        username = 'phumi1'
        month = 10
        day = 1

        request1 	= APIRequestFactory().get('/api/v1/birthdays/'+ username +'/10/1/')
        get_detail  = DateBirthdayListViewSet.as_view({'get': 'list'})
        response1 	= get_detail(request1,username=username,month=unicode(month),day=unicode(day))

        self.assertEqual(response1.status_code,status.HTTP_200_OK)


