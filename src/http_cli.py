# -*- coding: utf-8 -*-

"""Main module."""
from prompt_toolkit import Application
from http_cli_lib.layout.main_layout import layout
from logging.config import dictConfig
from http_cli_lib.logger import logging_config
from http_cli_lib.key_bindins.kbs import global_kb as kb
from prompt_toolkit.enums import EditingMode

dictConfig(logging_config)
app = Application(full_screen=True, layout=layout, key_bindings=kb, editing_mode=EditingMode.VI)
