import discord
from strategies import ApiExtraction, ScrapingExtraction
from config import TOKEN

class ArticleBot:
    def __init__(self, strategy):
        self.strategy = strategy
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            print(f'Conectado como: {self.client.user}')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('!articles'):
                articles = self.get_articles()
                await message.channel.send('\n'.join(articles))

    def get_articles(self):
        return self.strategy.extract()

    def run(self):
        self.client.run(TOKEN)


if __name__ == "__main__":
    # Puedes elegir la estrategia que desees usar al instanciar el bot.
    # Aquí estoy usando ApiExtraction como ejemplo, pero podrías cambiar a ScrapingExtraction u otra.
    bot = ArticleBot(strategy=ApiExtraction())
    bot.run()
