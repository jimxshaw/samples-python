import sales

# If we import a separate Python module and want to use items from that module,
# we must prefix those items with the module's name.
cart = sales.Cart()
order = sales.Order()
order.get_input()


# As long as the quit boolean is false, we continue processing orders.
while not order.quit:
    cart.process(order)
    order = sales.Order()
    order.get_input()

# Since we overrode the __repr__ method in the Cart class, that implementation
# will be printed instead of the detault __repr__ implementation.
print(cart)
