import discord
from discord.ext import commands
import google.generativeai as genai
import json
import matplotlib.pyplot as plt
import io
from math import pi
import typing


prompt = """You are a pokedex in the real-life. What it means is that I will send you photos from real-life that can be not related to pokemon. 

Example: you can receive a photo of a Lucario plushy, a computer, a hoodie, etc.

Your goal is to:

1. Analyze the photo I send you.

2- Give me a description of what I send you. 

3. Give me his species.

4. Give me his stats (weight, height, speed, HP, attack, defense, special attack, special defense, type).

The description, the species, and the stats must be realistic, like if I was in a Pokémon game.
the description must have some lore related to the photo. For example, for gyarados, it says that he can destroy cities.

You must return a JSON. the result must be like this:
{
    species: string
    name: string
    weight: number
    height: number
    hp: number
    attack: number
    defense: number
    specialAttack: number
    specialDefense: number
    speed: number
    description: string
    type: Type[]
    move: Move[]
}
the stats (except the weight and the height) are in the range of 0 to 200
the weight is in kg
the height is in cm

here's the value for Type
Type {
  Normal = 0,
  Fire = 1,
  Water = 2,
  Electric = 3,
  Grass = 4,
  Ice = 5,
  Fighting = 6,
  Poison = 7,
  Ground = 8,
  Flying = 9,
  Psychic = 10,
  Bug = 11,
  Rock = 12,
  Ghost = 13,
  Dragon = 14,
  Dark = 15,
  Steel = 16,
  Fairy = 17,
}
For the type, you must give me the number and not the string. For example, if the type is "Fire", you must return 1.

here's the value for Move
Move {
  name: string
  type: Type
  power: number
  accuracy: number
  description: string
  pp: number
}
for the moves, you can only have 4 of them. 
You can choose moves that are already existing in the game or create new ones. Ideally, unless it's literally a pokemon from the game, you should create AT LEAST a "Signature move"  However, it must make sense with the description you gave me.
be careful, I only want one pokemon. not multiple pokemons in one photo.
"""
pokemonTypes = {
    0: "Normal",
    1: "Fire",
    2: "Water",
    3: "Electric",
    4: "Grass",
    5: "Ice",
    6: "Fighting",
    7: "Poison",
    8: "Ground",
    9: "Flying",
    10: "Psychic",
    11: "Bug",
    12: "Rock",
    13: "Ghost",
    14: "Dragon",
    15: "Dark",
    16: "Steel",
    17: "Fairy"
}

pokemonEmojiTypes = {
    0: "🦌",  # Normal
    1: "🔥",  # Fire
    2: "💧",  # Water
    3: "⚡️",  # Electric
    4: "🌿",  # Grass
    5: "❄️",  # Ice
    6: "🥊",  # Fighting
    7: "☠️",  # Poison
    8: "⛰️",  # Ground
    9: "🪁",  # Flying
    10: "🔮",  # Psychic
    11: "🐛",  # Bug
    12: "🪨",  # Rock
    13: "👻",  # Ghost
    14: "🐉",  # Dragon
    15: "🌑",  # Dark
    16: "⚙️",  # Steel
    17: "✨"   # Fairy
}




#Gemini API
genai.configure(api_key="AIzaSyDlb8JtTZYOxua-SvXNvMAAbioJ4OVtGSw")
model =  genai.GenerativeModel(model_name='gemini-2.0-flash-exp', generation_config={"response_mime_type": "application/json"})

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('Logged on as', bot.user)


