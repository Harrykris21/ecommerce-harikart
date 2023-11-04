$(document).ready(function() {
    console.log("working ok`")
    const monthNames = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ];
    

    $("#commentForm").submit(function(e) {
        e.preventDefault();
        console.log("AJAX code executed");

        
        $("#commentForm").submit(function(e) {
            e.preventDefault();
            
            // Disable the submit button to prevent multiple submissions
            $("#submit-button").prop("disabled", true);
        
            // ... Rest of your AJAX code ...
        });
        

        let dt = new Date();
        let time = dt.getDay() + " "+ monthNames[dt.getUTCMonth()] + "," + dt.getUTCFullYear()

        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function(response) {
                console.log("111111111222222222233333333333");
                if (response.bool === true) {
                    // Build the HTML structure as a string
                    let _html = '<li>' +
                        '<div class="people-box">' +
                        '<div>' +
                        '<div class="people-image">' +
                        '<img src="https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1223671392?k=20&m=1223671392&s=170667a&w=0&h=kEAA35Eaz8k8A3qAGkuY8OZxpfvn9653gDjQwDHZGPE=" class="img-fluid blur-up lazyload" alt="">' +
                        '</div>' +
                        '</div>' +
                        '<div class="people-comment">' +
                        '<a class="name" href="javascript:void(0)">' + response.context.user + '</a>' +
                        '<div class="date-time">' +
                        '<h6 class="text-content">' + time + '</h6>' +
                        '<div class="product-rating">';

                    // Build the rating stars based on response.context.rating
                    // for (var i = 1; i <= response.context.rating; i++) {
                    //     _html += '<i class="fas fa-star text-warning"></i>';
                    // }

                    // Assuming response.context.rating is a number between 1 and 5
                    for (var i = 1; i <= 5; i++) {
                    // Use a ternary operator to add either a filled or empty star
                    _html += '<i class="fas fa-star ' + (i <= response.context.rating ? 'text-warning' : '') + '"></i>';
                    }

                    // Close the rating stars div and continue with HTML structure
                    _html += '</div>' +
                        '</div>' +
                        '<div class="reply">' +
                        '<p>' + response.context.review + ' <a href="javascript:void(0)">Reply</a></p>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</li>';

                    // Prepend the _html to an element with the id "review-list"
                    $("#review-list").prepend(_html);

                    // Optionally, hide the form
                    $("#hide-comment-form").hide();
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
            }
        });
    });







    $(".table-responsive-xl").on("click", ".delete-product", function () {
    // $(".delete-product").on("click", function () {
        console.log("working delete-product`------------////----------------")

        
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        console.log("Product ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("working beforeSend`------------////----------------")
                this_val.hide()
            },
            success: function(response){
                console.log(response);
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
                console.log("working success`------------////----------------")


            }
        })
    
    });



    
    // $(".table-responsive-xl").on("click", ".update-qty", function () {
    //     // $(".delete-product").on("click", function () {
    //         console.log("working Update-Qty`------------////----------------")
    
            
    //         let product_id = $(this).attr("data-product");
    //         let this_val = $(this);
    //         let product_quantity = $(".product-qty-"+ product_id).val();
            
            

    //         console.log("Product ID:", product_id);
    //         console.log("Product QTY:", product_quantity);

    
    //         $.ajax({
    //             url: "/update-qty",
    //             data: {
    //                 "id": product_id
    //             },
    //             dataType: "json",
    //             beforeSend: function(){
    //                 console.log("working beforeSend`------------////----------------")
    //                 // this_val.hide()
    //             },
    //             success: function(response){
    //                 console.log(response);
    //                 this_val.show()
    //                 $(".cart-items-count").text(response.totalcartitems)
    //                 $("#cart-list").html(response.data)
    //                 console.log("working success`------------////----------------")
    
    
    //             }
    //         })
        
    //     });

    $(".table-responsive-xl").on("click", ".update-qty", function () {
        
        let thisButton = $(this);

        let product_id = thisButton.attr("data-product");
      
        let product_quantity = $(".product-qty-" + product_id).val();

        let product_price = $(".item-price-" + product_id).val();
        let product_price_total = product_quantity *product_price;

        let subItemTotalAmountClass = ".sub_item_total_amount-" + product_id;

        
            console.log("Product ID:", product_id);
            console.log("Product QTY:", product_quantity);
            console.log("Product Price:", product_price);
            console.log("Product Total Price:", product_price_total);
            console.log("subItemTotalAmountClass:", subItemTotalAmountClass);

            
        $.ajax({
            url: "/update-qty",
            data: {
                "id": product_id,
                "qty": product_quantity,  // Include 'qty' in the request
                "product_price_total":product_price_total
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Working beforeSend");
                // You can add loading/spinner logic here
                thisButton.hide();
            },
            success: function (response) {
                console.log(response);
                thisButton.show();
                $(".cart_total_amount").text(response.cart_total_amount);
                $(subItemTotalAmountClass).text(response.sub_item_total_amount);
                


                // $("#cart-list").html(response.data);
                console.log("Working success");
            }
        });
    });
    
    


});






