from django.conf.urls import url, include
from rest_framework import routers
from roadmap.views import IssueViewSet, Days, LabelCosts, Costs, WeeklyCosts


router = routers.DefaultRouter()
router.register(r'issues', IssueViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url('^days/(?P<from_ts>[0-9]{10})/(?P<to_ts>[0-9]{10})/', Days.as_view(), name='days_view'),
    url('^labels/', LabelCosts.as_view(), name='label_costs_view'),
    url('^costs/', Costs.as_view(), name='costs_view'),
    url('^weekcosts/', WeeklyCosts.as_view(), name='week_costs_view')
]
