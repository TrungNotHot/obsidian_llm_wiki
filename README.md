# Obsidian LLM Wiki

Repo chung cho hai bộ wiki, giữ nguyên cấu trúc thư mục và cách sử dụng riêng:

```text
.
├── obsidian_llm_wiki/   # Vault kiến thức tổng quát
├── llm_wiki_4pj/        # Bộ scaffold wiki cho dự án
└── TUTORIAL.md          # Hướng dẫn sử dụng
```

- [Vault kiến thức tổng quát](obsidian_llm_wiki/README.md): mở `obsidian_llm_wiki/` bằng Obsidian.
- [Wiki cho dự án](llm_wiki_4pj/README.md): dùng `llm_wiki_4pj/setup.sh` để tạo scaffold; mở `llm_wiki_4pj/docs/` bằng Obsidian.
- [Hướng dẫn](TUTORIAL.md).

Remote chung: `https://github.com/TrungNotHot/obsidian_llm_wiki`.
Hai thư mục là thư mục thường trong cùng repo, không phải submodule.
Các quy tắc `.gitignore` riêng vẫn áp dụng trong từng thư mục.
File chứa thông tin xác thực là local-only; cấu hình MCP cần thiết lập riêng sau khi clone.
