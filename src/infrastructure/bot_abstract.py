from abc import ABC, abstractmethod
import time
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from models.logger_model import LoggerConfig
from models.paper_model import ArticleMetadata, Schedule
from service.api_consumer import ResearchPaperSearcher

class AbstractChatBot(ABC):

    def __init__(self, token, 
                 research_paper_searcher: ResearchPaperSearcher, 
                 crondict: dict, 
                 schedule: Schedule, 
                 chunk_size: int = 10,
                 timesleepmsg: int = 120,
                 prefix='!'):
        self.token = token
        self.prefix = prefix
        self.schedule = schedule
        self.chunk_size = chunk_size
        self.timesleepmsg = timesleepmsg
        self.research_paper_searcher = research_paper_searcher  
        self.scheduler = AsyncIOScheduler()
        cron_args = crondict
        self.scheduler.add_job(self.run, trigger='cron', **cron_args)
        
        # Logger setup inside class
        config = LoggerConfig(name="ChatBot", log_file="ChatBot.log")
        self.logger = config.get_logger()

    @abstractmethod
    def get_channel_if(self, channel_name: str):
        """Retrieve a chat channel by its name. Platform-specific."""
        pass

    @abstractmethod
    def register_events(self):
        """Register bot-related events. Platform-specific."""
        pass

    @abstractmethod
    def register_commands(self):
        """Register bot commands. Platform-specific."""
        pass

    async def notify(self, message):
        """Send a notification message. Should be implemented in derived classes based on platform specifics."""
        pass  

    async def run(self):
        """Search for articles and notify the results."""
        articles = self.research_paper_searcher.search(self.schedule.search_keywords)

        if not articles:
            self.logger.warning("No articles found for the given search keywords.")
            return

        for i in range(0, len(articles), self.chunk_size):
            chunk = articles[i:i + self.chunk_size]
            message = self.format_articles(chunk)
            await self.notify(message)

            # Espera 120 segundos antes de continuar con el siguiente grupo de artículos.
            if i + self.chunk_size < len(articles):
                time.sleep(120)
    def format_articles(self, articles: List[ArticleMetadata]) -> str:
        """Format the list of articles into a string."""
        formatted_articles = []
        self.logger.info(f"Formatting articles...{len(articles)} found.")
        for article in articles:
            formatted_articles.append(f"{article.published}-{article.title} - {article.link}")
            formatted_articles.append("----"*10)
        return "\n".join(formatted_articles)

    @abstractmethod
    async def start_bot(self):
        """Start the bot. This might differ based on the chat platform being used."""
        pass

    def __del__(self):
        """Shutdown the scheduler when the bot is destroyed."""
        if self.scheduler:
            self.scheduler.shutdown()

