from django.conf.urls import patterns,url
from django.conf.urls.static import static
from birthdaywidget_app import views
from birthdaywidget_app.views import *

birthday = BirthdayListViewSet.as_view({
    'get': 'list'
})

month = MonthBirthdayListViewSet.as_view({
    'get': 'list'
})

date = DateBirthdayListViewSet.as_view({
    'get': 'list'
})

test = ListViewSet.as_view({
    'get': 'list'
})



urlpatterns = patterns('',
    url(r'^birthdays/(?P<username>[\w.-]+)/$', birthday ,name='birthday-list'),

    url(r'^birthdays/(?P<username>[\w.-]+)/(?P<month>[0-9]+)/$', month ,name='month-list'),

    url(r'^birthdays/(?P<username>[\w.-]+)/(?P<month>[0-9]+)/test/$', test ,name='month-list'),

    url(r'^birthdays/(?P<username>[\w.-]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', date ,name='date-list'),
)