from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_type = request.GET.get('sort')
    all_phones = []
    if sort_type is None:
        all_phones = Phone.objects.all()
    elif sort_type == 'name':
        all_phones = Phone.objects.order_by('name')
    elif sort_type == 'min_price':
        all_phones = Phone.objects.order_by('price')
    elif sort_type == 'max_price':
        all_phones = Phone.objects.order_by('price').reverse()
    context = {
        'phones': all_phones
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {
        'phone': phone
    }
    return render(request, template, context)
