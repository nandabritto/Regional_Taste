""" System Module """
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from products.models import Box
from user_profile.models import Address


class Order(models.Model):
    """
    Create order details and link it to the user
    """
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE)

    date_ordered = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, null=True, blank=False)
    billing_address = models.ForeignKey(
        'user_profile.Address', related_name='billing_address',
        on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'user_profile.Address', related_name='shipping_address',
        on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """
        Return a user string
        """
        return str(self.customer)

    def shipping(self):
        """
        Creates national or international shipping
        """
        national_shipping = settings.STANDART_SHIPPING_NATIONAL
        international_shipping = settings.STANDART_SHIPPING_INTERNATIONAL

        if self.shipping_address is not None:
            shipping_address = self.shipping_address

            if shipping_address.country == 'IE':
                shipping = national_shipping
            else:
                shipping = international_shipping
            return shipping
        else:
            shipping = 0
            return shipping

    @property
    def get_cart_total(self):
        """
        Get items and in the cart and sum to create cart total price
        """
        orderitems = self.orderbox_set.all().exclude(box__isnull=True)
        shipping = self.shipping()
        total = sum([item.get_total for item in orderitems], shipping)
        return total

    @property
    def get_cart_items(self):
        """
        Get items and in the cart and sum to create cart total items
        """
        orderitems = self.orderbox_set.all().exclude(box__isnull=True)
        total = sum([item.quantity for item in orderitems])
        return total


class OrderBox(models.Model):
    """
    Create orderbox details and quantity to add to the cart
    """
    box = models.ForeignKey(
        Box, on_delete=models.SET_NULL, blank=True, null=True)
    order_box = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    selected_products = models.CharField(max_length=500, null=True)

    class Meta:
        """
        Add correct plural name on Adress
        """
        verbose_name_plural = 'Ordered boxes'

    @property
    def get_total(self):
        """
        Multiply number of item to the box price to get total
        """
        total = self.box.box_price * self.quantity
        return total


class Payment(models.Model):
    """
    Create stripe payment
    """
    stripe_charge_id = models.CharField(max_length=50)
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string to payment
        """
        if self.customer:
            return str(self.customer.username)
        else:
            return str(self.stripe_charge_id)
