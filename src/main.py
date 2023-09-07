import os
import argparse
from typing import List
import yaml
from dotenv import load_dotenv

from models.paper_model import Schedule

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SLACK_TOKEN = os.getenv('SLACK_BOT_TOKEN')
DEFAULT_YAML_PATH = os.getenv('DEFAULT_YAML_PATH')
XPLORE_API_KEY = os.getenv('XPLORE_API_KEY')
SPRINGER_API_KEY = os.getenv('SPRINGER_API_KEY')

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

def run_bot(schedule: Schedule):
    # Aquí puedes instanciar y ejecutar tu bot dependiendo del 'app' de la instancia de Schedule.
    # Por ejemplo:
    if schedule.app == 'discord':
        print(f"Running Discord bot for channel {schedule.channel}...")
        # bot = DiscordBot()
        # bot.run(DISCORD_TOKEN)
    elif schedule.app == 'slack':
        print(f"Running Slack bot for channel {schedule.channel}...")
        # bot = SlackBot()
        # bot.run(SLACK_TOKEN)

def main():
    args = getargs()

    if not check_yaml_exists(args.config):
        print(f"Error: The specified YAML configuration file at '{args.config}' does not exist.")
        exit(1)

    schedules = get_schedules_from_yaml(args.config)
    if not schedules:
        print("Error: No schedules specified in the YAML configuration.")
        exit(1)

    threads = []

    for schedule in schedules:
        missing_tokens = check_tokens(schedule.app)
        missing_keys = check_api_keys()

        if missing_tokens:
            print(f"Error for {schedule.app}: Missing environment variables: {', '.join(missing_tokens)}")
            continue  # This will skip the current iteration and move to the next schedule.

        if missing_keys:
            print(f"Error for {schedule.app}: Missing API keys: {', '.join(missing_keys)}")
            continue  # This will skip the current iteration and move to the next schedule.

        print(f"Starting bot for app: {schedule.app} and channel: {schedule.channel}")
        
        thread = threading.Thread(target=run_bot, args=(schedule,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All bots are now running.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

