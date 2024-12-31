import discord
from discord.ext import commands
import google.generativeai as genai
import json



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
  pp: number
}
for the moves, you can only have 4 of them. You can choose moved already existing in the game or create new ones. However, it must make sense with the description you give me.
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
async def pokemon(ctx: commands.Context, attachment: discord.Attachment):
    if attachment is None:
        await ctx.send("Please attach an image of your 'Pokemon'.")
        return

    result = await attachment.read()
    await ctx.send("Processing the 'pokemon'...")

    response = model.generate_content([prompt, {"data": result, "mime_type": attachment.content_type}])

    json_response = json.loads(response.text)

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

        f"{description}\n"

        f"# Species:\n"
        f"{species}\n"

        f"# Stats:\n"

        f"### Weight:\n"
        f"{weight} kg\n"

        f"### Height:\n"
        f"{height} cm\n"

        f"### HP:\n"
        f"{hp}\n"

        f"### Attack:\n"
        f"{attack}\n"

        f"### Defense:\n"
        f"{defense}\n"

        f"### Special Attack:\n"
        f"{special_attack}\n"

        f"### Special Defense:\n"
        f"{special_defense}\n"

        f"### Speed:\n"
        f"{speed}\n"
        

        f"# Types:\n"
        f"{', '.join(pokemonTypes[int(t)] for t in types)}\n\n"

    )

    await ctx.send(formatted_response)

bot.run("MTMyMzQ2MjkyMzM1NTY4NDkzNA.GkWJIw.sQwgS2mC-pigD2V1__HDBS7opa38A5S3qMlPOI")

