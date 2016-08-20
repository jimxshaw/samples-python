
def go_shopping():
    cart = []

    while True:
        item = get_order()
        if item == "":
            break
        cart.append(item)
    
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

go_shopping()