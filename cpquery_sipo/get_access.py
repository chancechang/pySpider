import urllib, urllib2, sys
import ssl
AK='MYAp2QPym4jn1smIlGVyGVEC'
SK='lxDIewGKhNrKWijeBTcz7UVVVQxZmCNi'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+AK+'&client_secret='+SK
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)