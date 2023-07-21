from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


# Create your views here.
def store(request, category_slug=None):     # None is set to avoid getting error while loading the store page without slug 

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)

        # pagination for category vised products
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)

        # pagination for all products
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'count': product_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    # By using (category__slug), we can access the slug field in the Category model. because category is foriegnkey of Product.
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:                                                         # Q is used as alternative for (OR) in django
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'count': product_count,
    }
    return render(request, 'store/store.html', context)