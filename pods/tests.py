from rest_framework.test import APIClient
from time import time

# Create your tests here.

client = APIClient()

account = client.post('/api/accounts/', {'username': ('test' + str(int(time()))), 'password': 'test', 'email': 'test@exeter.edu'})
client.credentials(HTTP_AUTHORIZATION='JWT ' + account.data['token'])
pod = client.post('/api/pods/', {'name': 'test' + str(int(time()))})

print "get", client.get('/api/pods/' + str(pod.data['id']))

print account.data, pod.data