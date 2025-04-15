from django.db import models
from django.contrib.auth.models import User


class user_details(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    email = models.EmailField(null=False , blank=False)
    phone = models.IntegerField(null=False , blank= False)
    address = models.CharField(max_length=120 , blank=False , null=False)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class food(models.Model):
    class type_choice(models.TextChoices):
        nv = "NON-VEG"
        v = "VEG"

    class course_choice(models.TextChoices):
        appe = "Appetizer"
        soup = "Hot Hot Soup"
        starter = "Indian Starter"
        salad = "Salad, Papad And Raita"
        Rice = "Rice"
        bread = "Breads"
        chi = "Chinese"
        tand = "Tandoor"
        Main_veg = "Main Course Veg"
        Main_nv = "Main Course Non-Veg"
        Desert = "Desert"

    name = models.CharField(max_length = 30 , blank=False)
    ingredients = models.JSONField()
    image = models.ImageField(blank=True)
    price = models.IntegerField(blank=False)
    type = models.CharField(max_length=7 ,choices=type_choice , null=True , blank=True)
    course = models.CharField(max_length = 25 , choices=course_choice , null = True , blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create your models here.


class Review(models.Model):
    class Rating(models.IntegerChoices):
        Poor = 1 , "Poor"
        Ok = 2 , "Ok"
        Average = 3 , "Average"
        Good = 4 , "Good"
        Great = 5 , "Great"

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    food = models.ForeignKey(food , on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.IntegerField(choices=Rating.choices , null = False , blank= False)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]
    
class orders(models.Model):
    class stat(models.TextChoices):
        queue = "In Queue"
        making = "Preparing!"
        completed = "Prepared."
        out = "Out For Delevery"
        done = "Delivered"

    choices = [(i+1, i+1) for i in range(10)]

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    user_details = models.ForeignKey(user_details, on_delete=models.CASCADE)
    item = models.ManyToManyField(food)
    quant = models.IntegerField(choices=choices ,null=False , blank=False , default=1)
    status = models.CharField(max_length=17 , choices=stat , default=stat.queue)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
