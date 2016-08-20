
def go_shopping():
    cart = dict()

    while True:
        order = get_order()
        # If process_order returns False then not keyword will make it True.
        if not process_order(order, cart):
            break
    
    print(cart)
    print("Finished")

def get_order():
    print("[command] [item] (command is a to add, d to delete, q to quit)")
    line = input()
    # User input from start up to index 1.
    command = line[:1]
    # User input from index 2 until the end of the input.
    item = line[2:]
    # We return a tuple comprised of our command and item.
    return (command, item)

def process_order(order, cart):
    # Unpack order, which is a tuple.
    (command, item) = order

    if command == "a":
        # Add item to cart.
        add_to_cart(item, cart)
    elif command == "d" and item in cart:
        # Remove item from cart only if said item is in the cart.
        delete_from_cart(item, cart)
    elif command == "q":
        return False
    
    return True

def add_to_cart(item, cart):
    # If the input item key is not in the cart, first set the value to 0
    # then add 1 to the value. 
    if not item in cart:
        cart[item] = 0
    cart[item] += 1

def delete_from_cart(item, cart):
    # If the item key is in the cart, remove 1 from the value but only if 
    # the value is greater than 0. This is to prevent negative values.
    if item in cart and cart[item] > 0:
        cart[item] -= 1

go_shopping()