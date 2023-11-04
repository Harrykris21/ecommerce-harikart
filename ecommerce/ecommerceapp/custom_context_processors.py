from django.template.loader import render_to_string

def default(request):
    # Get 'cart_data_obj' from the session with a default of an empty dictionary
    cart_data = request.session.get('cart_data_obj', {})

    cart_total_amount = 0
    for p_id, item in cart_data.items():
        cart_total_amount += int(item['qty']) * float(item['price'])

    # Render the template and store it in a variable
    rendered_cart_list = render_to_string("async/header-cart-list.html", {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
    })

    # Create a dictionary with the context data you want to pass to the templates
    context = {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
        'rendered_cart_list': rendered_cart_list,  # Include the rendered template in the context
    }

    # Return the context dictionary
    return context
