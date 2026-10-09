# Obsidian LLM Wiki

One repository containing two separate wiki projects, each with its own structure and workflow:

```text
.
├── obsidian_llm_wiki/   # General knowledge vault
├── llm_wiki_4pj/        # Wiki scaffold for software projects
└── TUTORIAL.md          # Setup and usage guide
```

- [General knowledge vault](obsidian_llm_wiki/README.md): open `obsidian_llm_wiki/` in Obsidian.
- [Project wiki scaffold](llm_wiki_4pj/README.md): use `llm_wiki_4pj/setup.sh` to scaffold a project; open `llm_wiki_4pj/docs/` in Obsidian to explore the template.
- [Setup and usage guide](TUTORIAL.md).

Shared remote: `https://github.com/TrungNotHot/obsidian_llm_wiki`.
Both projects are regular directories in the same repository, not submodules.
The only `.git` directory is at the repository root. Each project has its own `.gitignore`; there is no root `.gitignore`.
Files matching `.env*` stay local. MCP configuration files are versioned and reference environment variables.
