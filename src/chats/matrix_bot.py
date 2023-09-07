import asyncio
from nio import AsyncClient, MatrixRoom, RoomMessageText

class MatrixBot:

    def __init__(self, homeserver: str, username: str, password: str):
        self.client = AsyncClient(homeserver, username)
        self.password = password

    async def connect(self):
        response = await self.client.login(self.password)
        if not isinstance(response, str):
            print(f"Logged in as {self.client.user_id} device id: {self.client.device_id}")
        else:
            print(response)

    async def disconnect(self):
        await self.client.logout()

    async def send_message(self, room_id: str, message: str):
        await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": message},
        )

    async def listen_messages(self, callback):
        self.client.add_event_callback(callback, RoomMessageText)
        await self.client.sync_forever(timeout=30000)  # milliseconds
if __name__=="__main__":
    # Usage
    async def custom_message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
        print(
            f"Message received in room {room.display_name}\n"
            f"{room.user_name(event.sender)} | {event.body}"
        )

    bot = MatrixBot("https://matrix.example.org", "@alice:example.org", "my-secret-password")

    asyncio.run(bot.connect())
    asyncio.run(bot.listen_messages(custom_message_callback))
