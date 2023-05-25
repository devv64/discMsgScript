import discord
import asyncio
import os
import sys
from config import myToken

os.environ["SSL_CERT_FILE"] = "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/certifi/cacert.pem"
TOKEN = myToken

intents = discord.Intents.default()
intents.all()

async def export_messages(server_id):
    # Create a Discord client with the specified intents
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')

        # Get the server object using the provided server ID
        server = client.get_guild(server_id)
        if server is None:
            print(f"Could not find server with ID: {server_id}")
            await client.close()
            return

        # Iterate over all channels in the server
        for channel in server.channels:
            if isinstance(channel, discord.TextChannel):
                print(f"Processing messages in channel: {channel.name}")
                # Fetch and process all messages in the channel
                try:
                    async for message in channel.history(limit=None):
                        print(f"{message.author.name}: {message.content}")
                        # Append the message content to the message.txt file
                        with open('message.txt', 'a', encoding='utf-8') as f:
                            f.write(f'{message.author.name}: {message.content}\n')
                except discord.Forbidden:
                    print(f"Skipping channel {channel.name}: No permission to access")

        # Close the client connection
        await client.close()

    # Start the client
    await client.start(TOKEN)

# Check if the server ID is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the server ID as a command-line argument.")
    sys.exit(1)

# Get the server ID from the command-line argument
server_id = int(sys.argv[1])

# Run the export_messages coroutine
asyncio.run(export_messages(server_id))