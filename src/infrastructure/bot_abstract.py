from abc import ABC, abstractmethod

class AbstractChatBot(ABC):

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

