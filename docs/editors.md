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

??? question "The server does not start for my included file. What is happening?"
    The server is only started on buffers whose filetype is `sshconfig`, and
    Neovim only detects that filetype for a few files: `~/.ssh/config`,
    `/etc/ssh/ssh_config`, and `.conf` files in `~/.ssh/` and
    `/etc/ssh/ssh_config.d`. A file pulled in with `Include` under another
    name or location is not detected.

    Check with `:set filetype?`. If it is not `sshconfig`, extend the
    detection with `vim.filetype.add()`:

    ```lua
    vim.filetype.add({
        pattern = {
            [".*/%.ssh/config%.d/.*"] = "sshconfig",
        },
    })
    ```
