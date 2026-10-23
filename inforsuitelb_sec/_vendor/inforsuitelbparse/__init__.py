# -*- coding: utf-8 -*-
from .parser import parse, parse_string
from .lexer import lex, lex_string
from .builder import build
from .formatter import format
from .ext.lua import LuaBlockPlugin

__all__ = ['parse', 'parse_string', 'lex', 'lex_string', 'build', 'format']

__title__ = 'inforsuitelbparse'
__summary__ = 'InforSuiteLB configuration file parser.'
__version__ = '2.0.3.3'

default_enabled_extensions = [LuaBlockPlugin()]
for extension in default_enabled_extensions:
    extension.register_extension()
