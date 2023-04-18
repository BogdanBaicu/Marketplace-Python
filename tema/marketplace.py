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
        self.carts = {} # dict containing all carts
        self.register_producer_lock = Lock()
        self.new_cart_lock = Lock()
        self.cart_lock = Lock()

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
        logging.info("Entering publish with parameters: %s  ,  %s", str(producer_id), str(product))

        #check if producer_id is valid
        if not producer_id in  self.producers:
            logging.error("Error publish: producer_id %s does not exist", str(producer_id))
            return False

        #check if producer's queue is not full
        if len(self.producers[producer_id]) == self.queue_size_per_producer:
            logging.error("Error publish: producer %s has the queue full", str(producer_id))
            return False
    
        # add the product to producer's list and mark it as not used
        try:
            self.producers[producer_id].append([product, 0])
            logging.info("Leaving publish")
            return True
        except ValueError as exception:
            logging.error("Error publish: %s", str(exception))
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        
        logging.info("Entering new_cart")
        # the id is the current number of carts
        # the lock is used to prevent multiple threads from creating carts simultaneously and so
        # running into race condition
        try:
            with self.new_cart_lock:
                cart_id = len(self.carts)
            self.carts[cart_id] = [] # initialize empty cart

            logging.info("Leaving new_cart")
            return cart_id
        except ValueError as exception:
            logging.error("Error new_cart: %s", str(exception))
            return None
        

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        logging.info("Entering add_to_cart with parameters: %s  ,  %s", str(cart_id), str(product))
        # the lock is used to prevent multiple threads from doing operations simultaneously, preventing
        # race condition 
        # search for the product in every producer's list, if the product existsm add it to the cart,
        # mark it as used
        try:
            with self.cart_lock:
                for key, value in self.producers.items():
                    for prod in value:
                        if product == prod[0]:
                            self.carts[cart_id].append((product, key))
                            prod[1] = 1
                            logging.info("Leaving add_to_cart, rpoduct added to cart")
                            return True
            logging.info("Leaving add_to_cart, product not in marketplace")
            return False
        except ValueError as exception:
            logging.error("Error add_to_cart: %s", str(exception))
            return False

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

    def test_publish(self):
        """
        test publish
        Check if a product is published successfully
        """
        self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish("prod0", "tea"))

    def test_new_cart(self):
        """
        test new_cart
        Check if the id of the first 2 carts is correct
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.new_cart(), 1)

    def test_add_to_cart(self):
        """
        test add_to_cart
        Check if a published product can be added to the cart and an object that is not published cannot be added
        """
        self.marketplace.register_producer()
        self.marketplace.publish("prod0", "tea")
        self.marketplace.new_cart()
        self.assertTrue(self.marketplace.add_to_cart(0, "tea"))
        self.assertFalse(self.marketplace.add_to_cart(0, "coffee"))
