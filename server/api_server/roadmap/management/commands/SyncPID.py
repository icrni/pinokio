import arrow

from django.core.management import BaseCommand
from django.conf import settings

from jira import JIRA

from roadmap.models import Issues, PIDLabel

class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"

    def handle(self, *args, **options):
        jira = JIRA(
            server='https://t-matix.atlassian.net',
            basic_auth=(settings.JIRA_USER, settings.JIRA_PASSWORD)
        )

        jql_str = 'project IN ("PID")'

        got = 50
        total = 0
        while got == 50:
            issues = jira.search_issues(
                jql_str=jql_str,
                startAt=total,
                fields='summary,status,issuetype,labels'
            )

            for issue in issues:
                print("Working on: {} {}".format(issue.key, issue.fields.summary))

                iss, created = Issues.objects.update_or_create(
                    key=issue.key,
                    defaults={
                        'status': issue.fields.status,
                        'name': issue.fields.summary,
                        'issue_type': issue.fields.issuetype,
                        'project': 'PID'
                    }
                )
                if created:
                    print("Updated!")

                iss.labels.clear()

                for label in issue.fields.labels:
                    lab, created = PIDLabel.objects.update_or_create(name=label)
                    iss.labels.add(lab)

            got = len(issues)
            total += got
            print('Got: {}, Total: {}'.format(got, total))
