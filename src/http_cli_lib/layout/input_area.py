from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
import six
from prompt_toolkit.widgets.toolbars import SearchToolbar
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.layout.margins import ScrollbarMargin, NumberedMargin
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


class UrlArea(object):

    """
    A simple input field.
    This contains a ``prompt_toolkit`` ``Buffer`` object that hold the text
    data structure for the edited buffer, the ``BufferControl``, which applies
    a ``Lexer`` to the text and turns it into a ``UIControl``, and finally,
    this ``UIControl`` is wrapped in a ``Window`` object (just like any
    ``UIControl``), which is responsible for the scrolling.
    This widget does have some options, but it does not intend to cover every
    single use case. For more configurations options, you can always build a
    text area manually, using a ``Buffer``, ``BufferControl`` and ``Window``.
    :param text: The initial text.
    :param multiline: If True, allow multiline input.
    :param lexer: ``Lexer`` instance for syntax highlighting.
    :param completer: ``Completer`` instance for auto completion.
    :param focusable: When `True`, allow this widget to receive the focus.
    :param wrap_lines: When `True`, don't scroll horizontally, but wrap lines.
    :param width: Window width. (``Dimension`` object.)
    :param height: Window height. (``Dimension`` object.)
    :param password: When `True`, display using asterisks.
    :param accept_handler: Called when `Enter` is pressed.
    :param scrollbar: When `True`, display a scroll bar.
    :param search_field: An optional `SearchToolbar` object.
    :param style: A style string.
    :param dont_extend_height:
    :param dont_extend_width:
    """

    def __init__(self, text='', multiline=True, password=False,
                 lexer=None, completer=None, accept_handler=None,
                 focusable=True, wrap_lines=True, read_only=False,
                 width=None, height=None,
                 dont_extend_height=False, dont_extend_width=False,
                 line_numbers=False, scrollbar=False, style='',
                 search_field=None, preview_search=True,
                 history=InMemoryHistory(),
                 prompt=''):
        assert isinstance(text, six.text_type)
        assert search_field is None or isinstance(search_field, SearchToolbar)

        if search_field is None:
            search_control = None
        elif isinstance(search_field, SearchToolbar):
            search_control = search_field.control

        self.history = history

        self.buffer = Buffer(
            document=Document(text, 0),
            multiline=multiline,
            read_only=read_only,
            completer=completer,
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            accept_handler=lambda buff: accept_handler and accept_handler())

        self.control = BufferControl(
            buffer=self.buffer,
            lexer=lexer,
            input_processors=[
                BeforeInput(prompt, style='class:text-area.prompt'),
            ],
            search_buffer_control=search_control,
            preview_search=preview_search,
            focusable=focusable)

        if multiline:
            if scrollbar:
                right_margins = [ScrollbarMargin(display_arrows=True)]
            else:
                right_margins = []
            if line_numbers:
                left_margins = [NumberedMargin()]
            else:
                left_margins = []
        else:
            wrap_lines = False  # Never wrap for single line input.
            height = D.exact(1)
            left_margins = []
            right_margins = []

        style = 'class:text-area ' + style

        self.window = Window(
            height=height,
            width=width,
            dont_extend_height=dont_extend_height,
            dont_extend_width=dont_extend_width,
            content=self.control,
            style=style,
            wrap_lines=wrap_lines,
            left_margins=left_margins,
            right_margins=right_margins)

    @property
    def text(self):
        return self.buffer.text

    @text.setter
    def text(self, value):
        self.buffer.document = Document(value, 0)

    @property
    def document(self):
        return self.buffer.document

    def add_history(self, text):
        self.history.append(text)

    @document.setter
    def document(self, value):
        self.buffer.document = value

    def __pt_container__(self):
        return self.window
