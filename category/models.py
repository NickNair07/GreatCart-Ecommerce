from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)


    # To change the plural name in the admin panel
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    # To get the url for each category listed in the navbar
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])        # products_by_category is from store.urls


    # To display the category name in admin panel
    def __str__(self):
        return self.category_name
    