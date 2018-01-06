from django.conf.urls import url, include
from rest_framework import routers
from roadmap.views import IssueViewSet, Days


router = routers.DefaultRouter()
router.register(r'issues', IssueViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url('^days/(?P<from_ts>[0-9]{10})/(?P<to_ts>[0-9]{10})/', Days.as_view(), name='days_view')
]
