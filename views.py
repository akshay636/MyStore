from django.db.models.expressions import Expression
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
# Create your views here.
def home(request):
    # products= Product.objects.all()
    # n= len(products)
    # nSlides= n//4 + ceil((n/4)-(n//4))
    # allProds=[[products, range(1, len(products)), nSlides],[products, range(1, len(products)), nSlides]]
    # params={'allProds':allProds }
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'stores/index.html', params)

def about(request):
    return render(request, 'stores/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request, 'stores/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'stores/tracker.html')


def search(request):
    return render(request, 'stores/search.html')

def products(request,myid):
    product=Product.objects.filter(id=myid)
    return render(request, 'stores/productdetails.html',{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update=OrderUpdate(order_id=order.order_id , update_desc="your order has been ready to ship..!")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'stores/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'stores/checkout.html')

   