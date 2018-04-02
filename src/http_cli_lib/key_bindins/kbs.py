from prompt_toolkit.key_binding import KeyBindings
import logging
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.filters import has_focus
from ..layout.main_layout import input_field, output_field
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_completions
from ..request import make_request
from prompt_toolkit.search import start_search
from prompt_toolkit.key_binding.bindings.auto_suggest import load_auto_suggest_bindings
from prompt_toolkit.key_binding.key_bindings import merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_vi_bindings, load_mouse_bindings

logger = logging.getLogger()

kb = KeyBindings()


@kb.add('c-q')
def exit_(event: KeyPressEvent):
    logger.info('exit')
    event.app.exit()


@kb.add('tab', filter=(~has_completions) & ~has_focus(input_field))
def _(event: KeyPressEvent):
    event.app.layout.focus_next()


@kb.add('s-tab')
def _(event: KeyPressEvent):
    event.app.layout.focus_previous()


@kb.add('enter', filter=has_focus(input_field))
def _(event: KeyPressEvent):
    text = make_request(input_field.text)
    output_field.buffer.document = Document(
        text=text, cursor_position=len(text))
    input_field.add_history(input_field.text)
    input_field.text = ''


@kb.add('c-f', filter=has_focus(output_field))
def _(event: KeyPressEvent):
    start_search(output_field.control)


global_kb = merge_key_bindings([
    kb, load_auto_suggest_bindings(),
    load_mouse_bindings(),
    load_vi_bindings()
])
