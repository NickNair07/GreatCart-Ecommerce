from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name  = models.CharField(max_length=200, unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=500, blank=True)
    price         = models.IntegerField()
    images        = models.ImageField(upload_to='photos/products')
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)    # models.CASCADE is used to delete the product-
                                                                                        # when the category is deleted
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # To get the url for each product single page
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)   # is_active is used to disable any variation if we want!
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):  # unicode instead of str. because product is not a string
        return self.variation_value
    