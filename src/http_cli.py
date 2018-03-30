# -*- coding: utf-8 -*-

"""Main module."""
from prompt_toolkit import Application
from lib.layout.main_layout import layout
from logging.config import dictConfig
from lib.logger import logging_config
from lib.key_bindins.kbs import global_kb as kb


dictConfig(logging_config)
app = Application(full_screen=True, layout=layout, key_bindings=kb)
