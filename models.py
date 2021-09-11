from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_id=models.AutoField
    desc=models.CharField(max_length=200)
    pub_date=models.DateField
    category=models.CharField(max_length=30)
    subcategory=models.CharField(max_length=30)
    image=models.ImageField(upload_to="stores/images")
    price=models.CharField(max_length=100)

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    name=models.CharField(max_length=60,default="")
    msg_id= models.AutoField(primary_key=True)
    phone=models.CharField(max_length=15,default="")
    email=models.CharField(max_length=70,default="")
    desc=models.CharField(max_length=500,default="")
    

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=8000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

class OrderUpdate(models.Model):
    order_id= models.IntegerField(default="")
    update_id=models.AutoField(primary_key=True)
    update_desc= models.CharField(max_length=5000,default="")
    timetamp= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:9]+"..."



