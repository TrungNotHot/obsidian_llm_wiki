# Hướng Dẫn Sử Dụng: LLM Wiki

Kho tài liệu này gồm 2 phần độc lập theo triết lý LLM Wiki của Andrej Karpathy:
- **`llm_wiki_4pj`**: Mẫu wiki (Scaffold) nhúng trực tiếp vào dự án phần mềm để quản lý tài liệu kỹ thuật sát với code.
- **`obsidian_llm_wiki`**: Kho tri thức trung tâm (Central Vault) độc lập, chứa toàn bộ kiến thức chung của bạn.

> **Nguyên tắc cốt lõi**: Bạn mở **Obsidian** để xem liên kết và đọc ghi chú. **AI Agent** (trong terminal) làm nhiệm vụ biên soạn, liên kết và dọn dẹp các tệp Markdown.

---

## Phần 0: Yêu cầu cài đặt của mỗi Vault 
- **Obsidian Desktop App**: tải tại https://obsidian.md/download.
- **2 plugin** (có sẵn trong `obsidian_llm_wiki/.obsidian/plugins/`; sau khi mở vault, vào *Settings → Community plugins*, tắt Restricted mode và bật):
  - `dataview`: truy vấn/hiển thị ghi chú theo frontmatter.
  - `remotely-save`: đồng bộ vault lên cloud (Optional)
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

### 2. Bảng 5 Skill dùng trong dự án

Mở terminal tại thư mục gốc của dự án code và gọi các lệnh sau:

| Skill | Cú pháp | Khi nào dùng & Chức năng | Mức suy luận (Effort) | Đầu ra chính |
|---|---|---|---|---|
| **Biên dịch tài liệu** | `/kb-compile` | Khi vừa ném tài liệu/spec vào `docs/raw/` (hoặc đưa link URL). AI tự đọc, chia thành các note nhỏ có liên kết `[[...]]`.<br>• Riêng dự án: Lưu vào `local/` (nếu chỉ dùng cho dự án này).<br>• Dùng chung: Lưu vào `universal/` (nếu là pattern có thể tái sử dụng). | 🧠 **High** | `docs/wiki/`, `docs/index.md`, `docs/log.md` |
| **Báo cáo chuyên sâu** | `/kb-report <câu hỏi>` | Khi gặp bài toán phức tạp cần điều tra (ví dụ: lỗi luồng dữ liệu, phân tích phương án kiến trúc). AI tự phân tích trong repo và lưu báo cáo vĩnh viễn (không trả lời trôi trong chat). Nếu wiki thiếu dữ liệu, AI hỏi bạn trước khi tìm web (nguồn web ghi rõ URL, gắn nhãn chưa kiểm chứng). | 🧠 **High** | `docs/reports/<slug>.md` |
| **Hỏi đáp nhanh** | `/kb-ask <câu hỏi>` | Tra cứu nhanh kiến thức trong `docs/wiki/`, trả lời ngay trong chat (có trích dẫn `[[note]]`), không ghi file. Nếu wiki thiếu, AI **hỏi bạn trước** khi tìm web và gắn nhãn nguồn web là chưa kiểm chứng. | ⚡ **Low** | Trả lời trong chat |
| **Cập nhật mục lục** | `/kb-index` | Sau khi tạo nhiều note mới hoặc sửa đổi cấu trúc wiki. AI quét lại toàn bộ note và xây lại mục lục, bảng thuật ngữ. | ⚡ **Low** | `docs/index.md` |
| **Kiểm tra sức khỏe** | `/kb-health` | Chạy định kỳ để rà soát chất lượng wiki. AI tìm `[[link hỏng]]`, note mồ côi (không có ai trỏ đến), và tài liệu bị lệch (drift) so với code thực tế. | ⚡ **Low** | `docs/wiki/TODO.md` |

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
| **Thu thập từ dự án** | `/kb-colluni` | **(Chỉ có ở Kho trung tâm)** Khi các dự án code đã tích lũy nhiều pattern hay. AI hỏi đường dẫn dự án, quét thư mục `universal/`, tự động ẩn biến/đường dẫn nội bộ nhạy cảm và gom về kho trung tâm. | 🧠 **High** | `raw/articles/<slug>.md` |
| **Biên dịch kiến thức** | `/kb-compile` | Khi có bài viết/sách mới ném vào `raw/articles/` hoặc sau khi vừa chạy `/kb-colluni`. AI biến nội dung thô thành các note nguyên tử tại `concepts/` và `entities/`. | 🧠 **High** | `wiki/`, `index.md`, `log.md` |
| **Nghiên cứu chủ đề** | `/kb-report <chủ đề>` | Khi muốn nghiên cứu, so sánh công nghệ mới (ví dụ: so sánh Kafka vs RabbitMQ). AI tổng hợp sâu và lưu báo cáo dài hạn. Nếu wiki thiếu dữ liệu, AI hỏi bạn trước khi tìm web (nguồn web ghi rõ URL, gắn nhãn chưa kiểm chứng). | 🧠 **High** | `reports/<slug>.md` |
| **Hỏi đáp nhanh** | `/kb-ask <câu hỏi>` | Tra cứu nhanh kiến thức trong wiki, trả lời ngay trong chat (có trích dẫn `[[note]]`), không ghi file. Nếu wiki thiếu, AI **hỏi bạn trước** khi tìm web và gắn nhãn nguồn web là chưa kiểm chứng. | ⚡ **Low** | Trả lời trong chat |
| **Cập nhật mục lục** | `/kb-index` | Xây dựng lại toàn bộ cây danh mục kiến trúc, glossary thuật ngữ và topic map của toàn vault. | ⚡ **Low** | `index.md` |
| **Kiểm tra sức khỏe** | `/kb-health` | Quét toàn bộ kho trung tâm để phát hiện link gãy, note mồ côi, sai định dạng frontmatter. | ⚡ **Low** | `wiki/TODO.md` |


