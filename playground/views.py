from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Count, Max, Min, Avg, Sum, F
from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem

# Create your views here.


def exercises(request):

    # Exercises

    # Customers with .com accounts
    customersWithComeAccounts = Customer.objects.filter(email__endswith='com')

    # Collections that don’t have a featured product
    collectionsWithNoFeaturedProduct = Collection.objects.filter(
        featured_product__isnull=True)

    # Products with low inventory (less than 10)
    productsWithLowInventory = Product.objects.filter(inventory__lt=10)

    # Orders placed by customer with id = 1
    ordersWithId1 = Order.objects.filter(customer__id=1)

    # Order items for products in collection 3
    orderItemsForProductsInCollection3 = OrderItem.objects.filter(
        product__collection__id=3)

    # Select products that have been ordered and sort them by title
    orderedProductsIds = OrderItem.objects.values(
        'product_id').distinct()  # distinct to clear duplicates

    productsOrdered = Product.objects.filter(
        id__in=orderedProductsIds).order_by('title')

    # Get the last 5 orders with their customer
    # and items (incl product)
    lastFiveOrders = Order.objects.select_related(
        'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # How many orders do we have?
    ordersCount = Order.objects.aggregate(orders=Count('id'))

    # How many units of product 1 have we sold?
    product1Sales = OrderItem.objects \
        .filter(product__id=1)         \
        .aggregate(units_sold=Sum('quantity'))

    # How many orders has customer 1 placed?
    customer1Orders = Order.objects \
        .filter(customer__id=1) \
        .aggregate(ordersCount=Count('id'))

    # What is the min, max and average price of the products in collection 3?
    productPrices = Product.objects \
        .filter(collection__id=3)   \
        .aggregate(max_price=Max('unit_price'), min_price=Min('unit_price'), avg_price=Avg('unit_price'))

    # Customers with their last order id
    lastOrderId = Customer.objects \
        .annotate(last_order_id=Max('order__id'))

    # Collections and count of their products
    countProductsOfColletions = Collection.objects \
        .annotate(product_count=Count('product'))

    # Customers with more than 5 orders
    customerWithMoreThanFiveOrders = Customer.objects \
        .annotate(orders_count=Count('order'))  \
        .filter(orders_count__gt=5)

    # Customers and the total amount they’ve spent
    customersAndTotalAmountSpent = Customer.objects \
        .annotate(total_amount_spent=Sum(
            F('order__orderitem__unit_price')
            * F('order__orderitem__quantity')
        ))

    # Top 5 best-selling products and their total sales
    topFiveBestSellingProducts = Product.objects    \
        .annotate(
            total_sales=Sum(
                F('orderitem__unit_price')
                * F('orderitem__quantity')
            ))  \
        .order_by('-total_sales')[:5]

    return render(request, 'exercises.html', {
        'selection': 'topFiveBestSellingProducts',
        'customersWithCom': list(customersWithComeAccounts),
        'collectionsWithNoFeaturedProduct': list(collectionsWithNoFeaturedProduct),
        'productsWithLowInventory': list(productsWithLowInventory),
        'ordersWithId1': list(ordersWithId1),
        'orderItemsForProductsInCollection3': list(orderItemsForProductsInCollection3),
        'productsOrdered': productsOrdered,
        'lastFiveOrders': lastFiveOrders
    })


def object_exercises():
    # Manually Create Object
    collection = Collection()
    collection.title = 'Video Games'
    # Product needs to exist before we create this
    collection.featured_product = Product(pk=1)
    collection.save()

    # If we run the above code it creates the object
    # If we change something and run it again it will update the
    # same object without creating new one
    # We need to update all fields or django will set fields that we don't
    # specify to empty strings

    # To delete run
    # collection.delete()
    # To delete multiple run
    # Collection.objects.filter(id__gt=5).delete()

    # Create a shopping cart with an item
    shoppingCart = Cart()
    shoppingCart.save()

    item1 = CartItem()
    item1.product_id = 1
    item1.quantity = 5
    item1.save()

    # Update the quantity of an item in a shopping cart
    item1 = CartItem.objects.get(pk=1)
    item1.quantity = 2
    item1.save()

    # Delete a cart with its items
    cart = Cart(pk=1)
    cart.delete()

    # Because we've enabled cascading in the relationship between
    # cart and its items, deleting a cart automatically causes
    # deletion of its items. So we don't need to delete each item
    # individually


def say_hello(request):

    # To make a change to database we wrap the commands in a transaction
    # clause so if something goes wrong database is left unaffacted

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'hello.html', {'name': 'George'})
