from typing import List
from chats.discord_bot import DiscordBot
from chats.matrix_bot import MatrixBot
from chats.slack_bot import SlackBot
from models.logger_model import LoggerConfig
from models.paper_model import ArticleMetadata, Schedule
from service.api_consumer import ResearchPaperSearcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
# Crea una instancia de LoggerConfig y obtén el logger.

config = LoggerConfig(name="ResearchBotScheduler", log_file="scheduler_bot.log")
logger = config.get_logger()
class ResearchBotScheduler:
    """_summary_
    Clase que se encarga de ejecutar el bot de acuerdo a un cron schedule.

    args:
        schedule (Schedule): Un objeto Schedule que contiene la información de la tarea a ejecutar.
        bot_token (str): El token del bot que se utilizará para enviar el mensaje.
        extraction_tokens (dict): Un diccionario con los tokens de extracción para la API de Semantic Scholar.
    """
    def __init__(self, 
                 schedule: Schedule, 
                 bot_token: str, 
                 extraction_tokens: dict) -> None:
        self.schedule = schedule
        self.bot_token = bot_token
        self.research_searcher = ResearchPaperSearcher(extraction_tokens)
        
        self.bots = {
            "discord": DiscordBot,
            "slack": SlackBot,
            "matrix": MatrixBot,
            # ... cualquier otro bot que pueda tener
        }

        # Inicializar el planificador
        self.bot_instance = self.bots[self.schedule.app](bot_token, '!', self)
        self.scheduler = AsyncIOScheduler()
        cron_args = self.parse_cron_string(self.schedule.cron_schedule)
        self.scheduler.add_job(self.run, trigger='cron', **cron_args)
    
    def parse_cron_string(self, cron_string: str) -> dict:
        """_summary_

        Args:
            cron_string (str): Cadena en formato cron que especifica el horario de ejecución de las búsquedas. Debe tener el siguiente formato: "minuto hora día_del_mes mes día_de_la_semana".

        Returns:
            dict: Diccionario con los valores correspondientes a los argumentos del método add_job de la librería apscheduler. Los valores son los siguientes:
            - "minute": valor correspondiente al minuto de la hora en que se ejecutará la tarea.
            - "hour": valor correspondiente a la hora en que se ejecutará la tarea.
            - "day": valor correspondiente al día del mes en que se ejecutará la tarea.
            - "month": valor correspondiente al mes en que se ejecutará la tarea.
            - "day_of_week": valor correspondiente al día de la semana en que se ejecutará la tarea.
        """
        minute, hour, day_of_month, month, day_of_week = cron_string.split()
        return {
            "minute": minute,
            "hour": hour,
            "day": day_of_month,
            "month": month,
            "day_of_week": day_of_week
        }

    async def on_message_received(self, message):
        # Process incoming message here if needed
        pass

    async def run(self):
        articles = self.research_searcher.search(self.schedule.search_keywords)
        
        if not articles:
            logger.warning("No articles found for the given search keywords.")
            return

        await self.bot_instance.wait_until_ready()  # Asumiendo que todos tus bots tienen este método
        message = self.format_articles(articles)
        channel_name = self.bot_instance.get_channel_name(self.schedule.channel)  # Asumiendo que todos tus bots tienen este método
        c = self.bot_instance.get_channel(channel_name)  # Asumiendo que todos tus bots tienen este método
        await c.send(message)


    def format_articles(self, articles: List[ArticleMetadata]) -> str:
        """
        Formatea una lista de metadatos de artículos en una cadena de texto legible.

        Args:
            articles (List[ArticleMetadata]): Una lista de metadatos de artículos.

        Returns:
            str: Una cadena de texto que contiene el título y el enlace de cada artículo, separados por un guión.
        """
        formatted_articles = []
        logger.info(f"Formatting articles...{len(articles)} found.")
        for article in articles:
            if not isinstance(article, ArticleMetadata):
                raise TypeError(f"Expected ArticleMetadata, got {type(article)}")
            else:
                formatted_articles.append(f"{article.title} - {article.link}")

        return "\n".join(formatted_articles[:10])

    async def start_scheduler(self):
        """_summary_
        Método que inicia el planificador.
        """
        logger.info("Starting scheduler...")
        await self.run()  # Ejecuta la tarea programada inmediatamente
        self.scheduler.start()
