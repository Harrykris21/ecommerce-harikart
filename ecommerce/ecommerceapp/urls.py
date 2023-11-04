
from django.urls import path,include
from ecommerceapp import views

app_name = 'ecommerceapp' 

urlpatterns = [
    path('',views.index,name='index'),
    path('category/',views.category_list_view,name='category_list'),
    path('product/',views.product_list_view,name='product_list'),
    path('category/<cid>/',views.category_product_list_view,name='category_product_list'),
    path('vendor-list/',views.vendor_list_view,name='vendor_list'), 
    path('vendor-detail/<vid>',views.vendor_detail_view,name='vendor_detail'), 
    path('product-detail/<pid>',views.product_detail_view,name='product_detail'), 

    #Add Revies
    path('ajax/add_review/<str:pid>/', views.ajax_add_review, name='ajax_add_review'),

    #Search
    path('search/', views.search_view, name='search'),

    #Filter
    path('filter-products/', views.filter_product, name='filter-products'),

    #AddToCart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    #ViewCart
    path('cart/', views.cart_view, name='cart'),

    #DeleteItemFrmCart
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    
    #UpdateQty
    path('update-qty/', views.update_qty, name='update-qty'),

    #Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    
    #PayPal
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    #Payment Sucsess 
    path('payment-completed/', views.payment_complete_view, name='payment-completed'),

    #Payment Failed 
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),

    #ViewWishlist
    path('wishlist/', views.view_wishlist, name='wishlist'),

    #AddWishlist
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),

    #AddWishlistIndex
    path('add-to-wishlist-index/', views.add_to_wishlist, name='add-to-wishlist-index'),

    #RemoveFrmWishlist
    path('remove-from-wishlist/', views.remove_wishlist, name='remove-from-wishlist'),

    #RemoveFrmWishlistIndex
    path('remove-from-wishlist-index/', views.remove_wishlist_index, name='remove-from-wishlist-index'),

 



 








    
]
