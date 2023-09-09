import asyncio
import os
import argparse
from typing import List
import yaml
from dotenv import load_dotenv
from bot import ResearchBotScheduler
from models.logger_model import LoggerConfig

from models.paper_model import Schedule

load_dotenv()
ENV_VARS = {
    "discord": "DISCORD_BOT_TOKEN",
    "slack": "SLACK_BOT_TOKEN"
}
API_KEYS = ["XPLORE_API_KEY", "SPRINGER_API_KEY"]
DEFAULT_YAML_PATH = os.getenv('DEFAULT_YAML_PATH')

config = LoggerConfig(name="ResearchBot", log_file="research_bot.log")
logger = config.get_logger()



def check_env_vars(app):
    """
    Checks if the necessary environment variables are set for the specified app.
    """
    missing_vars = []

    # Check API keys
    for key in API_KEYS:
        if not os.getenv(key):
            missing_vars.append(key)

    # Check bot tokens
    if app in ENV_VARS and not os.getenv(ENV_VARS[app]):
        missing_vars.append(ENV_VARS[app])

    return missing_vars

def check_yaml_exists(yaml_path):
    """
    Verifica si el archivo YAML especificado existe.

    Args:
        yaml_path (str): La ruta al archivo YAML.

    Returns:
        bool: True si el archivo existe, False de lo contrario.
    """
    return os.path.exists(yaml_path)
def get_schedules_from_yaml(yaml_path: str) -> List[Schedule]:
    """
    Lee los datos de programación de un archivo YAML y devuelve una lista de objetos Schedule.

    Args:
        yaml_path (str): La ruta al archivo YAML.

    Returns:
        List[Schedule]: Una lista de objetos Schedule.
    """
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
    """
    Lee los datos de programación de un archivo YAML y devuelve una lista de las aplicaciones programadas.

    Args:
        yaml_path (str): La ruta al archivo YAML.

    Returns:
        List[str]: Una lista de las aplicaciones programadas.
    """
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
    parser.add_argument("--logdir", help="Directory path for logs.", default="./logs")  # Argumento para el directorio de logs
    args = parser.parse_args()
    return args

async def run_scheduler(schedule: Schedule):
    extraction_tokens = {
        "xplore": os.getenv("XPLORE_API_KEY"),
        "springer": os.getenv("SPRINGER_API_KEY"),
    }

    if schedule.app in ENV_VARS:
        bot_token = os.getenv(ENV_VARS[schedule.app])
    else:
        logger.error(f"Unsupported app: {schedule.app}")
        return

    scheduler = ResearchBotScheduler(schedule, bot_token, extraction_tokens)
    await scheduler.initialize()

async def main():
    args = getargs()

    # Configure log path based on the argument
    config = LoggerConfig(name="ResearchBot", log_file="research_bot.log", log_folder=args.logdir)
    logger = config.get_logger()

    if not check_yaml_exists(args.config):
        logger.error(f"The specified YAML configuration file at '{args.config}' does not exist.")
        exit(1)

    schedules = get_schedules_from_yaml(args.config)
    if not schedules:
        logger.error("No schedules specified in the YAML configuration.")
        exit(1)

    tasks = []

    for schedule in schedules:
        missing_vars = check_env_vars(schedule.app)

        if missing_vars:
            logger.error(f"Error for {schedule.app}: Missing environment variables: {', '.join(missing_vars)}")
            continue

        logger.info(f"Starting scheduler for app: {schedule.app} and channel: {schedule.channel}")

        task = asyncio.create_task(run_scheduler(schedule))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    logger.info("All schedulers are now running.")

if __name__ == "__main__":
    asyncio.run(main())
