"""A Language Server for OpenSSH configuration files, with a CLI formatter.

Modules

- `ssh_config_ls.cli` — CLI to use implemented functionalities.
- `ssh_config_ls.lsp` — language server declaration.
- `ssh_config_ls.keywords` — definition of language keywords.
- `ssh_config_ls.lexer` — tokenization of SSH config files.
- `ssh_config_ls.parser` — parsing of SSH config tokens.
- `ssh_config_ls.formatter` — formatting of SSH config tree.
- `ssh_config_ls.completion` — completions solver.
- `ssh_config_ls.exceptions` — package exceptions.

## What is ssh-config-ls?

This module is an ongoing prototype of a language server, dedicated to OpenSSH
configuration files. Its current scope includes formatting, real-time error reporting,
and keyword completion.
The prototype is developed in Python and once hitting a mature state, the Rust
implementation will start.

## Why developing a LS for SSH configurations?

This little side project is an excuse to, in order of importance:

- force me to start learning Rust;
- understand LSP;
- work on my unit testing skills;
- revise my knowledge in parsing;
- create an application that I may need 3 minutes in my whole life and I didn't
    find existing.
"""

from importlib.metadata import version

__version__ = version(__name__)
