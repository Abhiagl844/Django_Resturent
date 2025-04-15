from django.forms import ModelForm
from .models import food , user_details
from django.contrib.auth.models import User

class foodForm(ModelForm):
    class Meta:
        model = food
        fields = "__all__"
        exclude = []

class user_detailsForm(ModelForm):
    class Meta:
        model = user_details
        fields = ["user","email" , "phone" , "address"]
        exclude = ["user"]