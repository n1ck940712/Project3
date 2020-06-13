from django.db import models

# Create your models here.
class orderList(models.Model):
    order_number = models.IntegerField()
    ordered_by = models.CharField(max_length=64)
    order_status = models.CharField(max_length=64)
    def __str__(self):
        return f"Order #{self.order_number} | {self.ordered_by} | {self.order_status}"

class cart(models.Model):
    category = models.CharField(max_length=64)
    item = models.CharField(max_length=64)
    price = models.FloatField()
    order_number = models.ForeignKey("orderList", on_delete=models.CASCADE)
    add_on1 = models.CharField(max_length=64, null=True)
    add_on2 = models.CharField(max_length=64, null=True)
    add_on3 = models.CharField(max_length=64, null=True)
    remark = models.CharField(max_length=64, null=True)
    def __str__(self):
        return f"{self.category} | {self.item} - {self.price}"

class menuCategory(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class regularPizza(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()
    def __str__(self):
        return self.name

class sicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()
    def __str__(self):
        return f"{self.name} | S-{self.small} | L-{self.large}"

class pizzaToppings(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class dinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()
    def __str__(self):
        return self.name

class salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    def __str__(self):
        return self.name

class pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    def __str__(self):
        return self.name

class subs(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()
    def __str__(self):
        return self.name

class addOn(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    def __str__(self):
        return f"{self.name} | {self.price}"
