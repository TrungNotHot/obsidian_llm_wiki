# Tutorial: LLM Wiki — `llm_wiki_4pj` + `obsidian_llm_wiki`

Hai folder này là **một hệ thống**, dựa trên ý tưởng LLM Wiki của Andrej Karpathy (+ Hermes Agent): AI agent viết và bảo trì wiki, con người đọc/duyệt bằng Obsidian.

| | `llm_wiki_4pj` | `obsidian_llm_wiki` |
|---|---|---|
| Vai trò | **Template** nhúng vào từng project (repo code) | **Vault trung tâm** (General Knowledge Base), độc lập project |
| Vị trí wiki | `<project>/docs/` | gốc repo (`raw/`, `wiki/`, `reports/`) |
| Phân vùng note | `universal/` (dùng lại được) + `local/` (riêng project) | `concepts/`, `entities/` phẳng (toàn là kiến thức chung) |
| Git | note **được track** cùng code | note **gitignored** (local-only) |
| Skill riêng | — | `/kb-colluni` |
| Skill chung | `/kb-compile` `/kb-report` `/kb-index` `/kb-health` | giống bên trái |

## 1. Luồng tổng thể

```
 Project A (llm_wiki_4pj)        Project B (llm_wiki_4pj)
 docs/wiki/*/universal/          docs/wiki/*/universal/
          \                         /
           \__  /kb-colluni  _______/      (rewrite, bỏ chi tiết riêng project)
                     v
        obsidian_llm_wiki/raw/articles/    (raw, KHÔNG có [[wikilink]])
                     v  /kb-compile
        obsidian_llm_wiki/wiki/concepts|entities/
                     v  /kb-report
        obsidian_llm_wiki/reports/
```

Tức là: làm việc hằng ngày trong project → tri thức tái sử dụng nằm ở `universal/` → định kỳ gom về vault trung tâm.

## 2. Ba layer (giống nhau ở cả hai)

| Layer | Thư mục | Quy tắc |
|---|---|---|
| Raw | `raw/` | Bất biến: web clip, spec, PDF/DOCX đã convert. Frontmatter có `source_url`/`source_file`, `ingested`, `sha256`. |
| Wiki | `wiki/` | Note sống, agent bảo trì: `concepts/`, `entities/`, `easy_read/`, `_archive/`, `TODO.md`. |
| Reports | `reports/` | Câu trả lời lâu dài. *Never answer in chat, always answer in files.* |

File quản trị: `SCHEMA.md` (hiến pháp), `index.md` (catalog + glossary), `log.md` (log append-only). Ở `llm_wiki_4pj` chúng nằm trong `docs/`.

## 3. Chuẩn bị