// $(document).ready(function (){
//     $(".filter-checkbox").on("click", function(){
//         console.log("????????????????===>CLICKED CKECKBOX");
//     } )
// })

// $(document).ready(function () {
    
//     // Use event delegation to handle clicks on .filter-checkbox
//     $(document).on("click", ".filter-checkbox", function () {
        
//         bject = {}

//         $(".filter-checkbox").each(function(){
//             let filter_value = $(this).val()
//             let filter_key = $(this).filter_key()

//             filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
//                 return element.value
//             })

//         })

//         console.log("Filter object is:", filter_object);
//     });
// });

$(document).ready(function () {
    
    // Use event delegation to handle clicks on .filter-checkbox
    $(document).on("click", ".filter-checkbox", function () {
        
        let filter_object = {}; // Initialize an empty object

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val();
            let filter_key = $(this).attr("data-filter"); // Get the data-filter attribute value

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function(element){
                return element.value;
            });
        });

        console.log("Filter object is:", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending data..");
            },
            success: function(response){
                console.log("data filterred successfully")
                $("#filtered-products").html(response.data);
                $("#filtered-products-2").html(response.data2);
               
            }

        })

    });
});


//Add to Cart 
$("#add-to-cart-btn").on("click", function () {

    let this_val = $(this)
    let index = this_val.attr("data-index")
    console.log("Data Index:", index);

    let quantity = $("#product-quantity-" + index).val();
    let weight = $("#product-weight-" + index).val();
    let title = $("#product-title-" + index).val();
    let id = $("#product-id-" + index).val();
    let pid = $("#product-pid-" + index).val();
    let price = $("#product-price-" + index).val();
    let image = $("#product-image-" + index).val();
    let oldprice = $("#product-old_price-" + index).val();
    let tprice = price * quantity;
    let savingprice =  $("#product-old_price-" + index).val() - $("#product-price-" + index).val() ;
    
    
  

    
    console.log("Index", index);
    console.log("Quantity", quantity);
    console.log("Weight", weight);
    console.log("title", title);
    console.log("id", id);
    console.log("pid", pid);
    console.log("price", price);
    console.log("oldprice", oldprice);
    console.log("image", image);
    console.log("Current Element", this_val);
    console.log("tprice", tprice);
    console.log("savingprice", savingprice);
    

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id':id,
            'pid':pid,
            'image':image,
            'qty':quantity,
            'weight':weight,
            'title':title,
            'price':price,
            'tprice':tprice,
            'oldprice':oldprice,
            'savingprice':savingprice,

            

            

            
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding product to cart ..")
        },
        success: function(response){
            // this_val.html("✔")
            // console.log("Product added to cart ..");
            // $(".cart-items-count").text(response.totalcartitems)
                    
            this_val.html("Item Added To Cart").css("color", "green");
            console.log("Product added to cart ..");
            $(".cart-items-count").text(response.totalcartitems)
            $("#header-cart-lista").html(response.data)

        },
        error: function(xhr, status, error) {
            console.log("AJAX Request Error: " + error);
            console.log("Data sent in AJAX request:", data);
            console.log("Response from the server:", response);
            console.log("Server response status code:", response.status);


            // Handle the error, e.g., display an error message to the user
        }
    })
});


