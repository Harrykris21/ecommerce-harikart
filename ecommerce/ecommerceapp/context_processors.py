from ecommerceapp.models import Category,Tags,Vendor,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WishList,Address
from django.db.models import Count
from django.contrib import messages
from django.contrib.messages import warning

def default(request):

    # Retrieve all categories along with the count of products in each category
    categories_with_counts = Category.objects.annotate(product_count=Count('product'))

    vendors = Vendor.objects.all()

     # Retrieve all categories and their corresponding products
    categories_with_products = Category.objects.prefetch_related('product_set')

    # Create a dictionary to store categories and their corresponding products
    categories_dict = {}
    for category in categories_with_products:
        categories_dict[category] = list(category.product_set.all())

    #CartItemsView
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])   

        # return render(request,"cart.html",({"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount}))
    # EndCart

    #WishlistItems
    try:
        wishList= WishList.objects.filter(user=request.user)
        wishlist_ids = [item.product.id for item in wishList]
    except:
        messages.warning(request,"You need to Login before accessing Wishlist ")
        wishList= 0
            

    




 
    return {
        'categories':categories_with_counts,
        'vendors' :vendors,
        'categories_with_products': categories_dict,
        'cart_total_amount':cart_total_amount,
        'wishList':wishList,
        'wishlist_ids': wishlist_ids,
        # "cart_data": request.session['cart_data_obj'],
        # ({"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    }



# def default(request):

#     # Retrieve all categories along with the count of products in each category
#     categories_with_counts = Category.objects.annotate(product_count=Count('product'))
#     vendors = Vendor.objects.all()


#     # Retrieve all categories along with their products
#     categories_with_products = Category.objects.prefetch_related('product_set')

#     # Create a dictionary to store categories and their corresponding products
#     categories_dict = {}
#     for category in categories_with_products:
#         categories_dict[category] = list(category.product_set.all())

#     return categories_dict



#     return {
#         'categories':categories_with_counts,
#         'vendors' :vendors,
#         'categories_with_products':categories_dict,
#     }