- Agent đọc `CLAUDE.md`/`AGENTS.md` và hỗ trợ skills (Claude Code là chuẩn). Python 3 cho script của `kb-health`, `kb-compile`.
- [Obsidian](https://obsidian.md) để xem graph/backlinks.
- (Tuỳ chọn) MCP Obsidian: cài plugin **Local REST API** (port `27124`), cần `uvx`, rồi `export OBSIDIAN_API_KEY=...` (cấu hình trong `.mcp.json`). Không có MCP agent vẫn sửa file trực tiếp được.

## 4. Cài vault trung tâm (`obsidian_llm_wiki`)

1. Obsidian → *Open folder as vault* → chọn `obsidian_llm_wiki` (thư mục gốc).
2. Nếu thiếu `index.md`/`log.md`: copy từ `index.example.md`/`log.example.md`.
3. Sửa dòng **Domain** và tag taxonomy trong `SCHEMA.md` nếu cần (tag mới phải thêm vào schema **trước**).
4. Chạy Claude Code tại thư mục này.

## 5. Gắn wiki vào một project (`llm_wiki_4pj`)

```bash
cd llm_wiki_4pj
./setup.sh /path/to/your-project
cp CLAUDE.md /path/to/your-project/    # setup.sh chỉ copy AGENTS.md, không copy CLAUDE.md
```

`setup.sh` copy (không ghi đè) `.agents/`, `.claude/`, `.mcp.json`, `AGENTS.md`, `docs/` (kèm `docs/.obsidian`), chmod script, và thêm rule ignore vào `.gitignore` của project (`docs/raw/binary/*`, `docs/raw/superpowers/**`, `workspace*.json`).

Sau đó mở `docs/SCHEMA.md` → **Part 2: Project Domain Configuration**: điền *Domain Scope* và *Project-Specific Domain Tags* (vd `billing`, `api`). Mở `your-project/docs` làm vault Obsidian (tuỳ chọn). Xong, mọi thứ khác chạy sẵn.

## 6. Các skill

Chạy trong agent, tại gốc project hoặc gốc vault tương ứng.

| Skill | Làm gì | Ghi vào |
|---|---|---|
| `/kb-compile` | Biến source trong `raw/` (hoặc URL) thành note atomic | `wiki/`, `index.md`, `log.md` |
| `/kb-report <câu hỏi>` | Điều tra, viết report đầy đủ; kết luận tái dùng được đẩy ngược vào `wiki/concepts/` | `reports/` |
| `/kb-index` | Dựng lại catalog, glossary, concept map | `index.md` |
| `/kb-health` | Lint: link hỏng, orphan, note cũ, thiếu frontmatter, lệch code–doc | `wiki/TODO.md` |
| `/kb-colluni` *(chỉ vault trung tâm)* | Gom note universal từ vault của project | `raw/articles/` **duy nhất** |

Mọi thao tác compile/index/health/report/archive đều phải append `log.md` và cập nhật `index.md`.

## 7. Quy trình mẫu

### A. Trong một project
1. Clip tài liệu vào `docs/raw/articles/` (hoặc PDF/Office vào `docs/raw/binary/`).
2. `/kb-compile` → note vào `wiki/concepts|entities/universal` (pattern chung) hoặc `local` (riêng project).
3. Hỏi sâu: `/kb-report tại sao DAG employee load lại dòng không đổi?`
4. `/kb-index` → `/kb-health` → xem diff → **tự commit** (agent không tự commit).

### B. Đẩy tri thức chung về vault trung tâm
1. Trong `obsidian_llm_wiki`, chạy `/kb-colluni` và chỉ tới vault/project nguồn.
2. Skill đọc `index.md` của nguồn (mục *Universal Architecture Patterns* / *Universal Platforms & Infrastructure*; fallback: các thư mục `*/universal/`).
3. Agent **viết lại theo ngữ nghĩa**: tên riêng project → case study chung, bỏ path nội bộ, giữ nguyên công thức, diagram, bảng, pseudo-code.
4. Kết quả: `raw/articles/<slug-kebab-case>.md`, **không chứa `[[wikilink]]`** (tránh ghost backlink ở raw layer). Skill không đụng `wiki/` hay `index.md`.
5. Chạy `/kb-compile` để tổng hợp + cross-link vào wiki trung tâm.

### C. Bảo trì định kỳ
`/kb-index` sau thay đổi lớn, `/kb-health` thường xuyên, xử lý `wiki/TODO.md`.

## 8. Quy tắc viết note (`SCHEMA.md`)

```yaml
---
title: "Watermark Incremental Sync"
created: 2026-01-01
updated: 2026-01-01
type: concept            # concept|entity|comparison|query|report|architecture|guide
tags: [architecture, pipeline]   # chỉ lấy từ taxonomy
sources: [raw/articles/some-source.md]
confidence: high         # high|medium|low
contested: false
contradictions: []
status: published        # published|draft|deprecated
---
```

- Tên file lowercase, nối bằng `-` (theo schema); ≥ 2 `[[wikilink]]` ra ngoài cho mỗi concept/entity; mỗi lần sửa cập nhật `updated`.
- Tổng hợp ≥ 3 source → thêm provenance `^[raw/source.md]` vào đoạn chính.
- Chỉ tạo page khi chủ đề xuất hiện ở ≥ 2 source hoặc là trọng tâm của spec đã duyệt. Page > 200 dòng → tách.
- Thao tác đụng ≥ 10 page → agent phải tóm tắt và xin xác nhận trước.
- Mâu thuẫn: giữ cả hai phía kèm nguồn/ngày, `contested: true`, liệt kê `contradictions`, ghi log + TODO.
- Archive: chuyển vào `wiki/_archive/<subfolder>/`, xoá khỏi `index.md`, link đến ghi `[[slug]] (archived)`, ghi log.
- Scale: `index.md` mục > 50 entry thì chia nhỏ; > 200 page thêm `wiki/topic-map.md`; `log.md` > 500 entry thì rotate thành `log-YYYY.md`.

## 9. Guardrails

- **Không auto-commit.** Agent để thay đổi cho bạn review.
- **Secrets**: `.env*`, `mcp_config.json`, `.obsidian/plugins/*/data.json` — agent phải hỏi trước. Path trong `.agentignore` không bao giờ được đọc.
- **Git**: project → note được track; vault trung tâm → note local-only, chỉ track schema/cấu hình agent.
- Việc nhỏ dùng quy trình nhẹ; chỉ dùng brainstorming/plan khi tái cấu trúc lớn.

## 10. Xử lý sự cố

| Triệu chứng | Cách xử lý |
|---|---|
| Node ma/unresolved trong graph | Xoá `[[ ]]` khỏi `raw/`; chạy `/kb-health` |
| `/kb-colluni` không tìm thấy gì | Kiểm tra `index.md` nguồn có mục universal, hoặc có thư mục `*/universal/` |
| Không thấy skill `/kb-*` | Chắc chắn `.claude/skills/kb-*` có ở thư mục bạn mở Claude Code |
| `check_health.py` không chạy được | `chmod +x .claude/skills/kb-health/scripts/check_health.py` |
| MCP không dùng được | Bật Obsidian + Local REST API, đặt `OBSIDIAN_API_KEY`; hoặc sửa file trực tiếp |
| Agent không theo quy tắc | Đảm bảo `CLAUDE.md`/`AGENTS.md` ở gốc project/vault |
