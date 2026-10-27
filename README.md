<!-- LTeX: language=en -->

# SSH-config Language Server (sshls)

<div align="center"> <!-- rumdl-disable-line no-inline-html -->

![sshls logo](https://gitlab.com/uploads/-/system/project/avatar/82167111/logo.png)

[![License](https://img.shields.io/gitlab/license/nifra%2Fssh-config-ls)](https://spdx.org/licenses/MIT.html)
[![PyPI](https://img.shields.io/pypi/v/ssh-config-ls)](https://pypi.org/project/ssh-config-ls/)
[![prek](https://raw.githubusercontent.com/j178/prek/main/docs/assets/badge.svg)](https://github.com/j178/prek)

[**Get started**](https://sshls.nicolasmaignan.fr/installation/) | [**Docs**](https://sshls.nicolasmaignan.fr/)

</div>

A Language Server for OpenSSH configuration files, with a CLI formatter.

## ✨ Features

- Formatting of SSH config files via the `sshls format` command
- Language server started with `sshls server`, following the Language Server Protocol (LSP)
- Formatting, real-time error reporting and keyword completion through the language server

## 📦 Installation

You can install the tool easily with `pipx` or `uv`:

```sh
uv tool install ssh-config-ls
```

## 🧑‍💻 Editor integration

While the formatter can be used from the terminal, the main feature of `sshls` is its server. Since it is compliant with the LSP, it can be more or less easily used with your favorite editor.

### Neovim 0.11+

If `sshls` is available on your path, you can use the `vim.lua` framework to configure the server, in `<rtp>/lsp/sshls.lua`:

```lua
return {
    cmd = { "sshls", "server" },
    filetypes = { "sshconfig" },
    settings = {}, -- Put your options there
}
```

Just do not forget to enable the config:

```lua
vim.lsp.enable("sshls")
```

## 🔧 Configuration

The language server accepts the following options from the client (e.g. Neovim):

```lua
{
    formatter = {
        indent = "    ",  -- Indentation for directives inside Host and Match blocks
        separator = " ",  -- Separator between a keyword and its arguments
        sort_directives = true, -- Sort directives within blocks
    }
}
```

## 🚧 Roadmap

This is the Python prototype of the language server. The following features are currently planned to reach a mature state and a stable API, but additional features may be added as development progresses:

- [x] Implement a lexer
  - [x] Keep comments for easier formatting
- [x] Implement a parser
  - [x] Parse directives blocks (the global one and `Host` and `Match` ones)
- [x] Implement a formatter
  - [x] Remove blocks without directives
  - [x] Indent `Host` and `Match` blocks
  - [x] Sort directives within a block
  - [ ] Sort consecutive `Host` blocks
- [x] Provide a CLI
  - [x] Add the `format` subcommand to format a file
  - [ ] `format`: add a `--check` option to give a status code
  - [ ] `format`: add a `--diff` option to show the difference between the current file and the formatted replacement
  - [x] Add the `server` subcommand to start the language server over STDIO
- [x] Language server
  - [x] `textDocument/formatting`
  - [x] `textDocument/completion`
  - [x] `textDocument/diagnostic` - Report syntax errors
  - [ ] `textDocument/diagnostic` - Report warnings
  - [ ] `textDocument/hover`
- [ ] Test coverage

Once all features have been implemented and the program has reached a mature stage, I will release version 1.0 and start working on the Rust rewrite. Of course, I will continue to fix bugs, but new features will not necessarily be added to the Python implementation in the meantime (and since learning Rust is the main reason I started this project, it will take time).

For the Rust implementation, it is planned to use the `tower-lsp` crate instead of the `pygls` Python module.

### More badges

[![Python badge](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgitlab.com%2Fnifra%2Fssh-config-ls%2F-%2Fraw%2Fmain%2Fpyproject.toml&style=for-the-badge)](https://www.python.org/downloads/)
[![Packager: uv](https://gitlab.com/nifra/assets/-/raw/main/badges/uv.svg)](https://docs.astral.sh/uv/)
[![Linter/Formatter: ruff](https://gitlab.com/nifra/assets/-/raw/main/badges/ruff.svg)](https://docs.astral.sh/ruff/)
[![Type checker: ty](https://gitlab.com/nifra/assets/-/raw/main/badges/ty.svg)](https://docs.astral.sh/ty/)

### References

- [The Rust Book](https://doc.rust-lang.org/book)
- [Rustlings](https://github.com/rust-lang/rustlings)
- [tower-lsp](https://github.com/ebkalderon/tower-lsp)
