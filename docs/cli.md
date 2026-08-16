---
icon : lucide/square-terminal
---

<!-- LTeX: language=en -->

# CLI Commands

sshls provides a Command Line Interface to access all its functionalities. The CLI is implemented with [`typer`](https://typer.tiangolo.com/).

For each command or sub commands, you can access some information by adding `--help`.

## Commands

### `format`

Formats the selected file. It requires at least an explicit file path and does not support directories.

```sh
sshls format [OPTIONS] {files}...
```

**Arguments** <!-- rumdl-disable-line no-emphasis-as-heading -->

`files`: List of config files to format.

**Options** <!-- rumdl-disable-line no-emphasis-as-heading -->

`--indent`: Indentation applied to directives inside a block. (default: 4 spaces)

`--separator`: Separator between keywords and their arguments. (default: 1 space)

`--sort-directives` / `--no-sort-directives`: Sort directives within blocks. (default: True)

`--help`: Show the command help.

### `server`

Start the language server in STDIO mode.

**Options** <!-- rumdl-disable-line no-emphasis-as-heading -->

`--help`: Show the command help.

### `version`

Display the tool version.

**Options** <!-- rumdl-disable-line no-emphasis-as-heading -->

`--help`: Show the command help.

## Global options

`--install-completion`: Install completion for the current shell.

`--show-completion`: Show completion for the current shell, to copy it or customize the installation.

`--help`: Show the CLI help.
