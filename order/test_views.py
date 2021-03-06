""" System Module """
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Box
from .models import Order, OrderBox, Address, Payment


class SetupModelTestCase(TestCase):
    """
    Base test case to be used in all models tests
    """

    def setUp(self):
        """ Setup for testing models """
        self.username = 'joe'
        self.password = '12345'
        self.user = User.objects.create_user(
            username=self.username,
            email='joe@doe.com',
            password=self.password)
        self.client.login(username='joe', password='12345')
        self.user2 = User.objects.create_user(
            username='joe2',
            email='joe2@doe.com',
            password='12345')
        self.billing_address1 = Address.objects.create(
            customer=self.user,
            address1='Apartment 1',
            address2='Parnell Street',
            county='Dublin',
            country='Ie',
            eircode='12345',
            address_type='B',
            default='True'
        )
        self.shipping_address1 = Address.objects.create(
            customer=self.user,
            address1='Apartment 2',
            address2='Parnell Street 2',
            county='Dublin 2',
            country='Ie',
            eircode='123456',
            address_type='S',
            default='True'
        )
        # Payment creation
        self.payment1 = Payment.objects.create(
            stripe_charge_id='123456789',
            customer=self.user,
            amount='900',
            timestamp='1643316725'
        )
        # Order creation
        self.order1 = Order.objects.create(
            customer=self.user,
            date_ordered='Oct. 24, 2021, 8:52 p.m.',
            billing_address=self.billing_address1,
            shipping_address=self.shipping_address1
            )
        self.shipping = True
        # Box creation
        self.box1 = Box.objects.create(
            box_name='testBox1',
            box_price=float('49.99'),
            category='Countries',
            box_description='test Box 1'
            )
        self.orderbox1 = OrderBox.objects.create(
            box=self.box1,
            order_box=self.order1,
            quantity=int('2')
            )
        self.checkout = {
                    'shipping_address1': self.shipping_address1.address1,
                    'shipping_address2': self.shipping_address1.address2,
                    'shipping_county': self.shipping_address1.county,
                    'shipping_country': self.shipping_address1.country,
                    'shipping_eircode': self.shipping_address1.eircode,
                    'billing_address1': self.billing_address1.address1,
                    'billing_address2': self.billing_address1.address2,
                    'billing_county': self.billing_address1.county,
                    'billing_country': self.billing_address1.country,
                    'billing_eircode': self.billing_address1.eircode,
                    }


class TestCheckoutView(SetupModelTestCase):
    """
    Checkout test class using payload from setup model class
    """
    def test_get_checkout(self):
        """
        Check if checkout data is correct and
        save checkout info
        """
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_post_if_form_is_valid(self):
        """
        Check if checkout data is correct and
        save checkout info
        """
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_valid_default_shipping(self):
        """
        Check if checkout data is correct and
        use default shiping address
        """
        self.checkout['use_default_shipping'] = True
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_valid_set_default_shipping(self):
        """
        Check if checkout data is correct and
        use default shiping address
        """
        self.checkout['set_default_shipping'] = True
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_not_valid_set_default_shipping(self):
        """
        Check if checkout data is correct and
        there is no default shiping address
        """
        self.shipping_address1.default = False
        self.shipping_address1.save()
        self.checkout['use_default_shipping'] = True
        payload = {
            'use_default_shipping': True,
            'use_default_billing': True
            }
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_not_valid(self):
        """
        Check if checkout data is not correct
        """
        self.checkout['use_default_shipping'] = False
        self.checkout['shipping_address1'] = ''
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_valid_and_use_same_billing_address(self):
        """
        Check if form is valid and use the same billing and
        shipping address
        """
        self.checkout['same_billing_address'] = True
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_valid_set_default_billing(self):
        """
        Check if checkout data is correct and
        user set default billing address
        """
        self.checkout['use_default_shipping'] = False
        self.checkout['same_billing_address'] = False
        self.checkout['use_default_billing'] = True
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_if_form_is_not_valid_set_default_billing(self):
        """
        Check if checkout data is not correct and
        user set default billing address
        """
        self.checkout['use_default_shipping'] = False
        self.checkout['same_billing_address'] = False
        self.checkout['use_default_billing'] = True
        self.billing_address1.default = False
        self.billing_address1.save()
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_set_default_billing(self):
        """
        Check set default billing address
        """
        self.checkout['set_default_billing'] = True
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_set_default_billing_not_valid(self):
        """
        Check set default billing address when form is not valid
        """
        self.checkout['use_default_billing'] = False
        self.checkout['billing_address1'] = ''
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)

    def test_post_with_no_order_valid(self):
        """
        Check exception if post without order valid
        """
        self.order1.ordered = True
        self.order1.save()
        payload = self.checkout
        response = self.client.post(reverse('checkout'), payload)
        self.assertEqual(response.status_code, 302)


class TestPaymentView(SetupModelTestCase):
    """
    Test all payment functions
    """
    def test_payment_view(self):
        """
        Test response on payment view page by url
        """
        url = reverse('payment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch("stripe.Charge.create")
    def test_payment_post(self, charge_mock):
        """
        Create a mock payment and check if redirect to correct url
        """
        charge_mock.return_value = {'id': "ch_XXXXX"}
        response = self.client.post(reverse('payment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/order/success/' + str(self.order1.id),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)


class TestSuccessView(SetupModelTestCase):
    """
    Test success view function
    """
    def test_get_success_payment(self):
        """
        Check if payment is successfull
        """
        response = self.client.get(reverse('success', args=[self.order1.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_success_payment_not_logged(self):
        """
        Check is client attemp to pay logged out
        """
        self.client.logout()
        self.client.login(username='joe2', password='12345')
        response = self.client.get(reverse('success', args=[self.order1.id]))
        self.assertEqual(response.status_code, 302)


class TestGetCheckoutView(SetupModelTestCase):
    """
    Checkout test class using payload from setup model class
    """
    def test_get_if_form_is_valid(self):
        """
        Check if checkout data is correct and
        save checkout info
        """
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)


class TestGetCheckoutSummaryView(SetupModelTestCase):
    """
    Checkout summary test class using payload from setup model class
    """
    def test_get_view(self):
        """
        Check if checkout summary view  is correct
        """
        response = self.client.get(reverse('checkout_summary'))
        self.assertEqual(response.status_code, 200)


class TestOrderDetailView(SetupModelTestCase):
    """
    OrderDetailView test class using payload from setup model class
    """
    def test_get_view(self):
        """
        Check if order detail view is correct
        """
        response = self.client.get(reverse('order_detail', kwargs={
            'pk': self.order1.id}))
        self.assertEqual(response.status_code, 200)
