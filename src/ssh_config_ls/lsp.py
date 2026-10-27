"""Describe the Language Server."""

from importlib.metadata import version

from lsprotocol import types
from pygls.lsp.server import LanguageServer
lazy from pygls.workspace import TextDocument

from ssh_config_ls.completion import get_completion
from ssh_config_ls.formatter import DEFAULT_INDENT, DEFAULT_SEPARATOR, format_tree
from ssh_config_ls.lexer import tokenize, tokenize_with_errors
from ssh_config_ls.parser import DEFAULT_SORT, parse

# ------------------------------------------------------------
# SERVER
# ------------------------------------------------------------

server = LanguageServer("ssh-config-ls", version("ssh_config_ls"))
"""SSH config language server."""

# ------------------------------------------------------------
# CAPABILITIES
# ------------------------------------------------------------


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: types.DidOpenTextDocumentParams) -> None:
    """Parse a document when it is opened."""
    document = server.workspace.get_text_document(params.text_document.uri)
    _publish_diagnostics(ls, document)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams) -> None:
    """Parse a document when it is changed."""
    document = server.workspace.get_text_document(params.text_document.uri)
    _publish_diagnostics(ls, document)


@server.feature(types.TEXT_DOCUMENT_FORMATTING)
async def format_document(
    ls: LanguageServer, params: types.DocumentFormattingParams
) -> list[types.TextEdit]:
    """Format the whole document."""
    config = await ls.workspace_configuration_async(
        types.ConfigurationParams(items=[types.ConfigurationItem(section="formatter")])
    )

    formatter_config = config[0] or {}
    indent = formatter_config.get("indent", DEFAULT_INDENT)
    separator = formatter_config.get("separator", DEFAULT_SEPARATOR)
    sort_directives = formatter_config.get("sort_directives", DEFAULT_SORT)

    doc = ls.workspace.get_text_document(params.text_document.uri)
    text = doc.source

    try:
        formatted = format_tree(
            parse(tokenize(text), sort_directives=sort_directives),
            indent=indent,
            separator=separator,
        )
    except ValueError:
        return []

    lines = text.splitlines()
    if lines:
        last_line = len(lines) - 1
        last_char = len(lines[last_line])
    else:
        last_line, last_char = 0, 0

    return [
        types.TextEdit(
            range=types.Range(
                start=types.Position(line=0, character=0),
                end=types.Position(line=last_line, character=last_char),
            ),
            new_text=formatted,
        )
    ]


@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completion(params: types.CompletionParams) -> list[types.CompletionItem]:
    """Provide completions for a keyword."""
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line]

    return [
        types.CompletionItem(label=word)
        for word in get_completion(current_line, params.position.character)
    ]


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _publish_diagnostics(ls: LanguageServer, document: TextDocument) -> None:
    """Publish diagnostics to the client."""
    _, errors = tokenize_with_errors(document.source)

    diagnostics = [
        types.Diagnostic(
            range=types.Range(
                start=types.Position(line=e.line, character=e.positions[0]),
                end=types.Position(line=e.line, character=e.positions[1]),
            ),
            message=str(e),
            severity=types.DiagnosticSeverity.Error,
            code=e.code,
            source="sshls",
        )
        for e in errors
    ]

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri, diagnostics=diagnostics, version=document.version
        )
    )
