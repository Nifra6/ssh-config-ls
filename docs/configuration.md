---
icon : lucide/settings
---

<!-- LTeX: language=en -->

# Configuration

For now, the language server can only be configured by the client (i.e. your editor). It accepts the following settings:

```toml
[formatter]
indent = "    "         # Indentation for directives inside Host and Match blocks
separator = " "         # Separator between a keyword and its arguments
sort_directives = true  # Sort directives within blocks
```
