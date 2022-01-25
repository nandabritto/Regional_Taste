""" System Module """
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .forms import CheckoutForm
from .models import Order, Address, OrderBox, Payment
from django.core.exceptions import ObjectDoesNotExist
import stripe 
from django.conf import settings
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY

def order(request):
    """
    A view to return order page
    """
    return render(request, 'order/order.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(
                customer=customer, ordered=False)
            items = order.orderbox_set.all()
            cartItems = order.get_cart_items
            context = {
                'form': form,
                'items': items, 
                'order': order, 
                'cartItems': cartItems,
                # 'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                # 'client_secret' : settings.CLIENT_SECRET
            }
            return render(self.request, 'order/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                county = form.cleaned_data.get('county')
                country = form.cleaned_data.get('country')
                eircode = form.cleaned_data.get('eircode')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                billing_address = Address(
                    customer = self.request.user,
                    address1 = address1,
                    address2 = address2,
                    county = county,
                    country = country,
                    eircode = eircode,
                    address_type = 'B'                
                )
                print(billing_address)
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect("cart")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order" )
            return redirect("cart")


class PaymentView(View):

    def get (self, *args, **kwargs):
        return render(self.request, "order/payment.html")

    def post(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)

        token = self.request.POST.get('stripeToken')
        amount = int(order.get_cart_total * 100)


        try:
            charge = stripe.Charge.create(
            amount = amount,
            currency = "eur",
            source=token,
        )


            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.customer = self.request.user
            payment.amount = order.get_cart_total
            payment.save()


            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful")
            return redirect("/")



        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}") 
            return redirect("/")

        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.error(self.request, "Rate Limited Error") 
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameter") 
            return redirect("/")

        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated") 
            return redirect("/")

        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.error(self.request, "Network error") 
            return redirect("/")

        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.error(self.request, "Something went wrong, you were not charged. Try again.") 
            return redirect("/")

        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "A serious error occurred.") 
            return redirect("/")


       
        





        
