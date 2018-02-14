from ..Core.types import Types
from ..Core.commands import Commands
from ..Core.registers import Registers
from ..Utils.atoi import *


class GC(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if GC.is_loaded:
            return

        self.load('gc.asm')
        GC.is_loaded = True

    def run(self):
        self.compiler.code.add(Commands.CALL, ['gc'])

    def increment(self):
        self.compiler.code.add(Commands.CALL, ['gc.gc_increment'])

    def check_args(self, args):
        for arg in args:
            var_pointer = self.compiler.environment.get_local_var(arg)
            var_type_pointer = self.compiler.environment.get_local_var_runtime_type(arg)
            self.compiler.code.add(Commands.MOV, [Registers.EAX, var_pointer])
            self.compiler.code.add(Commands.MOV, [Registers.EBX, var_type_pointer])
            self.compiler.code.add(Commands.CALL, ['gc.gc_start_if_need'])