//Add to Cart Index
$(".addcart-button").on("click", function () {
    let this_val = $(this);
    let index = this_val.attr("data-index");
    console.log("Data Index:", index);

    let quantity = $("#product-quantity-" + index).val();
    let weight = $("#product-weight-" + index).val();
    let title = $("#p-title-" + index).val(); // Fixed the ID here
    let id = $("#product-id-" + index).val();
    let pid = $("#product-pid-" + index).val();
    let price = $("#product-price-" + index).val();
    let image = $("#product-image-" + index).val();
    let oldprice = $("#product-old_price-" + index).val();
    let tprice = price * quantity;
    let savingprice = oldprice - price;

    console.log("Index", index);
    console.log("Quantity", quantity);
    console.log("Weight", weight);
    console.log("title", title);
    console.log("id", id);
    console.log("pid", pid);
    console.log("price", price);
    console.log("oldprice", oldprice);
    console.log("image", image);
    console.log("Current Element", this_val);
    console.log("tprice", tprice);
    console.log("savingprice", savingprice);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': id,
            'pid': pid,
            'image': image,
            'qty': quantity,
            'weight': weight,
            'title': title,
            'price': price,
            'tprice': tprice,
            'oldprice': oldprice,
            'savingprice': savingprice,
        },
        dataType: 'json',
        beforeSend: function () {
            console.log("Adding product to cart ..");
        },
        success: function (response) {
            this_val.html("✔").css("color", "#0da487");;
            console.log("Product added to cart ..");
            $(".cart-items-count").text(response.totalcartitems);
            $("#header-cart-lista").html(response.data);
        },
        error: function (xhr, status, error) {
            console.log("AJAX Request Error: " + error);
            console.log("Data sent in AJAX request:", data);
            console.log("Response from the server:", response);
            console.log("Server response status code:", response.status);

            // Handle the error, e.g., display an error message to the user
        }
    });
});


//AddToWishlist
// $(".addwishlist-button").on("click", function () {
//     let this_val = $(this);
//     let product_id = this_val.attr("data-index");
//     console.log("Product Id:", product_id);

//     $.ajax({
//         url: '/add-to-wishlist-index', // Corrected URL
//         data: {
//             'id': product_id,
//         },
//         dataType: 'json',
//         beforeSend: function () {
//             console.log("Adding product to Wishlist ..");
//             this_val.hide(); // Hide the button that was clicked
//         },
//         success: function (response) {
//             console.log("success", response.data);
//             // Update the appropriate HTML element with the response data
//             // $("#delete_wishlist_index").html(response.data)
//             this_val.show();
//             if (response.bool == true) {
//                 console.log("Added to Wishlist ..");
//             }
//         },
//     });
// });

//AddToWishlist
//AddToWishlist
$(".addwishlist-button").on("click", function () {
    let this_val = $(this);
    let product_id = this_val.attr("data-index");
    console.log("Product Id:", product_id);

    $.ajax({
        url: '/add-to-wishlist-index', // Corrected URL
        data: {
            'id': product_id,
        },
        dataType: 'json',
        beforeSend: function () {
            console.log("Adding product to Wishlist ..");
            this_val.hide(); // Hide the button that was clicked
        },
        success: function (response) {
            console.log("success", response.data);
            this_val.show();

            if (response.bool == true) {
                console.log("Added to Wishlist ..");
                // Change the class of the button and set the color while retaining the data attribute
                let product_id = this_val.attr("data-index");
                this_val.removeClass("addwishlist-button")
                    .addClass("fa-solid fa-heart fa-beat-fade fa-lg delete_wishlist_index")
                    .css("color", "#f31616")
                    .attr("data-wishlist-product", product_id);
            }
        },
    });
});




  
  
  


//RemoveWishlist

$(document).on("click", ".delete_wishlist", function () {
    $(this).off("click");
    let wishlist_id = $(this).attr("data-wishlist-produt");
    let this_val = $(this);

    console.log("wishlist-id:", wishlist_id);

    $.ajax({
        url: "/remove-from-wishlist",
        data: {
            "id": wishlist_id
        },
        dataType: "json",
        beforeSend: function () {
            console.log("Deleting from wishlist...");
        },
        success: function (response) {
            if (response.error) {
                console.log("Error: " + response.error);
            } else {
                console.log("Deleted");
                $("#wishlist-list").html(response.data);
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
});

// RemoveWishlistFRrmIndex

//RemoveWishlist

$(document).on("click", ".delete_wishlist_index", function () {
    $(this).off("click");
    let wishlist_id = $(this).attr("data-wishlist-produt");
    let this_val = $(this);

    console.log("wishlist-id:", wishlist_id);

    $.ajax({
        url: "/remove-from-wishlist-index",
        data: {
            "id": wishlist_id
        },
        dataType: "json",
        beforeSend: function () {
            console.log("Deleting from wishlist...");
        },
        success: function (response) {
            console("Success")
            if (response.error) {
                console.log("Error: " + response.error);
            } else {
                console.log("Deleted");
                $("#remove-wishlist-index").html(response.data);
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
});




