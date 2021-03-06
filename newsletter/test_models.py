""" System Module """
from django.test import TestCase
from .models import NewsletterUser, Newsletter


class SetupModelTestCase(TestCase):
    """
    Base test case to be used in all models tests
    """
    def setUp(self):
        """
        Setup for testing models
        """
        self.email = 'joe@email.com'
        self.subject = 'Test Subject'
        self.body = 'Test Body'
        self.nlu = NewsletterUser.objects.create(email=self.email)


class NewsletterUserTestCase(SetupModelTestCase):
    """
    Test NewsletterUser model function
    """
    def test__str__(self):
        """
        Test if newsletter user is returning correct string
        """
        self.assertEqual(str(self.nlu), 'joe@email.com')


class NewsletterTestCase(SetupModelTestCase):
    """
    Test Newsletter models function
    """
    def test__str__(self):
        """
        Test if newsletter is returning correct string
        """
        news = Newsletter.objects.create(
            subject=self.subject,
            body=self.body,
            )
        self.assertEqual(str(news), 'Test Subject')
