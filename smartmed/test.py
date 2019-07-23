from django.test import TestCase
from django.test.client import Client


class AdminTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/admin', follow = True) 
        self.assertEqual(response.status_code, 200)

class AccountsTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/login', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardEmployeeListTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/employee/list', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardEmployeeCreateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/employee/create', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardEmployeeUpdateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/employee/update/123', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardEmployeeSelfUpdateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/employee/self_update', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardPartnerListTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/partner/list', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardPartnerCreateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/partner/create', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardPartnerUpdateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('/dashboard/partner/update/123', follow = True) 
        self.assertEqual(response.status_code, 200)

class DashboardPartnerUpdateTest(TestCase):
    def setUp(self): 
        self.client = Client()

    def test(self):
        response = self.client.get('dashboard/partner/self_update', follow = True) 
        self.assertEqual(response.status_code, 200)

