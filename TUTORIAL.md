# Hướng Dẫn Sử Dụng: LLM Wiki

Kho tài liệu này gồm 2 phần độc lập theo triết lý LLM Wiki của Andrej Karpathy:
- **`llm_wiki_4pj`**: Mẫu wiki (Scaffold) nhúng trực tiếp vào dự án phần mềm để quản lý tài liệu kỹ thuật sát với code.
- **`obsidian_llm_wiki`**: Kho tri thức trung tâm (Central Vault) độc lập, chứa toàn bộ kiến thức chung của bạn.

Mỗi vault có hai cây công cụ cùng nội dung: `.claude/` (cho Claude Code) và `.agents/` (cho Gemini/Antigravity), gồm `skills/`, `scripts/` và `references/`. `.claude/` là bản gốc, `.agents/` được sinh bằng `sync_agents.py` (xem Phần 6).

> **Nguyên tắc cốt lõi**: Bạn mở **Obsidian** để xem liên kết và đọc ghi chú. **AI Agent** (trong terminal) làm nhiệm vụ biên soạn, liên kết và dọn dẹp các tệp Markdown.

---

## Phần 0: Yêu cầu cài đặt của mỗi Vault 
- **Obsidian Desktop App**: tải tại https://obsidian.md/download.
- **2 plugin** (có sẵn trong `obsidian_llm_wiki/.obsidian/plugins/`; sau khi mở vault, vào *Settings → Community plugins*, tắt Restricted mode và bật):
  - `dataview`: truy vấn/hiển thị ghi chú theo frontmatter.
  - `remotely-save`: đồng bộ vault lên cloud (Optional)
