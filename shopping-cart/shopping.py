
def go_shopping():
    # A set is used instead of a list because a set can only have unique items.
    cart = set()

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
        cart.add(item)
    elif command == "d" and item in cart:
        # Remove item from cart only if said item is in the cart.
        cart.remove(item)
    elif command == "q":
        return False
    
    return True

go_shopping()