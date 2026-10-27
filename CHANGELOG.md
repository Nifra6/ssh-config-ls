<!-- LTeX: language=en -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.2] - 2026-10-27

### Added

- Add a changelog following the [Keep a Changelog] format.
- Add a configuration doc section for the language server settings.
- Add keywords to the package metadata.
- Document the `sshconfig` filetype in the Neovim integration page.

### Changed

- Updated to Python 3.15, which is now the minimum supported version.
- Use `lazy` import keyword instead of importing within CLI function.
- Ensure all URLs use HTTPS.
- Update [prek] hooks and dev dependencies.
- Use the official [ty] [prek] hook instead of a local hook.
- README intro have been cleaned.

### Security

- Update [uv] to 0.13.5, fixing the
  [eMudhra intermediate CA compromise](https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576).

## [0.10.1] - 2026-08-16

### Added

- `sshls format` now accepts multiple files.
- `sshls format` now prints how many files have been formatted or left unchanged.

## [0.10.0] - 2026-08-11

### Added

- A `KeywordDef` class to define properties for each keyword.

### Changed

- The `Keyword` StrEnum class defined in `lexer.py` has been replaced by an `Enum` in `keywords.py`.
- Members of `Keyword` are now UPPERCASE instead of CamelCase.

## [0.9.1] - 2026-08-10

### Changed

- The "Bad configuration option" error has been renamed "E001". Its description has been changed to "The keyword `{keyword}` is unknown.".
- The "No argument after keyword" error has been renamed "E002".

## [0.9.0] - 2026-08-10

### Added

- The server now publishes diagnostics (`textDocument/publishDiagnostics`) when an SSH config file is opened or changed.
- A new function `tokenize_with_errors` that returns the caught `SSHConfigError`s alongside the tokens when applying the lexer.
- For now, two errors are diagnosed:
  - If an unknown keyword is used, send an error with the description "Bad configuration option: `{keyword}` is unknown.".
  - If a keyword is alone on its line (i.e. without argument), send an error with the description "No argument after keyword.".
- The `KeywordArgToken` now takes an additional `line_number` field to link to the file line number.

## [0.8.2] - 2026-08-10

### Changed

- Keyword completion now works when the cursor is anywhere in the keyword (i.e. the first word of the line).

## [0.8.1] - 2026-08-07

### Changed

- Completion for keywords is now enabled when other words are on the line.

## [0.8.0] - 2026-08-07

### Added

- `textDocument/completion` capability added to the server for keywords.
- Tests for exceptions raised on an invalid indent or separator when formatting.

## [0.7.7] - 2026-07-09

### Fixed

- Arguments starting with `=` are now quoted to preserve idempotency when formatting.

## [0.7.6] - 2026-06-27

### Added

- CLI command `sshls version` to print the package version.
- [PyPI] badge in the README.
- Idempotency tests for the parser and the formatter.

### Changed

- Corrected CLI commands in the README.
- Use the [PyPI] package name in the README installation section.

## [0.7.5] - 2026-06-27

### Changed

- Exceptions are now caught silently when formatting with the language server.

### Fixed

- Fix CI package publishing by adding a [PyPI] token.

## [0.7.4] - 2026-06-27

### Added

- A new argument `sort_directives` to disable sorting within blocks when formatting (enabled by default).
- The package is now published to [PyPI] for each Git tag, through CI and the [uv] build system.

## [0.7.3] - 2026-06-27

### Changed

- By default, `sshls` and `sshls format` now show help when run without arguments.

## [0.7.2] - 2026-06-22

### Added

- Directives are now sorted within blocks if there is no standalone comment in the block.

## [0.7.1] - 2026-06-22

### Changed

- Formatting no longer adds an extra empty line at the end of the file.

## [0.7.0] - 2026-06-19

### Added

- The language server has been implemented with the [pygls] dependency.
- `textDocument/formatting` capability added to the language server.
- `sshls server` launches the language server.

## [0.6.3] - 2026-06-16

### Added

- Indent and keyword-argument separator are now options of the `sshls format` CLI.
- Indent and keyword-argument separator defaults are now named `DEFAULT_INDENT` and `DEFAULT_SEPARATOR` constants.

