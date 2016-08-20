
def go_shopping():
    cart = []

    while True:
        item = get_item()
        if item == "":
            break
        cart.append(item)
    
    print(cart)
    print("Finished")

def get_item():
    print("Please enter an item: ")
    return input()

go_shopping()