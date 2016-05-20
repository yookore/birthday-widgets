#!/usr/bin/python

import pika
from birthdaywidget import settings

class Broker:

    def __init__(self):
        """
        Constructor connnect to the default exchange and queue
        """

        pass

    def publish(self,message):

        queue = settings.QUEUE

        self.credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
        self.connection  = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT_HOST,
                                                                             settings.RABBIT_PORT, '/',
                                                                             self.credentials))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue = queue, durable=True)

        # Defining the exchange
        self.channel.exchange_declare(exchange=settings.EXCHANGE,
                                      type='direct',
                                      durable=True)


        self.channel.queue_bind(exchange=settings.EXCHANGE, queue = queue)
        # Publish the message
        self.channel.basic_publish(
            exchange    = settings.EXCHANGE,
            routing_key = queue,
            body        =  message)
        print " [x] Sent %r to queue %r" % (message ,queue,)

        self.connection.close()






