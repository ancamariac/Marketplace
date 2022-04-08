"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Lock
import unittest
import logging
from logging.handlers import RotatingFileHandler
import tema.product as product_type

logging.Formatter.converter = time.gmtime
logging.basicConfig(
    handlers=[RotatingFileHandler('marketplace.log', maxBytes=5000000, backupCount=10)],
    format='%(asctime)s %(message)s',
    level=logging.INFO)
logger = logging.getLogger('marketplace_logger')


class TestMarketplace(unittest.TestCase):
    """
    Class for unittesting
    """
    def setUp(self):
        """
        Init marketplace
        """
        self.marketplace = Marketplace(5)

    def test_register_producer(self):
        """
        Test register_producer method
        """
        self.assertEqual(len(self.marketplace.producers), self.marketplace.register_producer())

    def test_publish(self):
        """
        Test publish method
        """
        producer_id = self.marketplace.register_producer()
        product = product_type.Tea("Matcha", 15, "Herbal")
        check_publish = self.marketplace.publish(producer_id, product)
        self.assertEqual(check_publish, True)

    def test_new_cart(self):
        """
        Test new_cart method
        """
        self.assertEqual(len(self.marketplace.consumers), self.marketplace.new_cart())

    def test_add_to_cart(self):
        """
        Test add_to_cart method
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        product = product_type.Coffee("Americano", 20, "5", "MEDIUM")

        self.marketplace.publish(producer_id, product)

        check_add_to_cart = self.marketplace.add_to_cart(cart_id, product)
        self.assertEqual(check_add_to_cart, True)

    def test_remove_from_cart(self):
        """
        Test remove_from_cart method
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        product = product_type.Coffee("Espresso", 18, "3", "LOW")

        self.marketplace.publish(producer_id, product)
        self.marketplace.add_to_cart(cart_id, product)

        self.marketplace.remove_from_cart(cart_id, product)
        self.assertEqual(len(self.marketplace.consumers[cart_id]), 0)

    def test_place_order(self):
        """
        Test place_order method
        """
        products_list = []
        products_list.append(product_type.Tea("Green Tea", 14, "Herbal"))
        products_list.append(product_type.Coffee("Espresso", 28, "4", "HIGH"))
        products_list.append(product_type.Tea("Black Tea", 18, "Herbal"))

        cart_id = self.marketplace.new_cart()

        for product_unit in products_list:
            self.marketplace.consumers[cart_id].append(product_unit)

        check_place_order = self.marketplace.place_order(cart_id)
        self.assertEqual(products_list, check_place_order)


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    queue_size_per_producer: int
    producers: list   # list of number of products per producer
    consumers: list   # list of products in consumers' carts

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = [[]]
        self.consumers = []
        self.register_producer_lock = Lock()
        self.new_cart_lock = Lock()
        self.add_to_cart_lock = Lock()
        self.remove_from_cart_lock = Lock()

        logger.info("Init Marketplace for "
                    "queue_size_per_producer = %d", self.queue_size_per_producer)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        with self.register_producer_lock:
            id_producer = len(self.producers)
        self.producers.append([])
        logger.info("Registered producer with producer_id = %d", id_producer)
        return id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: Int
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.producers[producer_id]) < self.queue_size_per_producer:
            self.producers[producer_id].append(product)
            logger.info(product)
            logger.info(producer_id)
            return True
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            id_cart = len(self.consumers)
        self.consumers.append([])
        logger.info("Created a new cart with the cart_id: %d", id_cart)
        return id_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.add_to_cart_lock:
            for producer in self.producers:
                if product in producer:
                    self.consumers[cart_id].append(product)
                    producer.remove(product)
                    logger.info(product)
                    logger.info(cart_id)
                    return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if product in self.consumers[cart_id]:
            self.consumers[cart_id].remove(product)
            with self.remove_from_cart_lock:
                self.producers[0].append(product)
            logger.info(product)
            logger.info(cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logger.info(cart_id)
        logger.info(self.consumers[cart_id])
        return self.consumers[cart_id]
