import requests
import urllib
import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import telegram
from telegram.ext import Updater, CommandHandler

def download_song(song_id, quality):
    response = requests.get(f"https://www.jiosaavn.com/api.php?p=webapi_song&action=download&token=&id={song_id}&_format=json")
    download_link = response.json()['data']['song'][f'media_url{quality}']
    urllib.request.urlretrieve(download_link, f"{song_id}.mp3")
    print(f"Downloaded {song_id}.mp3")

def extract_audio(input_file, output_file):
    subprocess.call(['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file])
    print(f"Extracted audio from {input_file} to {output_file}")

def create_cover_image(title, artist, song_id):
    # Create a blank image
    image = Image.new('RGB', (1000, 1000), color='white')

    # Add text to the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', size=100)
    draw.text((100, 400), title, font=font, fill='black')
    draw.text((100, 600), artist, font=font, fill='black')

    # Save the image
    image.save(f"{song_id}.jpg")
    print(f"Created cover image for {song_id}")

def send_song(bot, chat_id, song_id, title, artist):
    song_file = open(f"{song_id}.mp3", 'rb')
    cover_file = open(f"{song_id}.jpg", 'rb')
    bot.send_audio(chat_id, audio=song_file, title=title, performer=artist, thumb=cover_file)
    song_file.close()
    cover_file.close()

def download_extract_and_create_cover(bot, update, args):
    song_id = args[0]
    title = args[1]
    artist = args[2]
    quality = args[3] if len(args) > 3 else ''
    download_song(song_id, quality)
    extract_audio(f"{song_id}.mp3", f"{song_id}.m4a")
    create_cover_image(title, artist, song_id)
    chat_id = update.message.chat_id
    send_song(bot, chat_id, song_id, title, artist)
    print("All tasks completed successfully!")

def set_quality(bot, update, args):
    quality = args[0]
    user_id = update.message.from_user.id
    with open(f"{user_id}.txt", 'w') as f:
        f.write(quality)
    update.message.reply_text(f"Set song quality to {quality}.")

def get_quality(user_id):
    try:
        with open(f"{user_id}.txt", 'r') as f:
            return f.read()
    except:
        return ''

# Example usage
if __name__ == '__main__':
    token = 'YOUR_BOT_TOKEN'
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('download', download_extract_and_create_cover, pass_args=True))
    dispatcher.add_handler(CommandHandler('set_quality', set_quality, pass_args=True))
    updater.start_polling()
    updater.idle()
