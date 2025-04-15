from django.forms import ModelForm
from .models import cartItems , cartSes
from django.db.models import Q


class cartForm(ModelForm):
    class Meta:
        model = cartItems
        fields = ["quantity"]
#        constraints = [
 #           model.cart == cartSes.id,
  #      ]

