from django.test import TestCase


class NewListTestCase(TestCase):
    def test_open_list_should_success(self):
        url = '/news/'
        response = self.client.get(path=url)
        # assert response.status_code == 200  # assert - утверждение, которое проверяет, является ли условие истинным
        self.assertEqual(response)