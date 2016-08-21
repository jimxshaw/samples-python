class Cart:

    def __init__(self):
        self._contents = dict()

    # We're overriding the default implementation of this Python representation method.
    # Think of this method as akin to C#'s .ToString method.
    def __repr__(self):
        return "{0} {1}".format(Cart, self.__dict__)

    def process(self, order):
        if order.add:
            # If the input item key is not in the cart, first set the value to 0
            # then add 1 to the value. If there's already the same item in the
            # cart then simply add 1 to the value.
            if not order.item in self._contents:
                self._contents[order.item] = 0
            self._contents[order.item] += 1
        elif order.delete:
            # If given the command to delete an item and that item is in our dictionary,
            # decrease its value by 1. If that item's value reaches 0 or below, completely
            # remove that item key from the dictionary.
            if order.item in self._contents:
                self._contents[order.item] -= 1
                if self._contents[order.item] <= 0:
                    del self._contents[order.item]

        print(self._contents)


class Order:
    
    def __init__(self):
        # By default our quit boolean is False meaning the app won't quit unless
        # the user tells the app to quit. Also, initialize a few other attributes.
        self.quit = False
        self.add = False
        self.delete = False
        self.item = None

    def get_input(self):
        print("[command] [item] (command is a to add, d to delete, q to quit)")
        line = input()
        # User input from start up to index 1.
        command = line[:1]
        # User input from index 2 until the end of the input.
        self.item = line[2:]

        if command == "a":
            self.add = True
        elif command == "d":
            self.delete = True
        elif command == "q":
            self.quit = True


cart = Cart()
order = Order()
order.get_input()


# As long as the quit boolean is false, we continue processing orders.
while not order.quit:
    cart.process(order)
    order = Order()
    order.get_input()

# Since we overrode the __repr__ method in the Cart class, that implementation
# will be printed instead of the detault __repr__ implementation.
print(cart)
