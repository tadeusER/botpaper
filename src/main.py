import os
import argparse
import threading
from typing import List
import yaml
from dotenv import load_dotenv
from bot import ResearchBotScheduler
from models.logger_model import LoggerConfig

from models.paper_model import Schedule

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SLACK_TOKEN = os.getenv('SLACK_BOT_TOKEN')
DEFAULT_YAML_PATH = os.getenv('DEFAULT_YAML_PATH')
XPLORE_API_KEY = os.getenv('XPLORE_API_KEY')
SPRINGER_API_KEY = os.getenv('SPRINGER_API_KEY')
config = LoggerConfig(name="ResearchBot", log_file="research_bot.log")
logger = config.get_logger()

def check_api_keys():
    missing_keys = []

    if not XPLORE_API_KEY:
        missing_keys.append("XPLORE_API_KEY")
    if not SPRINGER_API_KEY:
        missing_keys.append("SPRINGER_API_KEY")

    return missing_keys

def check_tokens(app):
    missing_tokens = []

    if app == "discord" and not DISCORD_TOKEN:
        missing_tokens.append("DISCORD_BOT_TOKEN")
    elif app == "slack" and not SLACK_TOKEN:
        missing_tokens.append("SLACK_BOT_TOKEN")

    return missing_tokens

def check_yaml_exists(yaml_path):
    return os.path.exists(yaml_path)
def get_schedules_from_yaml(yaml_path: str) -> List[Schedule]:
    schedules = []
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        if data and 'schedules' in data:
            for schedule_data in data['schedules']:
                schedule = Schedule(
                    channel=schedule_data['channel'],
                    app=schedule_data['app'],
                    cron_schedule=schedule_data['cron_schedule'],
                    search_keywords=schedule_data['search_keywords']
                )
                schedules.append(schedule)
    return schedules
def get_apps_from_yaml(yaml_path):
    apps = []
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        if data and 'schedules' in data:
            for schedule in data['schedules']:
                apps.append(schedule['app'])
    return apps

def getargs():
    parser = argparse.ArgumentParser(description="Run a bot for specific apps.")
    parser.add_argument("--config", help="Path to the YAML configuration file.", default=DEFAULT_YAML_PATH)
    args = parser.parse_args()
    return args

def run_scheduler(schedule: Schedule):
    extraction_tokens = {
        "xplore": XPLORE_API_KEY,
        "springer": SPRINGER_API_KEY,
        # Puedes agregar otros tokens aquí
    }

    # Elegir el token del bot basado en el app
    if schedule.app == "discord":
        bot_token = DISCORD_TOKEN
    elif schedule.app == "slack":
        bot_token = SLACK_TOKEN
    else:
        bot_token = None  # o manejar esto de otra manera

    # Iniciar el ResearchBotScheduler
    scheduler = ResearchBotScheduler(schedule, bot_token, extraction_tokens)
    scheduler.start_scheduler()

def main():
    args = getargs()

    if not check_yaml_exists(args.config):
        logger.error(f"The specified YAML configuration file at '{args.config}' does not exist.")
        exit(1)

    schedules = get_schedules_from_yaml(args.config)
    if not schedules:
        logger.error("No schedules specified in the YAML configuration.")
        exit(1)

    threads = []

    for schedule in schedules:
        missing_tokens = check_tokens(schedule.app)
        missing_keys = check_api_keys()

        if missing_tokens:
            logger.error(f"Error for {schedule.app}: Missing environment variables: {', '.join(missing_tokens)}")
            continue

        if missing_keys:
            logger.error(f"Error for {schedule.app}: Missing API keys: {', '.join(missing_keys)}")
            continue

        logger.info(f"Starting scheduler for app: {schedule.app} and channel: {schedule.channel}")

        # Usar threading para ejecutar cada ResearchBotScheduler en su propio hilo
        thread = threading.Thread(target=run_scheduler, args=(schedule,))
        thread.start()
        threads.append(thread)

    # Esperar a que todos los hilos finalicen
    for thread in threads:
        thread.join()

    logger.info("All schedulers are now running.")

if __name__ == "__main__":
    main()

