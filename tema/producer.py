"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = None

    def run(self):
        #generate producer id
        self.producer_id = self.marketplace.register_producer()

        while True:
            for prod_data in self.products:
                counter = prod_data[1]

                while counter:
                    # try to publish the product
                    published = self.marketplace.publish(self.producer_id, prod_data[0])

                    # if it's already published, sleep
                    if published is True:
                        sleep(prod_data[2])
                        counter -= 1

                    # try to republish
                    else:
                        sleep(self.republish_wait_time)
