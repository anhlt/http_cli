from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Label, Frame
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.widgets.toolbars import CompletionsToolbar, ArgToolbar, SearchToolbar, ValidationToolbar, SystemToolbar
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory, ConditionalAutoSuggest
from prompt_toolkit.layout.processors import AppendAutoSuggestion
from .input_area import UrlArea

from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexers.data import JsonLexer

http_completer = WordCompleter([
    'http://', 'https://', 'com', 'org', 'www', 'jp'])

buffer = Buffer()
help_text = "Http"

search_field = SearchToolbar(text_if_not_searching=[
    ('class:not-searching', "Press '/' to start searching.")])

output_field = TextArea(style='class:output-field',
                        scrollbar=True,
                        line_numbers=True,
                        text=help_text,
                        search_field=search_field,
                        lexer=PygmentsLexer(JsonLexer)
                        )

input_field = UrlArea(height=3, prompt='>>> ',
                      style='class:input-field', completer=http_completer, accept_handler=True)


input_field.control.input_processors.append(AppendAutoSuggestion())

container = HSplit([
    Label('Request URL'),
    HSplit([
        Frame(input_field),
        CompletionsToolbar()
    ]),
    HSplit([
        output_field,
        search_field
    ])
])

root_container = VSplit([
    Window(width=10, content=BufferControl(buffer=buffer)),
    Window(width=1, char='|'),
    container,
    ArgToolbar(),
    SystemToolbar(),
    ValidationToolbar(),
])
layout = Layout(root_container)
