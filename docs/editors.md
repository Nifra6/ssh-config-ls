---
icon : lucide/plug
---

<!-- LTeX: language=en -->
<!-- rumdl-disable-file code-block-style -->

# Editors

sshls includes a Language Server providing formatting, linting and keyword completion.

The following explains how you can connect sshls to your editor with the `sshls server`, through stdio.

## :simple-neovim: Neovim

If `sshls` is available on your path, you can use Neovim's built-in LSP client (available since Neovim 0.11+) to configure the server:

=== "lsp/sshls.lua"

    ```lua
    return {
        cmd = { "sshls", "server" },
        filetypes = { "sshconfig" },
        root_markers = { "config" },
        settings = {}, -- Put your options there
    }
    ```

=== "init.lua"

    ```lua
    vim.lsp.config["sshls"] = {
        cmd = { "sshls", "server" },
        filetypes = { "sshconfig" },
        root_markers = { "config" },
        settings = {}, -- Put your options there
    }
    ```

Make sure to enable the config in your configuration, such as in `init.lua`:

```lua 
vim.lsp.enable("sshls")
```
