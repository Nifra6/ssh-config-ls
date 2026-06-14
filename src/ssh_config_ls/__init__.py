"""An SSH config formatter, usable as a Language Server Protocol (LSP) plugin.

Modules

- `ssh_config_ls.lexer` — tokenization of SSH config files.
- `ssh_config_ls.parser` — parsing of SSH config tokens.
- `ssh_config_ls.formatter` — formatting of SSH config tree.
- `ssh_config_ls.exceptions` — package exceptions.

## What is ssh-config-ls?

This module is an ongoing prototype of a language server, dedicated to OpenSSH
configuration files. Its current planned scope is to be usable as a formatter
and potentially lint some errors (detected through the parsing of the file).
The prototype is developed in Python and once hitting a mature state, the Rust
implementation will start.

## Why developing a LS for SSH configurations?

This little side project is an excuse to, in order of importance:

- force me to start learning Rust;
- understand LSP;
- work my unit testing;
- revise my knowledge in parsing;
- create an application that I may need 3 minutes in my whole life and I didn't
    find existing.
"""

from importlib.metadata import version

__version__ = version(__name__)
