from abc import ABC, abstractmethod

class AbstractChatBot(ABC):

    def __init__(self, token, prefix="!"):
        """
        Initialize the bot with the given configuration.

        Args:
        - config (dict): Configuration parameters for the bot.
        """
        self.token = token
        self.prefix = prefix

    @abstractmethod
    async def connect(self):
        """
        Connect the bot to the chat platform.
        """
        pass

    @abstractmethod
    async def disconnect(self):
        """
        Disconnect the bot from the chat platform.
        """
        pass

    @abstractmethod
    async def send_message(self, channel, message):
        """
        Send a message to a specified channel.

        Args:
        - channel (str): The channel where the message should be sent.
        - message (str): The message to be sent.
        """
        pass

    @abstractmethod
    async def listen_messages(self, callback):
        """
        Start listening for incoming messages and call the provided callback when a message is received.

        Args:
        - callback (func): A function to be called when a message is received.
        """
        pass

    @abstractmethod
    async def handle_error(self, error):
        """
        Handle any errors that occur while interacting with the chat platform.

        Args:
        - error (Exception): The error that occurred.
        """
        pass

    @abstractmethod
    async def set_configuration(self, config):
        """
        Set or update the bot's configuration.

        Args:
        - config (dict): Configuration parameters to be updated or set.
        """
        self.config.update(config)


