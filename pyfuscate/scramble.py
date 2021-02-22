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


def get_random_name():
    return random.choice(alphabet) + "".join(random.choices(alphabet + ints, k=5))


def scramble(text: str):
    """Replaces variable and function names in a block of Python code with randomized names."""
    replacements = {}
    import_replacements = {}
    parsed = copy.deepcopy(ast.parse(text))
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for name in node.names:
                old_name = name.asname or name.name
                new_name = get_random_name()
                import_replacements[old_name] = new_name
                name.asname = new_name
        elif isinstance(node, ast.Name):
            if node.id in import_replacements:
                node.id = import_replacements[node.id]
            elif node.id in replacements:
                node.id = replacements[node.id]
            elif isinstance(node.ctx, ast.Store):
                new_id = get_random_name()
                replacements[node.id] = new_id
                node.id = new_id
        elif isinstance(node, ast.arg):
            if node.arg in import_replacements:
                node.arg = import_replacements[node.arg]
            elif node.arg in replacements:
                node.arg = replacements[node.arg]
            else:
                new_arg = get_random_name()
                replacements[node.arg] = new_arg
                node.arg = new_arg
        elif isinstance(node, ast.Call):
            if node.keywords:
                d = ast.Dict(keys=[], values=[])
                for kw in node.keywords:
                    new_name = ast.Constant(value=kw.arg[::-1], kind=None)
                    n1 = ast.UnaryOp(op=ast.USub(), operand=ast.Constant(value=1, kind=None))
                    d.keys.append(ast.Subscript(value=new_name, slice=ast.Slice(lower=None, upper=None, step=n1, ctx=ast.Load())))
                    d.values.append(kw.value)
                node.keywords = [ast.keyword(arg=None, value=d)]


    return astunparse.unparse(parsed)


if __name__ == '__main__':
    with open('scramble.py', 'r') as fp:
        code = fp.read()
    scrambled = scramble(code)
    with open("fuck.py", "w") as fp:
        fp.write(scrambled)

