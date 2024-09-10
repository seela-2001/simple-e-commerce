from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MinValueValidator
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100,null = False,blank=False,
                            validators=[MinLengthValidator(3)])
    user = models.ForeignKey(User ,on_delete=models.CASCADE,null=True)
    image = models.ImageField(null=True,blank=True,default="/placeholder.png",upload_to="store\static\images\product_images")
    brand = models.CharField(max_length=100,null=True,blank=True,validators=[MinLengthValidator(3)])
    category = models.CharField(max_length=100,null=True,blank=True,validators=[MinLengthValidator(5)])
    description = models.TextField(null=True,blank= True)
    rating = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    num_reviews = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    price = models.FloatField(default=0,validators=[MinValueValidator(0)])
    count_in_stock = models.IntegerField(null=False,default = 0,validators = [MinValueValidator(0)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        constraints = [
            models.UniqueConstraint(fields=['name'],name = "unique_product_name"),
            models.CheckConstraint(check=models.Q(rating__gte=0)&models.Q(rating__lte=5),name="valid_rating"),
            models.CheckConstraint(check=models.Q(price__gte=0),name="non_negative_price"),
            models.CheckConstraint(check=models.Q(num_reviews__gte=0),name='non_negative_num_review'),
            models.CheckConstraint(check=models.Q(count_in_stock__gte=0),name='non_negative_count_in_stock')   
        ]


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_review')
    text = models.TextField(max_length=300,null=True,blank=True)
    rating = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    payment_methods_choices = [
        ("visa",'visa') ,
        ("cash",'cash') , 
        ("fawry",'fawry')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100,default='visa',choices=payment_methods_choices)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False) 
    paid_at = models.DateTimeField(null=True)
    delivered_at = models.DateField(null=True)
    price = models.FloatField(default=0)
    shipping_price = models.FloatField(default=50)
    total_price = models.FloatField(default=0)
    tax_price = models.FloatField(default = 0)

class OrderItem(models.Model):
    product = models.ManyToManyField(Product, through='Order_Products')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    price = models.FloatField(default=0)



class Order_Products(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    orderitem = models.ForeignKey(OrderItem,on_delete=models.CASCADE)


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='order_shipping')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()


