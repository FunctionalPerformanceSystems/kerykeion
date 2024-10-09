import logging
import re
from kerykeion import AstrologicalSubject, KerykeionChartSVG, grand_key, rulership_for_planets
from grand_key_outputs import  build_tree_string, build_tree 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import cairosvg
from wand.image import Image
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from datetime import datetime
import asyncio
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import os
from PIL import Image

# Function to check if the bot is already running


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states
NAME, YEAR, MONTH, DAY, TIME, LOCATION = range(6)

# Dictionary to store user data
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    user_data[user.id] = {}
    await update.message.reply_text(f"Hello, {user.name}! Let's create your profile. To start, please enter your name.")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    user_data[user.id]['name'] = update.message.text
    #years = [str(year) for year in range(datetime.now().year, 1800, -1)]
    years = [str(year) for year in range(1800, datetime.now().year + 1)]
    keyboard = [InlineKeyboardButton(year, callback_data=f"year_{year}") for year in years]
    reply_markup = InlineKeyboardMarkup([keyboard[i:i+5] for i in range(0, len(keyboard), 5)])
    await update.message.reply_text("Please select your year of birth:", reply_markup=reply_markup)
    return YEAR

async def year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    # Проверяем, является ли это нажатие кнопки
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        year = query.data.split('_')[1]  # Получаем год из callback_data
        user_data[user.id]['year'] = int(year)
        logger.info(f"User {user.id} selected year: {year}")
        await query.edit_message_reply_markup(reply_markup=None)
       #await query.edit_message_text("Year accepted. Please select your month of birth:")
    else:
        # Если это текстовое сообщение, проверяем, является ли оно допустимым годом
        try:
            year = int(update.message.text)  # Используем текстовое сообщение
            logger.info(f"User {user.id} entered year: {year}")
            if 0 <= year <= 2500:  # Убедитесь, что диапазон корректен
                user_data[user.id]['year'] = year
                #await update.message.reply_text("Year accepted. Please select your month of birth:")
                # Если это нажатие кнопки, можно продолжить с выбором месяца
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                keyboard = [InlineKeyboardButton(month, callback_data=f"month_{i+1}") for i, month in enumerate(months)]
                reply_markup = InlineKeyboardMarkup([keyboard[i:i+3] for i in range(0, len(keyboard), 3)])
                await update.message.reply_text("Please select your month of birth:", reply_markup=reply_markup)
                return MONTH
            else:
                await update.message.reply_text("Please enter a valid year between 0 and 2500")
                return YEAR
        except ValueError:
            await update.message.reply_text("Invalid input. Please enter a valid year.")
            return YEAR
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    keyboard = [InlineKeyboardButton(month, callback_data=f"month_{i+1}") for i, month in enumerate(months)]
    reply_markup = InlineKeyboardMarkup([keyboard[i:i+3] for i in range(0, len(keyboard), 3)])
    await query.message_text("Please select your month of birth:", reply_markup=reply_markup)
    return MONTH


async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    month = int(query.data.split('_')[1])
    user_data[user.id]['month'] = month
    days = range(1, 32)  # This is simplified and doesn't account for different month lengths
    keyboard = [InlineKeyboardButton(str(day), callback_data=f"day_{day}") for day in days]
    reply_markup = InlineKeyboardMarkup([keyboard[i:i+7] for i in range(0, len(keyboard), 7)])
    await query.edit_message_text("Please select your day of birth:", reply_markup=reply_markup)
    return DAY

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    day = int(query.data.split('_')[1])
    user_data[user.id]['day'] = day
    await query.edit_message_text("Please enter your time of birth in HH:MM format (e.g., 14:30)")
    return TIME

