from __future__ import unicode_literals

import re
import six
import logging
try:
    from collections import OrderedDict
except ImportError:  # For Python 2.6, nocover
    from ordereddict import OrderedDict

from itertools import chain
from prompt_toolkit.completion import Completer, Completion
from six.moves.urllib.parse import urlparse
from .completion import (ACTIONS, HEADER_NAMES, HEADER_VALUES)

logger = logging.getLogger()

RULES = [
    # (regex pattern, a method name in CompletionGenerator)
    (r'^(?![\s\S])', 'start_query'),
    (r'((?:[^\s\'"\\=:]|(?:\\.))+):((?:[^\s\'"\\]|(?:\\.))*)$',
     'header_values'),

    (r'(get|head|post|put|patch|delete)\s+', 'concat_mutations'),
    (r'rm\s+\-b\s+', 'existing_body_params'),
    (r'rm\s+\-h\s+', 'existing_header_names'),
    (r'rm\s+\-o\s+', 'existing_option_names'),
    (r'rm\s+\-q\s+', 'existing_querystring_params'),

    # The last two captures are full URL path and the last part of the URL
    # path. For example:
    # '/foo/bar' => ('/foo/bar', 'bar')
    # '/foo/bar/' => ('/foo/bar/', '')
    # 'foo/bar' => ('foo/bar', 'bar')
    # (r'(ls|cd)\s+(/?(?:[^/]+/)*([^/]*)/?)$', 'urlpaths'),
    # (r'^\s*[^\s]*$', 'root_commands')
]


def compile_rules(rules):
    compiled_rules = []
    for pattern, meta_dict in rules:
        regex = re.compile(pattern)
        compiled_rules.append((regex, meta_dict))
    return compiled_rules


RULES = compile_rules(RULES)


def fuzzyfinder(text, collection):
    """https://github.com/amjith/fuzzyfinder"""
    suggestions = []
    if not isinstance(text, six.text_type):
        text = six.u(text)
    pat = '.*?'.join(map(re.escape, text))
    regex = re.compile(pat, flags=re.IGNORECASE)
    for item in collection:
        r = regex.search(item)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    return (z for _, _, z in sorted(suggestions))


def match_completions(cur_word, word_dict):
    logger.debug(cur_word, word_dict)
    words = word_dict.keys()
    suggestions = fuzzyfinder(cur_word, words)
    for word in suggestions:
        desc = word_dict.get(word, '')
        yield Completion(word, -len(cur_word), display_meta=desc)


class CompletionGenerator(object):

    def header_values(self, context, match):
        header_name = match.group(1)
        header_values = HEADER_VALUES.get(header_name)
        if header_values:
            for value in header_values:
                yield value, header_name

    def actions(self, context, match):
        logger.debug('actions')
        return self._generic_generate(ACTIONS.keys(), {}, ACTIONS)

    def concat_mutations(self, context, match):
        logger.debug('concat_mutations')
        return chain(
            self._generic_generate(context.body_params.keys(),
                                   context.body_params, 'Body parameter'),
            self._generic_generate(context.querystring_params.keys(),
                                   context.querystring_params,
                                   'Querystring parameter'),
            self._generic_generate(HEADER_NAMES.keys(),
                                   context.headers, HEADER_NAMES),
        )

    def start_query(self, context, match):
        logger.debug(ACTIONS)
        return self._generic_generate(ACTIONS.keys(), {}, ACTIONS)

    def existing_body_params(self, context, match):
        params = context.body_params.copy()
        params.update(context.body_json_params)
        return self._generic_generate(params.keys(), params, 'Body parameter')

    def existing_querystring_params(self, context, match):
        return self._generic_generate(
            context.querystring_params.keys(),
            context.querystring_params, 'Querystring parameter')

    def existing_header_names(self, context, match):
        return self._generic_generate(context.headers.keys(),
                                      context.headers, HEADER_NAMES)

    def urlpaths(self, context, match):
        path = urlparse(context.url).path.split('/')
        overrided_path = match.group(2)
        if overrided_path:
            if overrided_path.startswith('/'):
                # Absolute path
                path = []
            path += overrided_path.split('/')[:-1]
        names = [
            node.name for node in context.root.ls(*path)
            if node.data.get('type') == 'dir'
        ]
        return self._generic_generate(names, {}, 'Endpoint')

    def _generic_generate(self, names, values, descs):
        for name in sorted(names):
            if isinstance(descs, six.string_types):
                desc = descs
            else:
                desc = descs.get(name, '')
            if name in values:
                value = values[name]
                if value is None:
                    desc += ' (on)'
                else:
                    value = six.text_type(value)
                    if len(value) > 16:
                        value = value[:13] + '...'
                    desc += ' (=%s)' % value
            yield name, desc


class HttpPromptCompleter(Completer):

    def __init__(self, context):
        logger.debug('init')
        self.context = context
        self.comp_gen = CompletionGenerator()

    def get_completions(self, document, complete_event):
        logger.debug(document.text_before_cursor)
        cur_text = document.text_before_cursor
        cur_word = None
        word_dict = None

        for regex, method_name in RULES:
            match = regex.search(cur_text)
            logger.debug(match)
            if match:
                gen_completions = getattr(self.comp_gen, method_name)
                completions = gen_completions(self.context, match)
                logger.debug(method_name)
                word_dict = OrderedDict(completions)
                logger.debug(word_dict)
                groups = match.groups()
                if len(groups) > 1:
                    cur_word = groups[-1]
                else:
                    cur_word = document.get_word_before_cursor(WORD=True)

                break

        if word_dict:
            for comp in match_completions(cur_word, word_dict):
                yield comp
