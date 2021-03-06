# Sublime Text Plugin
# apiDocAutocompletion adds apiDoc tags to list of code completion suggestions.
# Project: https://github.com/DWand/SublimeText_apiDoc_autocompletion
# License: MIT

import sublime
import sublime_plugin
import re

SETTINGS_FILENAME = 'apiDocAutocompletion.sublime-settings'


def is_line_start(view, location):
    """
    Determines whether the given location is situated on beginning of the comment line
    Returns:
        bool: True if the location is situated in the beginning of the comment line,
              False otherwise
    """
    word_bounds = view.word(location)
    line_bounds = view.line(location)
    prefix_bounds = sublime.Region(line_bounds.begin(), word_bounds.begin())
    prefix = view.substr(prefix_bounds)
    return re.search('\w', prefix) == None


class apiDocAutocompletion(sublime_plugin.EventListener):
    _suggestions = [
        ("@api\tapiDoc", "@api {${1:method}} ${2:path} ${3:[title]}"),
        ("@apiDefine\tapiDoc", "@apiDefine ${1:name} ${2:[title]}\n${3:* }           ${4:[description]}"),
        ("@apiDescription\tapiDoc", "@apiDescription ${1:text}"),
        ("@apiError\tapiDoc", "@apiError ${1:[(group)]} ${2:[{type\}]} ${3:field} ${4:[description]}"),
        ("@apiErrorExample\tapiDoc", "@apiErrorExample ${1:[{type\}]} ${2:[title]}\n${3:* }${4:example}"),
        ("@apiExample\tapiDoc", "@apiExample ${1:[{type\}]} ${2:title}\n${3:* }${4:example}"),
        ("@apiGroup\tapiDoc", "@apiGroup ${1:name}"),
        ("@apiHeader\tapiDoc", "@apiHeader ${1:[(group)]} ${2:[{type\}]} ${3:[field=defaultValue]} ${4:[description]}"),
        ("@apiHeaderExample\tapiDoc", "@apiHeaderExample ${1:[{type\}]} ${2:[title]}\n${3:* }${4:example}"),
        ("@apiIgnore\tapiDoc", "@apiIgnore ${1:[hint]}"),
        ("@apiName\tapiDoc", "@apiName ${1:name}"),
        ("@apiParam\tapiDoc", "@apiParam ${1:[(group)]} ${2:[{type\}]} ${3:[field=defaultValue]} ${4:[description]}"),
        ("@apiParamExample\tapiDoc", "@apiParamExample ${1:[{type\}]} ${2:[title]}\n${3:* }${4:example}"),
        ("@apiPermission\tapiDoc", "@apiPermission ${1:name}"),
        ("@apiSampleRequest\tapiDoc", "@apiSampleRequest ${1:url}"),
        ("@apiSuccess\tapiDoc", "@apiSuccess ${1:[(group)]} ${2:[{type\}]} ${3:field} ${4:[description]}"),
        ("@apiSuccessExample\tapiDoc", "@apiSuccessExample ${1:[{type\}]} ${2:[title]}\n${3:* }${4:example}"),
        ("@apiUse\tapiDoc", "@apiUse ${1:name}"),
        ("@apiVersion\tapiDoc", "@apiVersion ${1:version}"),
    ]

    def on_query_completions(self, view, prefix, locations):
        settings = sublime.load_settings(SETTINGS_FILENAME)

        plugin_disabled = settings.get('disabled', False)
        if plugin_disabled:
            return None

        # Block comment scopes:
        # C#:
        #     source.cs comment.block.source.cs
        # Go:
        #     source.go comment.block.go
        # Dart:
        #     -
        # Java:
        #     source.java comment.block.documentation.javadoc meta.documentation.comment.javadoc text.html
        # JavaScript:
        #     source.js comment.block.documentation.js
        # PHP:
        #     text.html.basic source.php.embedded.block.html comment.block.documentation.phpdoc.php
        # CoffeeScript:
        #     source.coffee comment.block.coffee
        # Erlang:
        #     source.erlang
        # Perl:
        #     source.perl meta.comment.full-line.perl comment.line.number-sign.perl
        #     source.perl comment.block.documentation.perl
        # Python:
        #     source.python string.quoted.double.block.python
        # Ruby:
        #     source.ruby comment.block.documentation.ruby
        # Clojure:
        #     source.clojure comment.line.semicolon.double.clojure

        target_scopes = [
            "comment.block",
            "source.perl meta.comment.full-line.perl comment.line.number-sign.perl",
            "source.python string.quoted.double.block.python",
            "source.erlang",
            "source.clojure comment.line.semicolon.double.clojure",
        ]

        location = locations[0]
        current_scope = view.scope_name(location)

        if any(scope in current_scope for scope in target_scopes) == True:
            if is_line_start(view, location):
                return apiDocAutocompletion._suggestions

        return None
