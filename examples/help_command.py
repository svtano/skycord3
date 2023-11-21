import skycord

bot = skycord.Bot()
bot.add_help_command()

if __name__ == "__main__":
    bot.load_cogs("cogs")
    bot.run("TOKEN")  # Replace with your bot token


# You can pass values for the help command in cogs like this:
class Example(skycprd.Cog, name="Example", description="This is a description", emoji="🐍"):
    ...


# You can disable the help command for a cog like this:
class Hidden(skycord.Cog, hidden=True):
    ...


# You can also group all commands in a cog with another existing cog:
# This will use the name and emoji of the grouped cog
class Grouped(skycord.Cog, group="Example"):
    ...
