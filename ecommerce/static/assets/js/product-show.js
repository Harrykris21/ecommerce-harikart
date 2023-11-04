// product-modal.js

$(document).ready(function() {
    // Listen for a click on the "eye" button
    $('li[data-bs-toggle="tooltip"] a[data-bs-target="#view"]').click(function() {
        // Get the product details from data attributes
        var title = $(this).data('product-title');
        var description = $(this).data('product-description');
        var price = $(this).data('product-price');
        var image = $(this).data('product-image');
        var qty = $(this).data('product-qty');
        var productId = $(this).data('product-id'); // Retrieve the product ID

        // Populate the modal with the product details
        $('#view .title-name').text(title);
        $('#view .price').text('$' + price);
        $('#view .productId').int(productId);
        $('#view .qty').text(qty);
        $('#view .product-detail p').text(description);
        $('#view .slider-image img').attr('src', image);

        // Show the modal
        $('#view').modal('show');
    });
});
