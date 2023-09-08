from typing import List
from chats.discord_bot import DiscordBot
from chats.matrix_bot import MatrixBot
from chats.slack_bot import SlackBot
from models.paper_model import ArticleMetadata, Schedule
from service.api_consumer import ResearchPaperSearcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class ResearchBotScheduler:
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
        self.scheduler = AsyncIOScheduler()
        cron_args = self.parse_cron_string(self.schedule.cron_schedule)
        self.scheduler.add_job(self.run, trigger='cron', **cron_args)
    
    def parse_cron_string(self, cron_string: str) -> dict:
        # Suponiendo un formato cron estándar "minuto hora día_del_mes mes día_de_la_semana"
        # Puedes ajustar esto según tus necesidades.
        minute, hour, day_of_month, month, day_of_week = cron_string.split()
        return {
            "minute": minute,
            "hour": hour,
            "day": day_of_month,
            "month": month,
            "day_of_week": day_of_week
        }

    async def run(self):
        # Realiza una búsqueda de artículos
        articles = self.research_searcher.search(self.schedule.search_keywords)
        
        # Formatea los artículos para enviarlos como mensaje
        message = self.format_articles(articles)
        
        # Selecciona el bot apropiado y envía el mensaje
        if self.schedule.app in self.bots:
            bot_class = self.bots[self.schedule.app]
            bot_instance = bot_class(self.bot_token)
            await bot_instance.connect()
            await bot_instance.send_message(self.schedule.channel, message)
            await bot_instance.disconnect()

    def format_articles(self, articles: List[ArticleMetadata]) -> str:
        formatted_articles = [f"{article.title} - {article.link}" for article in articles]
        return "\n".join(formatted_articles)

    def start_scheduler(self):
        self.scheduler.start()
