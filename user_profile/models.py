""" System Module """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_countries.fields import CountryField


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    """
    Create user profile with dfaul info
    """

    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address1',
        on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address2',
        on_delete=models.SET_NULL, blank=True, null=True)
    # default_address1 = models.CharField(max_length=100, null=True, blank=True)
    # default_address2 = models.CharField(max_length=100, null=True, blank=True)
    # default_county = models.CharField(max_length=20, null=True, blank=True)
    # default_country = CountryField(multiple=False, null=True, blank=True)
    # default_eircode = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        """
        Return string
        """
        return self.customer.username


class Address(models.Model):
    """
    Create address details and link to the user and order
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    county = models.CharField(max_length=20)
    country = CountryField(multiple=False)
    eircode = models.CharField(max_length=7)
    address_type = models.CharField(
        max_length=1,
        choices=ADDRESS_CHOICES,
        default='S')
    default = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     previous_address = self.objects.filter(
    #         customer=self.customer,
    #         address1 = self.address1,
    #         address2 = self.address2,
    #         county = self.county,
    #         country = self.country,
    #         eircode = self.eircode,
    #         address_type = self.address_type
    #         )
    #     if previous_address.exists():
    #         previous_address = self.default
    #         super(Address, previous_address).update(*args, **kwargs)
    #     else:
    #         super(Address, self).save(*args, **kwargs)

    def __str__(self):
        """
        Return a string to billing address
        """
        return str(self.customer)

    class Meta:
        """
        Add correct plural name on Adress
        """
        verbose_name_plural = 'adresses'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(customer=instance)
    instance.userprofile.save()

