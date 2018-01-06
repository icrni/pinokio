import urllib
import urllib2
import cookielib
import json

jira_serverurl = "https://t-matix.atlassian.net"
creds = { "username" : "igor.crnkovic@t-matix.com", "password" : "M4verick" }
authurl = jira_serverurl + "/rest/auth/latest/session"

# Get the authentication cookie using the REST API
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
req = urllib2.Request(authurl)
req.add_data('{ "username" : "igor.crnkovic@t-matix.com", "password" : "M4verick" }')
req.add_header("Content-type", "application/json")
req.add_header("Accept", "application/json")
fp = opener.open(req)
fp.close()

add_component_url = jira_serverurl + "/rest/api/2/field"

request = urllib2.Request(add_component_url)
fp = opener.open(request)

json = json.loads(fp.read())
for field in json:
    print(field['name'].encode('utf8'),field['id'].encode('utf8'))
