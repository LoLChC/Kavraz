from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
import os

class category(models.Model):
    title = models.CharField( max_length=50)
    images = models.ImageField(upload_to='category_images/')
    isActive = models.BooleanField()
    slug = models.SlugField(default="Otomatik-Doldurulacaktır", unique=True, db_index=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(args,kwargs)

    def __str__(self):
        return f"Kategorisi: {self.title}"


class products(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    images = models.ImageField(upload_to='product_images/')
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField()
    slug = models.SlugField(default="Otomatik-Doldurlacaktır", unique=True, db_index=True)
    featured = models.BooleanField()
    category = models.ForeignKey(category, default=111 ,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(args,kwargs)


    def __str__(self):
        return f"Adı: {self.title}, Fiyatı: {self.price}, Durumu: {self.isActive}, Ana Sayfada Listeleniyormu: {self.featured}, Slug:{self.slug} Kategorisi:{self.category}, Stok Miktarı:{self.stock}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    def item_price(self):
        return self.product.price * self.quantity

@receiver(pre_save, sender=products)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_images = products.objects.get(pk=instance.pk).images
    except products.DoesNotExist:
        return
    
    new_images = instance.images
    if old_images and old_images!= new_images:
        if os.path.isfile(old_images.path):
            os.remove(old_images.path)

@receiver(post_delete, sender=products)
def delete_image_on_product_delelte(sender, instance, **kwargs):
    if instance.images:
        if os.path.isfile(instance.images.path):
            os.remove(instance.images.path)

@receiver(pre_save, sender=category)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_images = products.objects.get(pk=instance.pk).images
    except products.DoesNotExist:
        return
    
    new_images = instance.images
    if old_images and old_images!= new_images:
        if os.path.isfile(old_images.path):
            os.remove(old_images.path)

@receiver(post_delete, sender=category)
def delete_image_on_product_delelte(sender, instance, **kwargs):
    if instance.images:
        if os.path.isfile(instance.images.path):
            os.remove(instance.images.path)


