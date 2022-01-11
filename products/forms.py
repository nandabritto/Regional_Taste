from django import forms

PRODUCT_CHOICES= [
    ('product1', 'PLACEHOLDER1'),
    (' product2', 'PLACEHOLDER2'),
    (' product3', 'PLACEHOLDER3'),
    (' product4', 'PLACEHOLDER4'),
    (' product5', 'PLACEHOLDER5'),
    
    ]

class UserForm(forms.Form):
    selected_product= forms.MultipleChoiceField(label='Choose the products for your box', widget=forms.CheckboxSelectMultiple,choices=PRODUCT_CHOICES)