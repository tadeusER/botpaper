import asyncio
from typing import List
from chats.discord_bot import DiscordBot
from chats.matrix_bot import MatrixBot
from chats.slack_bot import SlackBot
from models.logger_model import LoggerConfig
from models.paper_model import ArticleMetadata, Schedule
from service.api_consumer import ResearchPaperSearcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

config = LoggerConfig(name="ResearchBotScheduler", log_file="scheduler_bot.log")
logger = config.get_logger()

class ResearchBotScheduler:
    def __init__(self, schedule: Schedule, bot_token: str, extraction_tokens: dict):
        if not bot_token or not extraction_tokens:
            logger.error("Invalid or missing bot_token or extraction_tokens.")
            raise ValueError("Bot token and extraction tokens are required.")

        self.schedule = schedule
        self.bot_token = bot_token
        self.research_searcher = ResearchPaperSearcher(extraction_tokens, logger=logger)
        self.observers = []

        cron_args = self.parse_cron_string(self.schedule.cron_schedule)
        
        if self.schedule.app in ["discord", "slack", "matrix"]:
            self.bot_instance = self.get_bot(self.schedule.app, bot_token, cron_args)
        else:
            logger.error(f"Invalid app name provided: {self.schedule.app}")
            raise ValueError("Invalid app name provided.")
    
    async def initialize(self):
        await self.bot_instance.start_bot()

    def get_bot(self, app_name, token, crondict):
        if app_name == "discord":
            return DiscordBot(token, self.research_searcher, crondict, self.schedule)
        elif app_name == "slack":
            return SlackBot(token, self.research_searcher, crondict, self.schedule)  # Assuming it accepts these params
        elif app_name == "matrix":
            return MatrixBot(token, self.research_searcher, crondict, self.schedule)  # Assuming it accepts these params
        else:
            logger.error(f"Unsupported app_name: {app_name}")
            raise ValueError(f"Unsupported app_name: {app_name}")

    def parse_cron_string(self, cron_string: str) -> dict:
        try:
            minute, hour, day_of_month, month, day_of_week = cron_string.split()
            return {
                "minute": minute,
                "hour": hour,
                "day": day_of_month,
                "month": month,
                "day_of_week": day_of_week
            }
        except ValueError:
            logger.error(f"Invalid cron string format: {cron_string}")
            raise ValueError("Invalid cron string format.")
