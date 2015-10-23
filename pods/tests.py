from rest_framework.test import APIRequestFactory

# Create your tests here.

factory = APIRequestFactory()\

account = factory.post('/api/accounts', {'username': 'test', 'password': 'test', 'email': 'test@exeter.edu'})

print account