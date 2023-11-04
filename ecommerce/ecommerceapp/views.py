from django.shortcuts import render
from ecommerceapp.models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WishList,Address
from django.db.models import Count,Avg
from ecommerceapp.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.core import serializers


# Create your views here.
def index(request):
    products = Product.objects.all().order_by("-pid")
    Categories =  Category.objects.all()

    cart_total_amount = 0
    cart_data_pids = []
    
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            cart_data_pids.append(p_id)  # Add p_id to the list

    context= {
        "products":products,
        "categories":Categories,
        "cart_data_pids": cart_data_pids,  
    }
    return render(request, "index.html", context)



def product_list_view(request):
    products = Product.objects.all()
    # products = Product.objects.filter(featured="True")
    context= {
        "products":products
    }

    return render(request, "shop-top-filter.html", context)
 

def category_list_view(request):
    Categories =  Category.objects.all()
    products = Product.objects.all().order_by("-pid")
    context = {
        "categories":Categories,
        "products":products
    }
    return render(request, 'shop-category.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=category)

    context = {
        "category" : category,
        "products" : product,
    }
    return render(request, "shop-top-filter.html", context)

def vendor_list_view(request):
    vendor = Vendor.objects.all()
    context = {
        "vendor" : vendor
    }    
    return render(request, "vendor/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor)
    context = {
        "v" : vendor,
        "products" : products,
    }    
    return render(request, "vendor/vendor-detail.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    vendor_name = product.vendor
    vendor = Vendor.objects.get(title=vendor_name)
    products = Product.objects.all()
    p_images = product.p_images.all()
    reviews = ProductReview.objects.filter(product=product).order_by("date")
    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    

    make_review = True
    if request.user.is_authenticated:
        user_rev_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_rev_count > 0:
                make_review = False


    context = {
        "product": product,
        "vendor": vendor,
        "products": products,
        "p_images": p_images,
        "reviews" : reviews,
        "make_review" : make_review,
        "avg_rating": avg_rating,
        "review_form": review_form,
        
    }    
    return render(request, "product-detail.html", context)


def ajax_add_review(request, pid):
    r_product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        review = request.POST['review'],
        rating = request.POST['rating'],
        product=r_product,
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating' : request.POST['rating'],    
    }
    
    avg_rating = ProductReview.objects.filter(product=r_product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {   
        'bool':True,
        'context' : context,
        'avg_rating' : avg_rating
        } 
    )
    

def search_view(request):
     # Get the 'q' parameter from the GET request
    query = request.GET.get('q',)
    # products = Product.objects.filter((title__icontains = query) | (description__icontains = query)).order_by("-date")
    products = Product.objects.filter(title__icontains=query) | Product.objects.filter(description__icontains=query).order_by("-date")



    context = {
        "products": products,
        "query" : query,
    } 
    return render(request, "search.html", context)



def filter_product(request):
    categories=request.GET.getlist("category[]")
    vendor=request.GET.getlist("vendor[]")

    products = Product.objects.all().order_by("-date").distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in = categories).distinct() # Category__id is  category id  inProduct table it is chaced in categories fron jason

    if len(vendor) > 0:
        products = products.filter(vendor__id__in = vendor).distinct()

    context = {
        "products":products
    }    

    data = render_to_string("async/product-list.html",context)    
    data2 = render_to_string("async/product-list-2.html",context)    
    return JsonResponse({"data": data,"data2": data2})




@login_required
def view_wishlist(request):
    # try:
    wishList = WishList.objects.filter(user=request.user)
    # except:
    #     wishList = None

    context = {
        "w": wishList
    }    

    return render(request,"wishlist.html",context)

@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {

    }

    wishList_count= WishList.objects.filter(product=product, user=request.user).count()
    print(wishList_count)

    if wishList_count >0 :
        context = {
            "bool": True
        }
    else:
        new_wishlist = WishList.objects.create(
            product = product,
            user=request.user
        )

        context = {
            "bool": True
        }
    data = render_to_string("async/wishlist-btn.html",context)    
    return JsonResponse({"bool": True,"data":data})

def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = WishList.objects.filter(user=request.user)

    product = WishList.objects.get(id=pid)
    product.delete()

    context = {
        "bool": True,
        "w":wishlist,

    }
    wishlist_json = serializers.serialize('json',wishlist)
    data = render_to_string("async/wishlist.html",context)
    return JsonResponse({"data":data,"w":wishlist_json})

def remove_wishlist_index(request):
    pid = request.GET['id']
    wishlist = WishList.objects.filter(user=request.user)

    product = WishList.objects.get(id=pid)
    product.delete()

    context = {
        "bool": True,
        "w":wishlist,

    }
    wishlist_json = serializers.serialize('json',wishlist)
    data = render_to_string("async/wishlist-index.html",context)
    return JsonResponse({"data":data,"w":wishlist_json})

def add_to_cart(request):
    
    # Initialize the cart_data if it doesn't exist in the session.
    cart_data = request.session.get('cart_data_obj', {})

    product_id = request.GET.get('id')
    product_qty = float(request.GET.get('qty'))


    if product_id in cart_data:
        # Product is already in the cart, update the quantity.
        cart_data[product_id]['qty'] += product_qty
    else:
        # Product is not in the cart, add it.
        cart_data[product_id] = {
            'image': request.GET.get('image'),
            'title': request.GET.get('title'),
            'weight': request.GET.get('weight'),
            'qty': product_qty,
            'price': request.GET.get('price'),
            'pid': request.GET.get('pid'),
            'oldprice': request.GET.get('oldprice'),
            'savingprice': request.GET.get('savingprice'),
            'tprice': request.GET.get('tprice'),
        }

    # Update the cart data in the session.
    request.session['cart_data_obj'] = cart_data
    request.session.save()


    rendered_cart_list = render_to_string("async/header-cart-list.html", {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),   
    })

    # return JsonResponse({"data": cart_data, 'totalcartitems': len(cart_data)})

    return JsonResponse({"data": cart_data, 'totalcartitems': len(cart_data), 'rendered_cart_list': rendered_cart_list})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])   

        return render(request,"cart.html",({"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}))
    else:
        messages.warning(request, "Your cart is empty")
        return render(request,"index.html")
    

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])   

    context = render_to_string("async/cart-list.html",({"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}))    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})
        
def update_qty(request):

    product_id = str(request.GET['id'])
    product_qty = str(request.GET['qty'])
    product_price_total = str(request.GET['product_price_total'])
    product_price_total

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            sub_item_total_amount = product_price_total   

    context = render_to_string("async/cart-list.html",({"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])}))    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'sub_item_total_amount':sub_item_total_amount})
 

@login_required
def checkout_view(request):

    host = request.get_host()
    paypal_dict = {
        "business": 'harikrishnananilkumar18@gmail.com',
        "amount" : '1',
        "item_name": "Order=Item-No-3",
        "invoice": "INVOICE_NO-3",
        "currency_code": "USD",
        "notify_url": 'http://{}{}'.format(host, reverse("ecommerceapp:paypal-ipn")),
        "return_url": 'http://{}{}'.format(host, reverse("ecommerceapp:payment-completed")),
        "cancel_url": 'http://{}{}'.format(host, reverse("ecommerceapp:payment-failed")),
       
    }


    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)




    cart_total_amount = 0
    shipping = 10.05
    tax = 5.5



    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            shipping *= int(item['qty'])
            tax *= int(item['qty'])
            final_amount = cart_total_amount + shipping + tax
              

        return render(request, "checkout.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'shipping':shipping,
            'tax':tax,
            'final_amount':final_amount,
            'paypal_payment_button':paypal_payment_button,

        })
    else:
        # Handle the case when 'cart_data_obj' is not in the session
        messages.warning(request, "Your cart is empty")
        return render(request, "cart.html")


def payment_complete_view(request):
    return render(request,"order-success.html")

def payment_failed_view(request):
    return render(request,"order-success.html")

def invoice_view(request):
    return render(request,"order-success.html")