import re
import ast
import copy
import random
import astunparse


# # Variable declaration regex
# #   First capture group: variable name
# #   Second capture group: variable value, any python expression
# variable_declaration = re.compile(r"""(\w+)\s*=\s*([^\s].+)""")

alphabet = "abcdefghijklmnopqrstuvwvyz"
alphabet += alphabet.upper()
ints = "1234567890_"


def scramble(text: str):
    """Replaces variable and function names in a block of Python code with randomized names."""
    replacements = {}
    parsed = copy.deepcopy(ast.parse(text))
    for node in ast.walk(parsed):
        if isinstance(node, ast.Name):
            if node.id in replacements:
                node.id = replacements[node.id]
            elif isinstance(node.ctx, ast.Store):
                new_id = random.choice(alphabet) + "".join(random.choices(alphabet+ints, k=5))
                replacements[node.id] = new_id
                node.id = new_id

    return astunparse.unparse(parsed)


code = """

from discord.ext import commands


bot = commands.Bot(command_prefix="!")

@bot.command()
async def test(ctx):
    await ctx.send("ok")

bot.run("token")

"""

if __name__ == '__main__':
    with open("fuck.py", "w") as fp:
        fp.write(scramble(code))

