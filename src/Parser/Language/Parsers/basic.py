from src.Parser.combinators import *
from src.consts import *

"""
Language keywords parsing (Reserved combinator with 'RESERVED' tag).
"""
def keyword(kw):
    return Reserved(kw, RESERVED)

"""
Integers parsing (Tag combinator with 'INT' tag).
A Process combinator (^ operator) is also used to convert token into an integer.
"""
num = Tag(INT) ^ (lambda i: int(i))

"""
Identifiers parsing (Tag combinator with 'ID' tag).
"""
id = Tag(ID)
