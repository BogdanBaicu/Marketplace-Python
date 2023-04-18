"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cart = None
        self.name = kwargs["name"]


    def run(self):
        for cart in self.carts:
            # generate id
            cart_id = self.marketplace.new_cart()

            # execute instructions for each product
            for prod in cart:
                quant = prod["quantity"]

                while quant:
                    available = None

                    if prod["type"] == "add":
                        available = self.marketplace.add_to_cart(cart_id, prod["product"])

                        if available:
                            quant -= 1
                        else:
                            # if product is not available, retry aflter retry_wait_time
                            sleep(self.retry_wait_time)
                    elif prod["type"] == "remove":
                        available = self.marketplace.remove_from_cart(cart_id, prod["product"])
                        quant -= 1

            # place order
            prod = self.marketplace.place_order(cart_id)

            # print the output
            for item in prod:
                print(f'{self.name} bought {item}')