- **`uv`** (Python): `/kb-compile` dùng khi chuyển file binary (`.pdf`, `.docx`...) sang Markdown (thư viện `markitdown`). Các skill `/kb-ask`, `/kb-report`, `/kb-health` chỉ cần `python3`.
- **Trình duyệt**: cài extension [Obsidian Web Clipper](https://obsidian.md/clipper) để biến bài viết web thành .md vào `raw/articles/`.

---

## Phần 1: Dùng `llm_wiki_4pj` (Wiki trong dự án code)

Dùng khi bạn muốn AI ghi chép tài liệu kiến trúc, API và quyết định thiết kế ngay bên cạnh mã nguồn của dự án.

### 1. Cài đặt vào dự án (chỉ làm 1 lần)
Từ thư mục gốc của repository này:

```bash
cd llm_wiki_4pj
./setup.sh /duong-dan/toi/du-an-cua-ban
cp -n CLAUDE.md /duong-dan/toi/du-an-cua-ban/   # Nếu dùng Claude Code
```

Mở `<du-an>/docs/SCHEMA.md`, tìm **Part 2: Project Domain Configuration** để điền mô tả ngắn và một vài tag nghiệp vụ của dự án (ví dụ: `billing`, `api`, `auth`).

### Cập nhật skill cho dự án đã cài
`setup.sh` dùng `cp -rn` (không ghi đè), nên chạy lại sẽ không cập nhật skill đã có. Để lấy phiên bản skill mới nhất từ `llm_wiki_4pj`, chép đè các thư mục công cụ (không chép `docs/`, vì `docs/SCHEMA.md` chứa cấu hình riêng của dự án):
```bash
cp -r llm_wiki_4pj/.claude/{skills,scripts,references} /duong-dan/toi/du-an-cua-ban/.claude/
cp -r llm_wiki_4pj/.agents/{skills,scripts,references} /duong-dan/toi/du-an-cua-ban/.agents/
```
Sau đó so `docs/SCHEMA.md` của dự án với bản mẫu để áp dụng các quy tắc mới (ví dụ định nghĩa `sha256`), vì skill trỏ về `SCHEMA.md` cho các quy tắc đó.

### 2. Bảng 5 Skill dùng trong dự án

Mở terminal tại thư mục gốc của dự án code và gọi các lệnh sau:

| Skill | Cú pháp | Khi nào dùng & Chức năng | Mức suy luận (Effort) | Đầu ra chính |
|---|---|---|---|---|
| **Biên dịch tài liệu** | `/kb-compile` | Khi vừa ném tài liệu/spec vào `docs/raw/` (hoặc đưa link URL). AI tự đọc, chia thành các note nhỏ có liên kết `[[...]]`. AI chọn note liên quan từ `docs/index.md` và grep tên khái niệm trước khi tạo trang mới, để cập nhật thay vì tạo trùng; khi chạy tương tác, nó nêu 3-5 điểm chính và danh sách trang sẽ tạo/cập nhật trước khi ghi.<br>• Riêng dự án: Lưu vào `local/` (nếu chỉ dùng cho dự án này).<br>• Dùng chung: Lưu vào `universal/` (nếu là pattern có thể tái sử dụng). | 🧠 **High** | `docs/wiki/`, `docs/index.md`, `docs/log.md` |
| **Báo cáo chuyên sâu** | `/kb-report <câu hỏi>` | Khi gặp bài toán phức tạp cần điều tra (ví dụ: lỗi luồng dữ liệu, phân tích phương án kiến trúc). AI tự phân tích trong repo và lưu báo cáo vĩnh viễn (không trả lời trôi trong chat). Khi wiki mô tả hành vi đã cài đặt trong code, AI đối chiếu với code thật và ghi các chỗ tài liệu lệch code vào một mục riêng; nếu đã có báo cáo cùng câu hỏi thì cập nhật báo cáo cũ. Nếu wiki thiếu dữ liệu, AI hỏi bạn trước khi tìm web (nguồn web ghi rõ URL, gắn nhãn chưa kiểm chứng). | 🧠 **High** | `docs/reports/<slug>.md` |
| **Kiểm tra sức khỏe** | `/kb-health` | Chạy định kỳ để rà soát chất lượng wiki. Script tìm `[[link hỏng]]`, note mồ côi, note thiếu trong index, sai frontmatter/tag và nguồn `raw/` bị sửa (source drift). Sau đó AI rà mâu thuẫn giữa các note (mặc định chỉ xét note mới đổi từ lần health trước), đối chiếu tài liệu với code, và gợi ý khái niệm chưa có trang. | 🧠 **High** | `docs/wiki/TODO.md` |
| **Hỏi đáp nhanh** | `/kb-ask <câu hỏi>` | Tra cứu nhanh kiến thức trong `docs/wiki/`, trả lời ngay trong chat (có trích dẫn `[[note]]`), không ghi file. Nếu wiki thiếu, AI **hỏi bạn trước** khi tìm web và gắn nhãn nguồn web là chưa kiểm chứng. | ⚖️ **Medium** | Trả lời trong chat |
| **Cập nhật mục lục** | `/kb-index` | Sau khi tạo nhiều note mới hoặc sửa đổi cấu trúc wiki. AI chỉ cập nhật mục lục cho note mới hoặc thay đổi (rebuild toàn bộ khi bạn yêu cầu), và hỏi bạn trước nếu có mục bị xóa hoặc từ 10 mục thay đổi. | ⚡ **Low** | `docs/index.md` |


### 3. Khi code thay đổi nhưng không có tài liệu trong `docs/raw/`

`/kb-compile` chỉ biến **nguồn đưa vào** (`docs/raw/` hoặc URL) thành note wiki. Nếu dev thêm code hoặc logic mới mà không ai viết spec vào `docs/raw/`, `/kb-compile` không có đầu vào nên sẽ không tạo note tương ứng. Có 3 cách bù:

1. **Phát hiện: `/kb-health`**: bước Agent Sweep so sánh các thành phần code đang có (ví dụ `dags/`, `src/`, `lib/`) với `docs/wiki/entities/`. Thành phần nào chưa có entity tương ứng sẽ được ghi vào `docs/wiki/TODO.md` ở mức 🔴 High (Critical Code Drift). Lưu ý: nó chỉ đối chiếu với trang **entity**, không kiểm tra các trang hướng dẫn trong `easy_read/`.
2. **Dịch ngược từ code: `/kb-report`**: AI đọc trực tiếp mã nguồn, SQL, test và ghi báo cáo vào `docs/reports/`, ví dụ:
   ```text
   /kb-report giải thích logic transform và watermark của module X
   ```
   Nếu report làm rõ một khái niệm/quy tắc tái sử dụng được, AI trích thành note nguyên tử trong `docs/wiki/concepts/` hoặc `entities/` (chỉ khi có khái niệm như vậy, không phải lần nào cũng có).
3. **Ra lệnh trực tiếp**: với thay đổi nhỏ, chỉ cần nói "Vừa thêm DAG X trong code, cập nhật wiki tương ứng". AI đọc code và sửa trang liên quan, đây là yêu cầu thường chứ không phải skill riêng, nên hãy dặn thêm cập nhật `docs/index.md` và `docs/log.md` rồi chạy `/kb-health` để kiểm tra link.

Với tính năng lớn, cách bài bản hơn là thả spec/thiết kế vào `docs/raw/superpowers/specs/` rồi chạy `/kb-compile`: wiki vừa có ngữ cảnh thiết kế (vì sao làm vậy), vừa được đối chiếu với code.

---

## Phần 2: Dùng `obsidian_llm_wiki` (Kho tri thức trung tâm)

Dùng làm kho bách khoa toàn thư cá nhân/công ty, độc lập hoàn toàn với mã nguồn của bất kỳ dự án nào.

### 1. Khởi động (chỉ làm 1 lần)
1. Trong Obsidian, chọn **Open folder as vault** và chọn:
   ```text
   <repository-root>/obsidian_llm_wiki/
   ```
2. Khởi tạo các file cấu hình mẫu (nếu chưa có):
   ```bash
   cd obsidian_llm_wiki
   test -e index.md || cp index.example.md index.md
   test -e log.md || cp log.example.md log.md
   test -e wiki/TODO.md || cp wiki/TODO.example.md wiki/TODO.md
   ```
3. Mở terminal ngay tại `obsidian_llm_wiki/` để gọi AI agent.

### 2. Bảng 6 Skill dùng trong Kho trung tâm

Mở terminal tại thư mục `obsidian_llm_wiki/` và gọi các lệnh sau:

| Skill | Cú pháp | Khi nào dùng & Chức năng | Mức suy luận (Effort) | Đầu ra chính |
|---|---|---|---|---|
| **Biên dịch kiến thức** | `/kb-compile` | Khi có bài viết/sách mới ném vào `raw/articles/` hoặc sau khi vừa chạy `/kb-colluni`. AI biến nội dung thô thành các note nguyên tử tại `concepts/` và `entities/`. Trước khi ghi, AI chọn note liên quan từ `index.md` và grep tên khái niệm trước khi tạo trang mới (để cập nhật thay vì tạo trùng và phát hiện mâu thuẫn), nêu 3-5 điểm chính cùng danh sách trang sẽ tạo/cập nhật; nếu ảnh hưởng ≥ 10 trang sẽ hỏi bạn trước. | 🧠 **High** | `wiki/`, `index.md`, `log.md` |
| **Nghiên cứu chủ đề** | `/kb-report <chủ đề>` | Khi muốn nghiên cứu, so sánh công nghệ mới (ví dụ: so sánh Kafka vs RabbitMQ). AI tổng hợp sâu và lưu báo cáo dài hạn; nếu đã có báo cáo cùng câu hỏi thì cập nhật báo cáo cũ. Nếu wiki thiếu dữ liệu, AI hỏi bạn trước khi tìm web (nguồn web ghi rõ URL, gắn nhãn chưa kiểm chứng). | 🧠 **High** | `reports/<slug>.md` |
| **Kiểm tra sức khỏe** | `/kb-health` | Script quét toàn kho để phát hiện link gãy, note mồ côi, note thiếu trong index, sai frontmatter/tag và nguồn `raw/` bị sửa; AI rà mâu thuẫn giữa các note (mặc định chỉ note mới đổi từ lần health trước) và gợi ý khái niệm chưa có trang. | 🧠 **High** | `wiki/TODO.md` |
| **Thu thập từ dự án** | `/kb-colluni` | **(Chỉ có ở Kho trung tâm)** Khi các dự án code đã tích lũy nhiều pattern hay. AI hỏi đường dẫn dự án, quét thư mục `universal/`, liệt kê ứng viên và **chờ bạn xác nhận**, rồi gỡ link nội bộ và thay tên máy chủ, URL nội bộ, thông tin xác thực, tên người, mã định danh riêng bằng mô tả chung. Không ghi đè bài đã gom: nếu nội dung khác thì hỏi bạn. | ⚖️ **Medium** | `raw/articles/<slug>.md` |
| **Hỏi đáp nhanh** | `/kb-ask <câu hỏi>` | Tra cứu nhanh kiến thức trong wiki, trả lời ngay trong chat (có trích dẫn `[[note]]`), không ghi file. Nếu wiki thiếu, AI **hỏi bạn trước** khi tìm web và gắn nhãn nguồn web là chưa kiểm chứng. | ⚖️ **Medium** | Trả lời trong chat |
| **Cập nhật mục lục** | `/kb-index` | Cập nhật mục lục cho note mới hoặc thay đổi (rebuild toàn bộ khi bạn yêu cầu); tách mục dài và dựng topic map khi vault lớn theo `SCHEMA.md`. | ⚡ **Low** | `index.md` |

---

## Phần 3: Cách 2 repo tương tác và trao đổi tri thức

Hai phần này không nằm riêng rẽ mà tạo thành một vòng lặp tích lũy kiến thức:

```text
[Dự án A (llm_wiki_4pj)]              [Dự án B (llm_wiki_4pj)]
docs/wiki/.../universal/             docs/wiki/.../universal/
           │                                    │
           └───────────── /kb-colluni ──────────┘
                                │ (Gom kiến thức chung, làm sạch thông tin nội bộ)
                                ▼
                   [Kho trung tâm: obsidian_llm_wiki]
                       raw/articles/<slug>.md
                                │
                                │ /kb-compile
                                ▼
                       wiki/concepts|entities/
```

### Quy trình 2 bước đưa kiến thức từ dự án về kho trung tâm:

1. **Bước 1 - Gom bài (`/kb-colluni`)**:
   - Đứng tại terminal của `obsidian_llm_wiki`, gõ:
     ```text
     /kb-colluni
     ```
   - Nhập đường dẫn tới dự án code (ví dụ: `/home/tdtr/workspace/my-backend-project`).
   - AI liệt kê các note ứng viên và **dừng chờ bạn xác nhận** gom note nào.
   - AI tự động lọc các note trong `universal/`, lược bỏ tên biến và đường dẫn nhạy cảm của dự án, rồi lưu bản nháp thô vào `obsidian_llm_wiki/raw/articles/`.

2. **Bước 2 - Nạp vào cây tri thức (`/kb-compile`)**:
   - Vẫn tại `obsidian_llm_wiki`, gõ tiếp:
     ```text
     /kb-compile
     ```
   - AI đọc bài thô vừa thu thập, gắn liên kết chéo `[[...]]` vào hệ thống kiến thức chung và cập nhật `index.md`.

---

## Phần 4: Lựa chọn Model & Mức suy luận (Reasoning Effort)

Không phải tác vụ nào cũng cần model đắt tiền hoặc bật thinking cao. Tối ưu hiệu quả và chi phí như sau:

### 💡 Bảng cấu hình trực quan (Ví dụ Sonnet 5.5 vs Haiku)

| Nhóm tác vụ | Skill | Model & Mức Effort khuyến nghị | Cách thiết lập thực tế |
|---|---|---|---|
| **Suy luận cao** | `/kb-compile`<br>`/kb-report`<br>`/kb-health` | 🧠 **Sonnet 5.5 (high)**<br>(Mức High) | Thiết lập trong chat / CLI:<br>`/model sonnet`<br>`/effort high` |
| **Suy luận trung bình** | `/kb-colluni`<br>`/kb-ask` | ⚖️ **Sonnet 5.5 (medium)**<br>(Mức Medium) | Thiết lập trong chat / CLI:<br>`/model sonnet`<br>`/effort medium` |
| **Cấu trúc & Định dạng** | `/kb-index` | ⚡ **$\le$ Sonnet 5.5 (low) hoặc Haiku**<br>(Dùng Haiku hoặc Sonnet 5.5 mức Low / tắt Thinking) | Thiết lập trong chat / CLI:<br>`/model haiku`<br>hoặc `/model sonnet` kèm `/effort low` |

> Bảng trên dùng tên lệnh của Claude Code. Với Gemini/Antigravity (`.agents/`), chọn model và mức suy luận tương đương.

---

### Chi tiết vì sao chọn cấu hình này:

1. **Tại sao dùng Sonnet 5.5 (high) cho Compile, Report, Health?**:
   - **`/kb-compile`**: Cần đọc hiểu đa tầng, bóc tách đúng bản chất khái niệm (atomic concept), kiểm tra xem có mâu thuẫn (contradiction) với các note cũ hay không.
   - **`/kb-report`**: Cần điều tra sâu xuyên suốt repo/codebase, liên kết nhiều giả thuyết logic để giải bài toán kỹ thuật phức tạp.
   - **`/kb-health`**: Script lo các lỗi máy móc (link gãy, note mồ côi, index, frontmatter/tag, source drift, note cũ). Phần "Agent Sweep" mới cần suy luận: tìm mâu thuẫn giữa các note và đối chiếu tài liệu với code (drift). Đây là việc cần đọc hiểu ngữ nghĩa nên không thể dùng mức Low.
   - *→ Mức High giúp model có đủ không gian "tư duy" để xử lý và liên kết dữ liệu phức tạp mà không bị ảo giác.*

2. **Tại sao dùng Sonnet 5.5 (medium) cho Colluni, Ask?**:
   - **`/kb-colluni`**: Cần trừu tượng hóa code cụ thể của dự án thành bài học tổng quát và làm sạch dữ liệu nhạy cảm nội bộ, nhưng phạm vi mỗi lần chạy hẹp và có quy trình rõ ràng nên Medium là đủ.
   - **`/kb-ask`**: Dù chỉ trả lời nhanh, AI vẫn phải chọn đúng note từ index, trích dẫn đúng nguồn và nhận ra khi wiki chưa đủ thông tin (để hỏi bạn trước khi tìm web). Câu hỏi cần tổng hợp nhiều nguồn thì dùng `/kb-report`.

3. **Tại sao chỉ cần $\le$ Sonnet 5.5 (low) hoặc Haiku cho Index?**:
   - **`/kb-index`**: Tác vụ gần như máy móc: lấy danh sách note mới hoặc thay đổi (từ script) rồi cập nhật mục lục, glossary theo mẫu có sẵn.
   - *→ Dùng Haiku hoặc Sonnet 5.5 ở mức Low giúp hoàn thành ngay trong vài giây, tiết kiệm tối đa chi phí token mà kết quả vẫn đủ tốt cho tác vụ theo khuôn mẫu.*

---

## Phần 5: Tùy chỉnh skill (số hop, ngưỡng, giới hạn)

Skill chỉ là file Markdown (`.claude/skills/<tên>/SKILL.md` là bản gốc, `.agents/skills/` được sinh từ đó), còn script dùng chung nằm ở `.claude/scripts/` (bản chép ở `.agents/scripts/`), nên bạn có thể **nhờ LLM sửa trực tiếp** để đổi hành vi, không cần code.

**Luồng tra cứu của `/kb-ask` và `/kb-report`** gọn, theo thứ tự:
1. **Tìm note liên quan**: AI đọc `index.md` (file lớn thì đọc phần liên quan hoặc grep), tự phân tích câu hỏi và chọn các mục phù hợp nhất bằng phán đoán. Chỉ đọc README thư mục khi index chưa phủ chủ đề. Nếu catalog không có mục khớp, hoặc trước khi kết luận wiki thiếu, AI grep từ khóa (kèm từ đồng nghĩa) trên `wiki/` và `reports/`.
2. **Đọc**: AI đọc đầy đủ các note liên quan nhất rồi dừng khi đã đủ trả lời (`/kb-ask` thường 3-8 note, nếu cần hơn khoảng 12 thì gợi ý chuyển `/kb-report`; `/kb-report` thường 8-15 note). Chỉ theo `[[wikilink]]` khi nó dẫn tới thứ câu trả lời cần. Mở `contradictions:` và `sources:` (`raw/`) khi cần.
3. **Tùy chọn, mở rộng theo link**: khi câu hỏi về quan hệ giữa các note, hoặc catalog không phủ chủ đề, AI chạy `outline.py` để xem hàng xóm (link và backlink) của các note đã đọc, gồm `title`, `tags`, `confidence` và toàn bộ heading; AI tự chọn note đáng đọc, script không chấm điểm.
4. **Chỉ `/kb-report`: đối chiếu code** khi wiki mô tả hành vi đã được cài đặt (DAG, SQL, config), ghi các chỗ tài liệu lệch code vào một mục riêng của báo cáo.

Chất lượng phụ thuộc nhiều vào bước 1, nên `index.md` cần mô tả rõ ràng từng mục (chạy `/kb-index` khi wiki thay đổi).

**Số hop** (chỉ áp dụng ở bước 3) là số lần "nhảy" qua `[[wikilink]]` từ các note đã đọc. Mặc định 1 hop; 2 hop cho quan hệ hoặc tóm tắt; 3 hop (chỉ `/kb-report`) cho chuỗi suy luận qua từ 3 note. Hop càng cao càng tốn token và dễ đọc lan sang note ít liên quan.

Muốn đổi, ra lệnh cho LLM, ví dụ:
```text
Sửa skill kb-report: luôn dùng outline.py với 2 hop.
Sửa skill kb-ask: không dùng outline.py, chỉ đọc index và grep.
```
Hãy sửa trong `.claude/`, rồi chạy `python3 sync_agents.py` để `.agents/` khớp lại (xem Phần 6).

**Các giá trị cấu hình khác có thể nhờ LLM đổi** (ghi rõ file cần sửa; nếu một giá trị xuất hiện ở nhiều file thì phải đổi đủ để không lệch):

| Cấu hình | Mặc định | Nằm ở đâu |
|---|---|---|
| Số note đọc đầy đủ (mức tham khảo, không phải hạn mức cứng) | `/kb-ask` 3-8 note (trên khoảng 12 thì chuyển `/kb-report`); `/kb-report` 8-15 note | `kb-ask/SKILL.md`, `kb-report/SKILL.md` |
| Số ứng viên `outline.py` in ra tối đa (`--limit`) | Mặc định theo hop: 20 / 40 / 60 cho 1 / 2 / 3 hop; khi bị cắt thì thu hẹp `--seeds` hoặc nâng `--limit` (tối đa 100, hằng `MAX_LIMIT`) | hàm `default_limit()` và hằng `MAX_LIMIT` trong `.claude/scripts/outline.py` và `.agents/scripts/outline.py` |
| Khi nào grep (kèm từ đồng nghĩa) toàn bộ `wiki/` và `reports/` | Khi catalog không có mục khớp, hoặc trước khi kết luận wiki thiếu | `kb-ask/SKILL.md`, `kb-report/SKILL.md` |
| Có/không cho tìm web, và hỏi trước khi tìm | Chỉ khi wiki thiếu, luôn hỏi trước | `kb-ask/SKILL.md`, `kb-report/SKILL.md`, `CLAUDE.md`/`AGENTS.md` (mục Web Search Policy) |
| Ngưỡng note "cũ" (stale): "Outdated vs cited source" (trang cũ hơn nguồn nó trích dẫn > 90 ngày) và "Aging candidates" (> 90 ngày kể từ lần cập nhật, chỉ coi là cũ nếu có nguồn mới hơn cùng chủ đề) | > 90 ngày | `kb-health/SKILL.md` **và** `.claude/scripts/check_health.py` và `.agents/scripts/check_health.py` |
| Ngưỡng tách note quá dài | > 300 dòng | Nguồn chính là `SCHEMA.md` (các skill, `CLAUDE.md` và `AGENTS.md` chỉ trỏ về đó); riêng `.claude/scripts/check_health.py` và `.agents/scripts/check_health.py` có hằng số riêng nên phải đổi cùng |
| Quy tắc `confidence`: không đặt `high` nếu chưa có từ 2 nguồn | 2 nguồn | `SCHEMA.md`, `kb-compile/SKILL.md`, `kb-report/SKILL.md`, `check_health.py` (mục "confidence: high with fewer than 2 sources") |
| Điều kiện tạo note mới | Khái niệm xuất hiện trong ≥ 2 nguồn | `kb-compile/SKILL.md`, `SCHEMA.md` |
| Số link ra tối thiểu mỗi note | 2 | `SCHEMA.md`, `CLAUDE.md` |
| Xoay vòng `log.md` | Khi quá 500 mục | `kb-health/SKILL.md`, `SCHEMA.md` |
| Ngưỡng chia mục trong `index.md` | > 50 mục / mục | `SCHEMA.md` |
| Tạo `topic-map.md` | Khi quá 200 trang | `SCHEMA.md` |
| Xác nhận trước khi sửa hàng loạt | ≥ 10 trang | `SCHEMA.md`, `CLAUDE.md`/`AGENTS.md`, `kb-compile/SKILL.md`, `kb-index/SKILL.md`, `kb-colluni/SKILL.md` |
| Số mục cuối `log.md` đọc khi khởi động | 5 mục gần nhất | `kb-report/SKILL.md`, `kb-compile/SKILL.md` |
| Phạm vi rà mâu thuẫn của `/kb-health` | Theo gia tăng (chỉ note mới đổi từ lần health trước); rà toàn bộ khi bạn yêu cầu | `kb-health/SKILL.md` |
| `/kb-index` cập nhật | Gia tăng mặc định; rebuild toàn bộ khi bạn yêu cầu; hỏi nếu có mục bị xóa hoặc từ 10 mục thay đổi | `kb-index/SKILL.md` |
| Định nghĩa `sha256` của `raw/` | Văn bản: hash phần thân (sau frontmatter, đã strip); nhị phân: hash file gốc | `SCHEMA.md`, `kb-compile/SKILL.md`, `kb-colluni/SKILL.md`, `check_health.py` |

Ví dụ: `Sửa kb-health: đổi ngưỡng stale từ 90 ngày thành 180 ngày (cả SKILL.md và check_health.py).`

---

## 📌 Quy tắc vàng & Phân chia vai trò (User vs AI)

### 1. Dữ liệu mới đặt ở đâu trong `raw/`?
Thư mục `raw/` là **nguồn sự thật bất biến (Immutable Source)**. File nào đặt vào đâu:

| Loại tệp / Nội dung | Thư mục lưu trữ | Ghi chú & Ví dụ |
|---|---|---|
| **Bài viết, Web clips, Markdown** | `raw/articles/` | Lưu bài đọc từ web, tài liệu kỹ thuật dạng text hoặc file `.md`. |
| **Tài liệu gốc Binary** | `raw/binary/` | File gốc `.pdf`, `.docx`, `.pptx`, `.xlsx`, ảnh chụp tài liệu (AI sẽ tự chuyển thành markdown). |
| **Ảnh, Sơ đồ đính kèm** | `raw/assets/` | File ảnh, screenshot kiến trúc được các note trong wiki nhúng vào. |
| **Bản đặc tả kỹ thuật (Spec)** | `raw/superpowers/specs/` | Các tài liệu Technical Design Specification, kiến trúc hệ thống trước khi code. |
| **Kế hoạch triển khai (Plan)** | `raw/superpowers/plans/` | Các bản kế hoạch thực thi theo từng giai đoạn (Phased Implementation Plans). |

---

### 2. User có phải chỉ cần quan tâm `raw/` không?
**Đúng, về mặt nạp dữ liệu!** Vai trò của User rất đơn giản:
- **Đầu vào (Input)**: Bạn chỉ cần quan tâm đưa file vào đúng chỗ trong `raw/` (hoặc gửi URL), sau đó gõ lệnh `/kb-*`.
- **Đầu ra (Output)**: Bạn mở **Obsidian** để xem đồ thị liên kết, tra cứu ghi chú ở `wiki/`, đọc báo cáo ở `reports/` và theo dõi danh sách việc ở `wiki/TODO.md`.
- **Tuyệt đối không cần làm thủ công**: Bạn không cần tự tạo note con, không cần tự nối link `[[...]]`, và không cần tự sửa `index.md` hay `log.md`.
- **Kiểm soát mã nguồn**: AI không tự commit Git. Sau mỗi phiên làm việc, bạn dùng `git status` và `git diff` để kiểm tra rồi commit bằng tay.

---

### 3. AI chỉ tương tác với những phần nào?
- **AI ĐỌC từ đâu?**:
  - Đọc tài liệu gốc trong `raw/`.
  - Đọc source code dự án (với `llm_wiki_4pj`) để đối chiếu và phát hiện độ lệch (code-doc drift).
  - Đọc `SCHEMA.md` để tuân thủ quy tắc tag, format và ngưỡng chia tách file.
  - Tìm trên web (`/kb-ask`, `/kb-report`) **chỉ khi wiki thiếu thông tin và sau khi hỏi bạn**; nguồn web luôn ghi rõ URL và gắn nhãn chưa kiểm chứng. Muốn giữ lâu dài thì clip vào `raw/articles/` rồi `/kb-compile`.
- **AI VIẾT & DUY TRÌ ở đâu?**:
  - `wiki/` (`concepts/`, `entities/`, `easy_read/`, `_archive/`): AI tự tạo, liên kết chéo `[[...]]`, cập nhật và lưu trữ.
  - `index.md`: AI tự động thêm/bớt mục lục và bảng thuật ngữ.
  - `log.md`: AI tự động ghi nhật ký append-only mọi hành động (compile, report, health check).
  - `reports/`: AI xuất các bài nghiên cứu/phân tích sâu dài hạn.
  - `wiki/TODO.md`: AI ghi danh sách link gãy, note mồ côi để theo dõi xử lý.
- ⛔ **Quy tắc bất biến đối với AI**: AI **KHÔNG BAO GIỜ chỉnh sửa nội dung trong `raw/`** sau khi đã lưu, nhằm đảm bảo nguồn gốc dữ liệu luôn nguyên bản.

---

## Phần 6: Đối chiếu với thiết kế gốc, đồng bộ và lưu ý git

**Ánh xạ với LLM Wiki gốc** (Karpathy, Hermes):

| Thao tác gốc | Skill ở đây | Ghi chú |
|---|---|---|
| Ingest: thu nguồn vào `raw/` | `/kb-compile` (nguồn cục bộ, URL, file nhị phân) và `/kb-colluni` (nguồn lấy từ vault dự án khác, chỉ ghi `raw/articles/`) | `/kb-colluni` là bước thu nguồn xuyên vault, sau đó chạy `/kb-compile` để biên dịch vào `wiki/` |
| Ingest: biên dịch thành trang wiki | `/kb-compile` | Hiển thị điểm chính và danh sách trang trước khi ghi (khi chạy tương tác) |
| Query | `/kb-ask` (chỉ đọc, trả lời trong chat) và `/kb-report` (lưu thành báo cáo, rút khái niệm tái sử dụng về wiki) | Hai biến thể của một thao tác: khác nhau ở chỗ có lưu file hay không |
| Lint | `/kb-health` | Có thêm đối chiếu tài liệu với code và mục gợi ý (khái niệm chưa có trang) |
| Index và log | `/kb-index` | Quy tắc quy mô (tách mục 50, bản đồ chủ đề 200, xoay log 500) nằm ở `SCHEMA.md` |

**Đồng bộ `.claude/` và `.agents/`**: `.claude/` là bản gốc, `.agents/` (cho Gemini/Antigravity) được sinh ra từ đó, áp dụng cho cả `obsidian_llm_wiki` và `llm_wiki_4pj`. Sau khi sửa skill, script hoặc references trong `.claude/`, chạy ở thư mục gốc:
```bash
python3 sync_agents.py --check   # chỉ báo chỗ lệch
python3 sync_agents.py           # ghi .agents/
```
Script đổi tiền tố đường dẫn `.claude/` thành `.agents/` và công cụ lấy URL của `/kb-compile` (`WebFetch` thành `read_url_content`); script Python được chép nguyên. `CLAUDE.md` và `AGENTS.md` không bị đồng bộ vì có nội dung riêng cho từng công cụ. Dự án đã cài từ `llm_wiki_4pj` thì cập nhật theo mục "Cập nhật skill cho dự án đã cài" ở Phần 1.

**Git, nhánh private và worktree**: ở nhánh `main`, nội dung wiki (`wiki/*/*`, `reports/*`, `index.md`, `log.md`, `raw/articles/*`) nằm trong `.gitignore` nên **không có lịch sử**; nếu một skill ghi hỏng thì git không khôi phục được. Để có lịch sử mà vẫn riêng tư, dùng nhánh `private/vault-history`:
- Nhánh này bỏ các ignore của nội dung, nên note, báo cáo, index và log được commit và có lịch sử. `raw/binary/`, `raw/assets/`, khóa và cấu hình plugin Obsidian, `.env*` vẫn bị ignore.
- **Không bao giờ đẩy nhánh này lên remote.** Hook `pre-push` cục bộ từ chối mọi nhánh `private/*`, nhưng hook chỉ nằm trong máy bạn (không theo repo khi clone).
- **Không `git switch` giữa hai nhánh trong cùng một thư mục**: các file nội dung chỉ được theo dõi ở nhánh private, nên chuyển sang `main` sẽ gỡ chúng khỏi ổ đĩa (dữ liệu vẫn còn trong commit, quay lại nhánh private sẽ khôi phục). Hãy dùng hai thư mục (git worktree):

| Thư mục | Nhánh | Dùng cho |
|---|---|---|
| Thư mục chính của repo | `private/vault-history` | Mở vault trong Obsidian, chạy `/kb-*` trên nội dung, commit lịch sử nội dung |
| Worktree (ví dụ `../obsidian-main`, tạo bằng `git worktree add ../obsidian-main main`) | `main` | Sửa thiết kế chung (skill, script, `SCHEMA.md`, `CLAUDE.md`, `AGENTS.md`, `TUTORIAL.md`) rồi đẩy lên remote |

- Sửa thiết kế ở worktree `main`: chạy `python3 sync_agents.py --check`, commit, `git push origin main`; sau đó ở thư mục chính chạy `git merge main` (nếu xung đột ở `.gitignore` thì giữ bản của nhánh private).
- Nếu lỡ sửa file thiết kế ở nhánh private, commit ở đó rồi đưa riêng các file thiết kế sang `main` bằng `git checkout private/vault-history -- <file>` trong worktree (không lấy nội dung vault và `.gitignore`).
- Commit riêng thay đổi `.gitignore` của nhánh private trước, rồi mới commit nội dung.
