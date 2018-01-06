from datetime import datetime, timedelta
from django.db.models import Sum, Q
from rest_framework import serializers, viewsets
from django.http import JsonResponse
from django.views.generic import View

from .models import Issues, Worklogs, Worker, Comment


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issues
        fields = ('id', 'key', 'name', 'assignee')


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer


class Days(View):

    def get(self, request, **kwargs):
        from_ts = datetime.fromtimestamp(int(kwargs['from_ts']))
        to_ts = datetime.fromtimestamp(int(kwargs['to_ts']))

        workers = Worker.objects.all()

        issues = Issues.objects.filter(
            Q(start_date__isnull=False, assignee__isnull=False),
            Q(start_date__lte=from_ts, end_date__gte=from_ts) |
            Q(start_date__lte=to_ts, end_date__gte=to_ts) |
            Q(start_date__gte=from_ts, end_date__lte=to_ts)
        )
        response = {}

        for worker in workers:
            response[worker.name] = {}

        for issue in issues:
            if issue.assignee not in response:
                continue

            dt = issue.end_date - issue.start_date

            for n in range(0, dt.days + 1):

                date = (issue.start_date + timedelta(days=n))
                date_formated = date.strftime("%d.%m.%Y")
                if date_formated not in response[issue.assignee]:
                    response[issue.assignee][date_formated] = []

                logged = Worklogs.objects.filter(
                    issue=issue, start=date
                ).annotate(total=Sum('timeSpentSeconds')).first()

                if logged:
                    logged = logged.total / 3600
                else:
                    logged = 0

                commits = Comment.objects.filter(
                    issue=issue, type='Commit', created=date
                ).count()

                response[issue.assignee][date_formated].append(
                    {
                        'key': issue.key,
                        'logged': '{:.2f}'.format(logged),
                        'status': issue.status,
                        'commits': commits
                    }
                )

        return JsonResponse(
            response,
            status=200
        )
