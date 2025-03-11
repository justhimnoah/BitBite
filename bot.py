import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load menu from a JSON file
with open('menu.json') as f:
    menu = json.load(f)

orders = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='menu')
async def show_menu(ctx):
    menu_message = "Here's our menu:\n"
    for item in menu:
        menu_message += f"{item}\n"
    await ctx.send(menu_message)

@bot.command(name='order')
async def order(ctx, *, order_item):
    user = ctx.message.author
    if order_item in menu:
        if user not in orders:
            orders[user] = []
        orders[user].append(order_item)
        await ctx.send(f'{order_item} has been added to your order.')
    else:
        await ctx.send(f'Sorry, we do not have {order_item} on the menu.')

@bot.command(name='myorder')
async def my_order(ctx):
    user = ctx.message.author
    if user in orders and orders[user]:
        order_list = ', '.join(orders[user])
        await ctx.send(f'Your current order: {order_list}')
    else:
        await ctx.send('You have no items in your order.')

@bot.command(name='clearorder')
async def clear_order(ctx):
    user = ctx.message.author
    if user in orders:
        orders[user] = []
        await ctx.send('Your order has been cleared.')
    else:
        await ctx.send('You have no items in your order.')

bot.run('YOUR_DISCORD_BOT_TOKEN')