### 3. Tùy chỉnh skill (ví dụ: số hop tra cứu)

Skill chỉ là file Markdown (`.claude/skills/<tên>/SKILL.md`, bản sao ở `.agents/skills/`), nên bạn có thể **nhờ LLM sửa trực tiếp** để đổi hành vi, không cần code.

**Số hop** là số lần "nhảy" qua `[[wikilink]]` từ note tìm thấy đầu tiên khi tra cứu. Mặc định theo loại câu hỏi:

| Loại câu hỏi | `/kb-ask` | `/kb-report` |
|---|---|---|
| Tra cứu một sự kiện (fact lookup) | 1 hop | 1 hop |
| Quan hệ giữa các note, tóm tắt | 2 hops | 2 hops |
| Suy luận nhiều bước (multi-hop) | Không dùng (gợi ý chuyển `/kb-report`) | 3 hops |

Muốn đổi, ra lệnh cho LLM, ví dụ:
```text
Sửa skill kb-ask: cho phép tối đa 3 hop với câu hỏi multi-hop.
Sửa skill kb-report: fact lookup chỉ 1 hop, các loại khác tối đa 2 hop.
```
Nhớ yêu cầu sửa **cả hai bản** `.claude/skills/` và `.agents/skills/` để không lệch nhau. Hop càng cao càng tốn token và dễ đọc lan sang note ít liên quan.

**Các giá trị cấu hình khác có thể nhờ LLM đổi** (ghi rõ file cần sửa; nếu một giá trị xuất hiện ở nhiều file thì phải đổi đủ để không lệch):

