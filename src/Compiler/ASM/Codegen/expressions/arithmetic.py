from ...Core.registers import Registers
from ...Core.commands import Commands
from ...Core.types import Types
from ...Runtime.gc import GC

""" Map: arithmetic operator in programming language = arithmetic operator in ASM """
binop_compare_map = {
    '+': {
        'operator': Commands.ADD,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '-': {
        'operator': Commands.SUB,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '*': {
        'operator': Commands.MUL,
        'operands': [Registers.EBX]
    },
    '/': {
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    },
    '%': {
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    }
}


def int_aexp(compiler, node):
    """ Integer compilation """
    compiler.code.add(Commands.MOV, [Registers.EAX, node.i])\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def binop_aexp(compiler, node):
    """ Arithmetic expression compilation """
    node.left.compile_asm(compiler)
    compiler.types.pop()
    node.right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EBX)\
        .add(Commands.POP, Registers.EAX)

    if node.op == '/' or node.op == '%':
        compiler.code.add(Commands.CDQ)

    compiler.code.add(binop_compare_map[node.op]['operator'], binop_compare_map[node.op]['operands'])

    if node.op == '%':
        compiler.code.add(Commands.MOV, [Registers.EAX, Registers.EDX])

    compiler.code.add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def var_aexp(compiler, node):
    """ Variable compilation """
    if node.context == 'assign':
        gc = GC(compiler)

        if compiler.environment.is_exist_local_var(node.name):
            var = compiler.environment.get_local_var(node.name)
            var_type = compiler.environment.get_local_var_runtime_type(node.name)
            compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s]' % Registers.ESP])
            compiler.code.add(Commands.MOV, [var_type, Registers.EAX])
            compiler.environment.update_local_var_type(node.name, node.type)

            compiler.code.add(Commands.MOV, [Registers.EAX, var])
            compiler.code.add(Commands.MOV, [Registers.EBX, var_type])
            gc.decrement()
        else:
            var = compiler.environment.add_local_var(node.type, node.name)
            var_type = compiler.environment.get_local_var_runtime_type(node.name)

        if compiler.environment.defined_object is not None:
            compiler.environment.set_link_object(var, compiler.environment.defined_object)
            compiler.environment.defined_object = None

        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
        gc.increment()

        compiler.code.add(Commands.POP, var_type)
        compiler.code.add(Commands.POP, var)
    else:
        compiler.code.add(Commands.MOV, [Registers.EAX, compiler.environment.get_local_var(node.name)])\
            .add(Commands.PUSH, Registers.EAX)
        runtime_var_type = compiler.environment.get_local_var_runtime_type(node.name)
        compiler.types.set(runtime_var_type)

        var_type = compiler.environment.get_local_var_type(node.name)
        return var_type