@bot.command()
async def pokemon(ctx: commands.Context, attachment: typing.Optional[discord.Attachment]):
    if attachment is None:
        await ctx.send("Oops! It looks like you forgot to attach an image. Please send me a picture of your 'Pokemon' so I can analyze it!")
        return

    result = await attachment.read()
    await ctx.send("Analyzing your image to generate a Pokémon profile. Please wait...")

    response = model.generate_content([prompt, {"data": result, "mime_type": attachment.content_type}])

    json_response = json.loads(response.text)
    print(json_response)
    name = json_response["name"]
    description = json_response["description"]
    species = json_response["species"]
    weight = json_response["weight"]
    height = json_response["height"]
    hp = json_response["hp"]
    attack = json_response["attack"]
    defense = json_response["defense"]
    special_attack = json_response["specialAttack"]
    special_defense = json_response["specialDefense"]
    speed = json_response["speed"]
    types = json_response["type"]
    moves = json_response["move"]


    formatted_response = (
        f"# {name}\n"
        f"{description}\n\n"
        f"**Species:** {species}\n"
        f"**Weight:** {weight} kg\n"
        f"**Height:** {height} cm\n"
        f"**HP:** {hp}\n"
        f"**Attack:** {attack}\n"
        f"**Defense:** {defense}\n"
        f"**Special Attack:** {special_attack}\n"
        f"**Special Defense:** {special_defense}\n"
        f"**Speed:** {speed}\n"
        f"**Types:** {', '.join(pokemonTypes[int(t)] for t in types)}\n"

        f"## Moves\n"
        f"1. **{moves[0]['name']}** - Power: {moves[0]['power']} - Accuracy: {moves[0]['accuracy']} - PP: {moves[0]['pp']}\n"
        f"**{pokemonEmojiTypes[int(moves[0]['type'])]}{pokemonTypes[int(moves[0]['type'])]}{pokemonEmojiTypes[int(moves[0]['type'])]}**\n"
        f"{moves[0]['description']}\n\n"
        
        f"2. **{moves[1]['name']}** - Power: {moves[1]['power']} - Accuracy: {moves[1]['accuracy']} - PP: {moves[1]['pp']}\n"
        f"**{pokemonEmojiTypes[int(moves[1]['type'])]}{pokemonTypes[int(moves[1]['type'])]}{pokemonEmojiTypes[int(moves[1]['type'])]}**\n"
        f"{moves[1]['description']}\n\n"

        f"3. **{moves[2]['name']}** - Power: {moves[2]['power']} - Accuracy: {moves[2]['accuracy']} - PP: {moves[2]['pp']}\n"
        f"**{pokemonEmojiTypes[int(moves[2]['type'])]}{pokemonTypes[int(moves[2]['type'])]}{pokemonEmojiTypes[int(moves[2]['type'])]}**\n"
        f"{moves[2]['description']}\n\n"
        
        f"4. **{moves[3]['name']}** - Power: {moves[3]['power']} - Accuracy: {moves[3]['accuracy']} - PP: {moves[3]['pp']}\n"
        f"**{pokemonEmojiTypes[int(moves[3]['type'])]}{pokemonTypes[int(moves[3]['type'])]}{pokemonEmojiTypes[int(moves[3]['type'])]}**\n"
        f"{moves[3]['description']}\n\n"
    )

    await ctx.send(formatted_response)

  # Create a spider chart
    labels = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']
    stats = [hp, attack, defense, special_attack, special_defense, speed]

    # Number of variables
    num_vars = len(labels)

    # Compute angle of each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Make sure the plot closes

    # Create the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], labels, color='black', size=10)  # Change label color and size

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([40, 80, 120, 160, 200], ["40", "80", "120", "160", "200"], color="grey", size=7)
    plt.ylim(0, 200)  # Define the limit for y-axis

    # Plot data
    stats += stats[:1]  # Close the loop by repeating the first value
    ax.plot(angles, stats, linewidth=3, linestyle='solid', color='orange')  # Thicker line with color

    # Fill the area under the plot with a gradient-like effect
    ax.fill(angles, stats, 'orange', alpha=0.4)  # Transparent orange fill

    # Save the chart to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    # Send the chart as an image attachment
    file = discord.File(buf, filename='pokemon_stats.png')
    await ctx.send(file=file)


@bot.command(name="pokemon-help")
async def help(ctx: commands.Context):
    formatted_response = (
        f"## /pokemon\n"
        f"Analyze the photo you send and generate a Pokémon profile.\n"
        f"**Usage:** `/pokemon [attachment]`\n"
    )

    await ctx.send(formatted_response)



bot.run("MTMyMzQ2MjkyMzM1NTY4NDkzNA.GkWJIw.sQwgS2mC-pigD2V1__HDBS7opa38A5S3qMlPOI")

