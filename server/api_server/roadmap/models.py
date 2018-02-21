from django.db import models


class PIDLabel(models.Model):
    name = models.CharField(max_length=200)


class Issues(models.Model):
    key = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    assignee = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    issue_type = models.CharField(max_length=200)
    epic_name = models.CharField(max_length=200, blank=True, null=True)
    epic_link = models.CharField(max_length=200, blank=True, null=True)
    timespent = models.CharField(max_length=200, blank=True, null=True)
    project = models.CharField(max_length=200, blank=True, null=True)
    labels = models.ManyToManyField(PIDLabel)
    linked_issues = models.ManyToManyField('self')


class Worklogs(models.Model):
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    worklog_id = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    start = models.DateField(blank=True, null=True)
    timeSpentSeconds = models.IntegerField()


class Worker(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)


class RemoteLink(models.Model):
    link_id = models.CharField(max_length=30)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)


class Comment(models.Model):
    comment_id = models.CharField(max_length=30)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    body = models.TextField()
    type = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