| Cấu hình | Mặc định | Nằm ở đâu |
|---|---|---|
| Số note đọc đầy đủ tối đa (`/kb-ask`) | ~6 note | `kb-ask/SKILL.md` |
| Số note đọc đầy đủ tối đa (`/kb-report`) | ~12 note | `kb-report/SKILL.md` |
| Có/không cho tìm web, và hỏi trước khi tìm | Chỉ khi wiki thiếu, luôn hỏi trước | `kb-ask/SKILL.md`, `kb-report/SKILL.md`, `CLAUDE.md`/`AGENTS.md` (mục Web Search Policy) |
| Ngưỡng note "cũ" (stale) | > 90 ngày | `kb-health/SKILL.md` **và** `kb-health/scripts/check_health.py` |
| Ngưỡng tách note quá dài | > 300 dòng | `kb-compile/SKILL.md`, `kb-health/SKILL.md`, `kb-health/scripts/check_health.py`, `SCHEMA.md`, `CLAUDE.md`/`AGENTS.md` |
| Điều kiện tạo note mới | Khái niệm xuất hiện trong ≥ 2 nguồn | `kb-compile/SKILL.md`, `SCHEMA.md` |
| Số link ra tối thiểu mỗi note | 2 | `SCHEMA.md`, `CLAUDE.md` |
| Xoay vòng `log.md` | Khi quá 500 mục | `kb-health/SKILL.md`, `SCHEMA.md` |
| Ngưỡng chia mục trong `index.md` | > 50 mục / mục | `SCHEMA.md` |
| Tạo `topic-map.md` | Khi quá 200 trang | `SCHEMA.md` |
| Xác nhận trước khi sửa hàng loạt | ≥ 10 trang | `CLAUDE.md` / `AGENTS.md` |
| Số dòng cuối `log.md` đọc khi khởi động | 20 dòng (`kb-compile`: 20–30) | `kb-report/SKILL.md`, `kb-compile/SKILL.md` |

Ví dụ: `Sửa kb-health: đổi ngưỡng stale từ 90 ngày thành 180 ngày (cả SKILL.md và check_health.py).`

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
| **Yêu cầu suy luận cao** | `/kb-compile`<br>`/kb-report`<br>`/kb-colluni` | 🧠 **$\ge$ Sonnet 5.5 (medium)**<br>(Tối thiểu Sonnet 5.5 mức Medium, hoặc High) | Thiết lập trong chat / CLI:<br>`/model sonnet`<br>`/effort medium` hoặc `/effort high` |
| **Cấu trúc & Định dạng** | `/kb-index`<br>`/kb-health`<br>`/kb-ask` | ⚡ **$\le$ Sonnet 5.5 (low) hoặc Haiku**<br>(Dùng Haiku hoặc Sonnet 5.5 mức Low / tắt Thinking) | Thiết lập trong chat / CLI:<br>`/model haiku`<br>hoặc `/model sonnet` kèm `/effort low` |

---

### Chi tiết vì sao chọn cấu hình này:

1. **Tại sao cần $\ge$ Sonnet 5.5 (medium) cho Compile, Report, Colluni?**:
   - **`/kb-compile`**: Cần đọc hiểu đa tầng, bóc tách đúng bản chất khái niệm (atomic concept), kiểm tra xem có mâu thuẫn (contradiction) với các note cũ hay không.
   - **`/kb-report`**: Cần điều tra sâu xuyên suốt repo/codebase, liên kết nhiều giả thuyết logic để giải bài toán kỹ thuật phức tạp.
   - **`/kb-colluni`**: Đòi hỏi khả năng trừu tượng hóa cực tốt để biến code cụ thể của dự án thành bài học tổng quát, đồng thời nhận diện và làm sạch triệt để các dữ liệu nhạy cảm nội bộ.
   - *→ Mức suy luận từ Medium trở lên giúp model có đủ không gian "tư duy" để xử lý và liên kết dữ liệu phức tạp mà không bị ảo giác.*

2. **Tại sao chỉ cần $\le$ Sonnet 5.5 (low) hoặc Haiku cho Index, Health, Ask?**:
   - Đây là các tác vụ máy móc: chạy script kiểm tra định dạng (`check_health.py`), quét chuỗi regex tìm link `[[...]]` gãy, gom danh sách note mồ côi và sắp xếp lại cây mục lục theo mẫu có sẵn.
   - **`/kb-ask`**: Chỉ tra cứu và trích dẫn lại nội dung có sẵn trong wiki (theo từ khóa và link `[[...]]`), không cần suy luận sâu. Câu hỏi cần tổng hợp nhiều nguồn thì dùng `/kb-report`.
   - *→ Dùng Haiku hoặc Sonnet 5.5 ở mức Low giúp hoàn thành ngay trong vài giây, tiết kiệm tối đa chi phí token mà kết quả vẫn chính xác 100%.*

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