## [0.6.2] - 2026-06-15

### Added

- Type alias `SSHBlock` for the union of the three config blocks `GlobalBlock`, `HostBlock` and `MatchBlock`.

### Changed

- Replaced the `for` loop in syntax tree formatting with a list comprehension.

## [0.6.1] - 2026-06-15

### Added

- Formatting removes blocks if they are empty (i.e. without directives).

## [0.6.0] - 2026-06-15

### Added

- A CLI has been created through the `sshls` interface, implemented with the [typer] dependency.
- Formatting is available in the CLI with the `sshls format` command.
- `sshls server` is reserved for the language server, to be implemented.

## [0.5.0] - 2026-06-14

### Added

- The formatter has been implemented, used through the `format_tree` function.
- Tests for the formatter.

## [0.4.0] - 2026-06-14

### Added

- Type checks with [ty] as a local [prek] hook.

### Changed

- The tokenizer has been renamed lexer.

## [0.3.0] - 2026-06-05

### Added

- The parser has been implemented, used through the `parse` function.
- Tests for the parser.

## [0.2.1] - 2026-05-29

### Added

- Module docstring long description.
- CI has been added, with [ruff] check/format.
- `check-yaml` added to [prek] hooks.
- Documentation is published with [pdoc] through CI and added to the project URLs.
- `pdoc`, `ruff` and `ty` have been added as dev dependencies.

### Changed

- The repository has been renamed `ssh-config-ls`.
- `pytest` has been moved from dependencies to dev dependencies.

## [0.2.0] - 2026-05-27

### Added

- Add [prek] hooks: `check-toml`, `end-of-file-fixer`, ruff formatting.
- The tokenizer now consumes comments instead of discarding them.

### Changed

- The `LineToken` named type, representing a tokenized config line, has been replaced by the frozen dataclass `KeywordArgToken`, with an optional comment property.

### Fixed

- Add `uv run` prefix to the [prek] hook of [pytest].

## [0.1.0] - 2026-05-27

### Added

- Plan for the development in the README.
- MIT licence.
- [prek] hooks with [ruff] checks and [pytest] checks.
- Create the `ssh-config-ls` package, with [pytest] as a dependency.
- A tokenizer (or lexer) with the `tokenize` function, using keywords described in the `Keyword` StrEnum.
- Tests for the tokenizer.

[unreleased]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.10.2...main
[0.10.2]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.10.1...v0.10.2
[0.10.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.10.0...v0.10.1
[0.10.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.9.1...v0.10.0
[0.9.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.9.0...v0.9.1
[0.9.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.8.2...v0.9.0
[0.8.2]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.8.1...v0.8.2
[0.8.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.8.0...v0.8.1
[0.8.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.7...v0.8.0
[0.7.7]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.6...v0.7.7
[0.7.6]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.5...v0.7.6
[0.7.5]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.4...v0.7.5
[0.7.4]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.3...v0.7.4
[0.7.3]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.2...v0.7.3
[0.7.2]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.1...v0.7.2
[0.7.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.7.0...v0.7.1
[0.7.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.6.3...v0.7.0
[0.6.3]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.6.2...v0.6.3
[0.6.2]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.6.1...v0.6.2
[0.6.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.6.0...v0.6.1
[0.6.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.5.0...v0.6.0
[0.5.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.4.0...v0.5.0
[0.4.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.2.1...v0.3.0
[0.2.1]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.2.0...v0.2.1
[0.2.0]: https://gitlab.com/nifra/ssh-config-ls/-/compare/v0.1.0...v0.2.0
[0.1.0]: https://gitlab.com/nifra/ssh-config-ls/-/commits/v0.1.0
[Keep a Changelog]: https://keepachangelog.com/en/1.1.0/
[pdoc]: https://pdoc.dev/
[prek]: https://prek.j178.dev/
[pypi]: https://pypi.org/project/ssh-config-ls/
[pygls]: https://pygls.readthedocs.io/en/latest/
[pytest]: https://docs.pytest.org/en/stable/
[ruff]: https://docs.astral.sh/ruff/
[ty]: https://docs.astral.sh/ty/
[typer]: https://typer.tiangolo.com/
[uv]: https://docs.astral.sh/uv/
