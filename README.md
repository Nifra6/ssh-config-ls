<!-- LTex: disable=false -->
<!-- LTeX: language=en -->

# SSH config formatter

[![Python badge](https://img.shields.io/badge/Python-3.11+-0066cc?style=for-the-badge&logo=python&logoColor=yellow)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://spdx.org/licenses/MIT.html)

[![Packager: uv](https://gitlab.com/nifra/assets/-/raw/main/badges/uv.svg)](https://docs.astral.sh/uv/)
[![Linter/Formatter: ruff](https://gitlab.com/nifra/assets/-/raw/main/badges/ruff.svg)](https://docs.astral.sh/ruff/)
[![Type checker: ty](https://gitlab.com/nifra/assets/-/raw/main/badges/ty.svg)](https://docs.astral.sh/ty/)

Little side project to start learning Rust and explore LSP.

---

<!-- LTeX: language=fr -->

## Formateur de config SSH — Plan de projet

### Étape 1 — Prototype Python

Objectif : valider la logique de parsing et de formatage sans se battre contre un nouveau langage.

**Note :** Couvrir les cas limites (commentaires inline, blocs Host/Match, lignes vides
multiples) et garder les tests sur le comportement observable (entrée/sortie texte) —
ils serviront de spec pour la réécriture Rust.

**Fonctionnalités à implémenter :**

**Lexer :**

- [x] Ajouter des tests sur le tokenizer
- [x] Implémenter un tokenizer pour le cœur de la config
- [x] Ajouter les commentaires dans le tokenizer
- [ ] Écrire tous les tests vicieux imaginables

**Parser :**

- [ ] Ajouter des tests sur le parser
- [x] Implémenter un parser
- [x] Parser les blocs `Host` et `Match`
- [ ] Écrire tous les tests vicieux imaginables

**Formatage :**

- [x] Préserver les commentaires et automatises les lignes vides
- [x] Normaliser l'indentation (4 espaces)
- [x] Canonicaliser la casse des clés (`hostname` → `Hostname`)
- [ ] Écrire tous les tests vicieux imaginables

**CLI :**

- [ ] `ssh-fmt <file>` — formate en place
- [ ] `ssh-fmt --check <file>` — exit code non-zéro si non formaté (CI)
- [ ] `ssh-fmt --diff <file>` — affiche le diff

**LSP :**

- [ ] Lib : [pygls](https://pygls.readthedocs.io/en/latest/)
- [ ] Créer le serveur
- [ ] Ajouter textDocument/formatting

**Hors scope pour l'instant :**

- [ ] Gérer les directives `Include`
- [ ] Trier les blocs (`*` en dernier)

---

### Étape 2 — Apprentissage Rust

Avant de réécrire, poser les bases du langage.

- [ ] Lire les chapitres fondamentaux de [The Book](https://doc.rust-lang.org/book), en particulier sur l'ownership et les enums
- [ ] Faire quelques exercices [Rustlings](https://github.com/rust-lang/rustlings) pour la syntaxe
- [ ] Libs à connaître pour ce projet : `pest` ou `winnow` (parsing), `clap` (CLI)

---

### Étape 3 — Réécriture en Rust

Réécrire le formateur en Rust en s'appuyant sur les tests Python comme spec.

- [ ] Reprendre exactement les mêmes fonctionnalités et la même interface CLI
- [ ] Les tests Python guident l'implémentation et valident la parité de comportement

---

### Étape 4 — Serveur LSP

Transformer le formateur en serveur LSP avec uniquement la capacité de formatage (`textDocument/formatting`).

- [ ] Lib : [`tower-lsp`](https://github.com/ebkalderon/tower-lsp) pour abstraire le protocole JSON-RPC
- [ ] Intégration Neovim via `vim.lsp.start()` ou `nvim-lspconfig` — pas de plugin dédié nécessaire

---

### Références

- [The Rust Book](https://doc.rust-lang.org/book)
- [Rustlings](https://github.com/rust-lang/rustlings)
- [tower-lsp](https://github.com/ebkalderon/tower-lsp)
- [LSP Specification — textDocument/formatting](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_formatting)
