from Helpers.string import *

def char(commands, env, character):
    commands.add(Push, ord(character))

def string(commands, env, characters):
    commands.add(Push, 0)
    for character in characters:
        char(commands, env, character)

def strlen(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    String.compile_strlen(commands, env)

def strget(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    String.compile_strget(commands, env)

def strset(commands, env, args):
    args.elements[0].compile_vm(commands, env)
    args.elements[1].compile_vm(commands, env)
    args.elements[2].compile_vm(commands, env)
    String.compile_strset(commands, env)