async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    time_str = update.message.text
    try:
        time = datetime.strptime(time_str, "%H:%M").time()
        user_data[user.id]['time'] = time
        location_button = KeyboardButton(text="Send Location", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True)
        #await update.message.reply_text("Please send your location or enter your city and country", reply_markup=reply_markup)
        await update.message.reply_text("Please send your location or enter your city and country")
        return LOCATION
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time in HH:MM format")
        return TIME

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    if update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        user_data[user.id]['location'] = f"Latitude: {latitude}, Longitude: {longitude}"
        user_data[user.id]['lat'] = latitude
        user_data[user.id]['lng'] = longitude
        await update.message.reply_text(f"Your location: Latitude: {latitude}, Longitude: {longitude}")
        await update.message.reply_location(latitude=latitude, longitude=longitude)
    else:
        user_data[user.id]['location'] = update.message.text
        # You might want to add geocoding here to get lat/lng from city name
        # For now, we'll use default values
        user_data[user.id]['lat'] = 0  # Default latitude for Moscow
        user_data[user.id]['lng'] = 0 # Default longitude for Moscow

    data = user_data[user.id]
    
    # Create AstrologicalSubject
    a_subject = AstrologicalSubject(
        name=data['name'],
        year=data['year'],
        month=data['month'],
        day=data['day'],
        hour=data['time'].hour,
        minute=data['time'].minute,
        nation="RU",  # Assuming Russia for now, you might want to ask for this separately
        city=data['location'] if isinstance(data['location'], str) else "Unknown",
        lat=data['lat'],
        lng=data['lng']
    )
    key_array = grand_key(a_subject)
    #formatted_output = text_output(key_array)
    formatted_output = build_tree_string(build_tree(key_array))
    rulership = rulership_for_planets(a_subject)
    await send_astrological_chart(update, a_subject)
    # You can now use a_subject for further astrological calculations

    await update.message.reply_text(
        f"Here is the collected information:\n"
        f"Name: {a_subject.name}\n"
        f"Date of Birth: {a_subject.day}.{a_subject.month}.{a_subject.year}\n"
        f"Time of Birth: {a_subject.hour:02d}:{a_subject.minute:02d}\n"
        f"Place of Birth: {a_subject.city}\n"
        f"Coordinates: Latitude {a_subject.lat}, Longitude {a_subject.lng}"
    )

    await update.message.reply_text(
        f"```\n{formatted_output}\n```",
        parse_mode='Markdown'
    )

    await update.message.reply_text(
        f"{rulership}"
    )
    
    return ConversationHandler.END

async def send_astrological_chart(update: Update, subject: AstrologicalSubject):
    # Generate chart
    chart = KerykeionChartSVG(subject)
    chart.makeSVG()
    svg_path = f"{chart.output_directory}/{chart.name}{chart.chart_type}Chart.svg"
    png_path = f"{chart.output_directory}/{chart.name}{chart.chart_type}Chart.png"
  
    await svg_to_png_screenshot(svg_path, png_path)
    # Send chart image
    with open(png_path, 'rb') as chart_file:
        #await update.message.reply_photo(document=chart_file, filename=f"{subject.name}_chart.png")
        await update.message.reply_photo(photo=chart_file, filename=f"{subject.name}_chart.png")
        
    # Clean up temporary files
    os.remove(svg_path)
    os.remove(png_path)
    '''
    # Send a message with the chart details
    await update.message.reply_text(
        f"Here's the astrological chart for {subject.name}\n"
        f"Born on: {subject.year}-{subject.month:02d}-{subject.day:02d} at {subject.hour:02d}:{subject.minute:02d}\n"
        f"Location: {subject.city}"
    )
    '''

async def svg_to_png_screenshot(svg_path, png_path, width=586, height=586):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up the Chrome driver
    service = Service('/opt/homebrew/bin/chromedriver')  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)

    #driver.set_window_size(width, height)

    # Load the SVG file
    driver.get(f"file://{os.path.abspath(svg_path)}")

    # Wait for the SVG to render
    #time.sleep(1)  # Adjust if necessary

    # Take a screenshot
    driver.save_screenshot(png_path)

    img = Image.open(png_path)
    width, height = img.size
 
    # Setting the points for cropped image
    left = width - 0.8 * width - 10
    top = height - 0.92 * height
    right = 0.8 * width - 10
    bottom = 0.92 * height - 17
 
    box = (left, top, right, bottom)
    img2 = img.crop(box)
    img2.save(png_path)

    # Clean up
    driver.quit()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7089013714:AAEEAO852O0xNpdJOgq7gg7k28xwYzPL-sI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            YEAR: [
                CallbackQueryHandler(year, pattern=r'^year_'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, year) 
            ],
            MONTH: [CallbackQueryHandler(month, pattern=r'^month_')],
            DAY: [CallbackQueryHandler(day, pattern=r'^day_')],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()