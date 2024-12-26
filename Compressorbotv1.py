import os

import time

from telethon import TelegramClient, events

from moviepy import VideoFileClip

# Replace these with your own values

API_ID = '22413321'

API_HASH = '19dc6a4da93120d1af60afd778559d55'

BOT_TOKEN = '7766638158:AAHRI72ksXh9nRD_-yOIVnUSVVUHsdZWpzU'

client = TelegramClient('video_compressor_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))

async def start(event):

    await event.respond("Welcome! Send me a video and I'll compress it for you.")

@client.on(events.NewMessage())

async def handle_video(event):

    if event.message.video:

        await event.respond("Downloading your video...")

        video_path = await event.message.download_media()

        

        # Estimate compression time

        original_size = os.path.getsize(video_path)

        estimated_time = original_size / (1024 * 1024) * 2  # Rough estimate: 2 MB/s

        await event.respond(f"Estimated compression time: {estimated_time:.2f} seconds.")

        

        # Compress the video

        await event.respond("Compressing your video...")

        start_time = time.time()

        

        compressed_path = "compressed_video.mp4"

        with VideoFileClip(video_path) as video:

            video.write_videofile(compressed_path, codec='libx264', bitrate='500k')

        

        compression_time = time.time() - start_time

        await event.respond(f"Compression completed in {compression_time:.2f} seconds.")

        

        # Send back the compressed video

        await event.respond("Sending back your compressed video...")

        await client.send_file(event.chat_id, compressed_path, caption="Here is your compressed video!")

        

        # Clean up

        os.remove(video_path)

        os.remove(compressed_path)

    else:

        await event.respond("Please send a video file.")

# Run the bot

print("Bot is running...")

client.run_until_disconnected()
