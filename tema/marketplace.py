"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import unittest
import logging
import time
from threading import Lock
from logging.handlers import RotatingFileHandler

# logging configuration
logging.basicConfig(filename = "marketplace.log", level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')
logging.Formatter.converter = time.gmtime
logging.getLogger('LOGGER').addHandler(RotatingFileHandler(filename = "marketplace.log", maxBytes = 1024 * 1024 * 5, backupCount = 10))

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = {} # dict containing all producers
        self.register_producer_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        logging.info("Entering register_producer")
        # the lock is used o prevent multiple threads from registering producers simultaneously
        # and avoid race condition
        # id is formed by "prod" and current number of producers in the producers dict, making
        # the id unique
        try:
            with self.register_producer_lock:
                producer_id = "prod" + str(len(self.producers))

            # initialize empty list of products for this producer
            self.producers[producer_id] = []

            logging.info("Leaving register_producer")
            return producer_id
        except ValueError as exception:
            logging.error("Error register_producer: %s", str(exception))
            return None

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        pass

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        pass

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        pass

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass

class TestMarketplace(unittest.TestCase):
    """
    Unittesting class
    """
    def setUp(self):
        self.marketplace = Marketplace(10)

    def test_register_producer(self):
        """
        test register_producer
        Check if the id of the first 2 producers is correct and the 3rd id is different to the
        argument passed
        """
        self.assertEqual(self.marketplace.register_producer(), "prod0")
        self.assertEqual(self.marketplace.register_producer(), "prod1")
        self.assertNotEqual(self.marketplace.register_producer(), "prod1")
