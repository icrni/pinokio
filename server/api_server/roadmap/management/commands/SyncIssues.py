import arrow

from django.core.management import BaseCommand
from django.conf import settings

from jira import JIRA

from roadmap.models import Issues, Worklogs, RemoteLink, Comment

class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"

    def handle(self, *args, **options):
        jira = JIRA(
            server='https://t-matix.atlassian.net',
            basic_auth=(settings.JIRA_USER, settings.JIRA_PASSWORD)
        )

        jql_str = 'project IN ({})'.format(','.join(settings.JIRA_PROJECTS))

        got = 50
        total = 0
        while got == 50:
            issues = jira.search_issues(
                jql_str=jql_str,
                startAt=total,
                fields='worklog,comment,issuelinks,summary,assignee,timespent,status,issuetype,customfield_10007,customfield_10008,customfield_11403,customfield_11404'
            )

            for issue in issues:
                print("Working on: {} {}".format(issue.key, issue.fields.summary))
                epic = None
                epic_link = None

                try:
                    epic = issue.fields.customfield_10008
                except AttributeError:
                    pass

                try:
                    epic_link = issue.fields.customfield_10007
                except AttributeError:
                    pass

                iss, created = Issues.objects.update_or_create(
                    key=issue.key,
                    defaults={
                        'assignee': issue.fields.assignee,
                        'status': issue.fields.status,
                        'start_date': issue.fields.customfield_11403,
                        'end_date': issue.fields.customfield_11404,
                        'name': issue.fields.summary,
                        'issue_type': issue.fields.issuetype,
                        'epic_name': epic,
                        'epic_link': epic_link,
                        'timespent': issue.fields.timespent
                    }
                )
                if created:
                    print("Updated!")

                for worklog in issue.fields.worklog.worklogs:
                    wlog, created = Worklogs.objects.update_or_create(
                        worklog_id=worklog.id,
                        defaults={
                            'issue': iss,
                            'author': worklog.author,
                            'start': arrow.get(worklog.started).datetime,
                            'timeSpentSeconds': worklog.timeSpentSeconds
                        }
                    )
                for comt in issue.fields.comment.comments:
                    if 'commit' in comt.body:
                        type = 'Commit'
                    elif 'merge request' in comt.body:
                        type = 'Merge Request'
                    else:
                        continue

                    comm, created = Comment.objects.update_or_create(
                        comment_id=comt.id,
                        defaults={
                            'issue': iss,
                            'body': comt.body,
                            'created': arrow.get(comt.created).datetime,
                            'type': type
                        }
                    )

                # remotelinks = jira.remote_links(issue.key)
                # for link in remotelinks:
                #     linkraw =link.raw['object']
                #     if 'name' in link.raw['application'] and link.raw['application']['name'] == 'Confluence':
                #         continue
                #     if 'title' in linkraw and 'url' in linkraw:
                #         rtype = 'unknown'
                #         if "GitLab: Mentioned on commit" in linkraw['title']:
                #             rtype = 'Commit'
                #         if "GitLab: Mentioned on merge request" in linkraw['title']:
                #             rtype = 'Merge request'
                #
                #         rlink, created = RemoteLink.objects.update_or_create(
                #             link_id=link.id,
                #             defaults={
                #                 'issue': iss,
                #                 'title': linkraw['title'],
                #                 'url': linkraw['url'],
                #                 'type': rtype
                #             }
                #         )

            got = len(issues)
            total += got
            print('Got: {}, Total: {}'.format(got, total))
