import discord
from discord.ext import commands
import json
import os

# Load menu from a JSON file safely
try:
    with open('menu.json', 'r') as f:
        menu = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    menu = []  # Default to an empty menu if the file is missing or corrupted

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

orders = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='menu')
async def show_menu(ctx):
    if not menu:
        await ctx.send("The menu is currently unavailable.")
        return

    menu_message = "Here's our menu:\n" + "\n".join(menu)
    await ctx.send(menu_message)

@bot.command(name='order')
async def order(ctx, *, order_item):
    user_id = ctx.author.id  # Use user ID instead of the object
    if order_item in menu:
        if user_id not in orders:
            orders[user_id] = []
        orders[user_id].append(order_item)
        await ctx.send(f'{order_item} has been added to your order.')
    else:
        await ctx.send(f'Sorry, we do not have {order_item} on the menu.')

@bot.command(name='myorder')
async def my_order(ctx):
    user_id = ctx.author.id
    if user_id in orders and orders[user_id]:
        order_list = ', '.join(orders[user_id])
        await ctx.send(f'Your current order: {order_list}')
    else:
        await ctx.send('You have no items in your order.')

@bot.command(name='clearorder')
async def clear_order(ctx):
    user_id = ctx.author.id
    if user_id in orders:
        orders[user_id] = []
        await ctx.send('Your order has been cleared.')
    else:
        await ctx.send('You have no items in your order.')

# Load bot token from an environment variable or a config file
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Recommended way
if not TOKEN:
    print("Error: No bot token found. Set DISCORD_BOT_TOKEN as an environment variable.")
else:
    bot.run(TOKEN)
