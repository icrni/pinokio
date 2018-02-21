from datetime import datetime, timedelta
from collections import deque
from django.db.models import Sum, Q
from rest_framework import serializers, viewsets
from django.http import JsonResponse
from django.views.generic import View
import arrow

from .models import Issues, Worklogs, Worker, Comment, PIDLabel


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

        workers = Worker.objects.filter(is_active=True)

        issues = Issues.objects.filter(
            Q(start_date__isnull=False, assignee__isnull=False),
            Q(start_date__lte=from_ts, end_date__gte=from_ts) |
            Q(start_date__lte=to_ts, end_date__gte=to_ts) |
            Q(start_date__gte=from_ts, end_date__lte=to_ts)
        ).exclude(issue_type='Epic', project='PID')
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


class LabelCosts(View):

    def get(self, request, **kwargs):
        workers = {}
        for wr in Worker.objects.all():
            workers[wr.name] = wr.cost

        result = {}
        costs = {}
        for label in PIDLabel.objects.all():
            result[label.name] = []
            for issue in Issues.objects.filter(
                    linked_issues__in=Issues.objects.filter(project='PID', labels=label)
            ):
                try:
                    if issue.issue_type == 'Epic':
                        result[label.name] = result[label.name] + [
                            (w.start, (w.timeSpentSeconds/3600) * workers[issue.assignee])
                            for w in Worklogs.objects.filter(
                                issue__in=Issues.objects.filter(epic_link=issue.key)
                            )]
                    elif issue.issue_type == 'Story':
                        result[label.name] = result[label.name] + [
                            (w.start, (w.timeSpentSeconds/3600) * workers[issue.assignee])
                            for w in Worklogs.objects.filter(
                                issue=issue
                            )]
                except:
                    pass

            data = deque((date, cost) for date, cost in sorted(result[label.name], key=lambda t:t[0]))

            grouped = {}
            while data:
                week = data[0][0] - timedelta(days=(data[0][0].isocalendar()[2] - 1))
                temp = [data.popleft()]
                while data and week.isocalendar()[:2] == data[0][0].isocalendar()[:2]:
                    temp.append(data.popleft())

                key = 'ISO week {}-W{:02}'.format(*week.isocalendar()[:2])
                key += ' ({} - {})'.format(week.strftime('%Y-%m-%d'),
                                           (week + timedelta(days=6)).strftime('%Y-%m-%d'))

                grouped[key] = sum(t[1] for t in temp)

            costs[label.name] = grouped

        return JsonResponse(
            costs,
            status=200
        )


class Costs(View):

    def get(self, request, **kwargs):
        workers = {}
        for wr in Worker.objects.all():
            workers[wr.name] = wr.cost

        result = []
        for label in PIDLabel.objects.all():
            for PID in Issues.objects.filter(project='PID', labels=label):
                for issue in Issues.objects.filter(
                        linked_issues=PID
                ):
                    try:
                        if issue.issue_type == 'Epic':
                            result = result + [{
                                'year': arrow.Arrow.fromdate(w.start).isocalendar()[0],
                                'week': arrow.Arrow.fromdate(w.start).isocalendar()[1],
                                'cost': round((w.timeSpentSeconds/3600) * workers[issue.assignee]),
                                'PID': PID.key,
                                'label': label.name
                            } for w in Worklogs.objects.filter(
                                    issue__in=Issues.objects.filter(epic_link=issue.key)
                                )]
                        elif issue.issue_type == 'Story':
                            result = result + [{
                                'year': arrow.Arrow.fromdate(w.start).isocalendar()[0],
                                'week': arrow.Arrow.fromdate(w.start).isocalendar()[1],
                                'cost': round((w.timeSpentSeconds / 3600) * workers[issue.assignee]),
                                'PID': PID.key,
                                'label': label.name
                            } for w in Worklogs.objects.filter(
                                    issue=issue
                                )]
                    except:
                        pass
        print(result)
        return JsonResponse(
            result,
            status=200, safe=False
        )
