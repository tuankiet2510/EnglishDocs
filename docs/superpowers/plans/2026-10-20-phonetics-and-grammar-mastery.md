# Chuyên Đề 1 & 2: Hệ Thống Hóa Ngữ Âm & Ngữ Pháp Trọng Tâm Ôn Thi Vào 10 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khắc phục triệt để các lỗi nội dung copy-paste, loại bỏ rác SEO, và nâng cấp toàn diện hệ thống Ngữ âm (Phonetics) & Ngữ pháp (Grammar - Sentence Transformation) trên Notion `EnglishDocs` theo chuẩn sư phạm ELT và ma trận đề thi vào 10 (Sở GD Quảng Ngãi 36/45 câu).

**Architecture:** Áp dụng mô hình Sư phạm 5 tầng (Bản chất -> Mẹo thần chú Mnemonic -> Bẫy Vietlish -> Bảng đối chiếu -> Đề thi thực chiến 10). Tận dụng Notion Color Callouts (Blue/Green/Yellow/Red/Purple), bảng biểu và sơ đồ trực quan. Xuất bản HTML offline tự động bằng script `notion_html_exporter.py` không tốn LLM token.

**Tech Stack:** Notion MCP (`@suekou/mcp-notion-server`), Python 3 (`notion_html_exporter.py`), Markdown, Mermaid.js.

**Spec:** `f:\OnThiC3\EnglishDocs\Agent.md`, `f:\OnThiC3\EnglishDocs\c674a7bc-c289-4cc6-8b91-d63996fc7c52_ExportBlock-3a529828-3dcf-422e-9e2f-431e356c1eba\EnglishDocs 26aeb70c17c580609c96e578765d55ad.md`, và bộ đề thi vào 10 Sở GD Quảng Ngãi.

## Global Constraints
- Phản hồi người dùng hoàn toàn bằng tiếng Việt chuẩn xác, sư phạm, súc tích.
- Ví dụ tiếng Anh đi kèm phiên âm chuẩn IPA (Cambridge/Oxford) và dịch nghĩa cô đọng.
- Triệt để tuân thủ bảng màu sư phạm Notion:
  - 🟦 Blue Callout: Công thức cốt lõi (Core Formula / Rule).
  - 🟩 Green Callout: Mẹo nhớ nhanh thần chú (Mnemonic).
  - 🟨 Yellow Callout: Lưu ý quan trọng & Ngoại lệ (Exceptions).
  - 🟥 Red Callout: Bẫy người Việt hay sai (Vietlish Traps / ❌ Sai -> ✅ Đúng).
  - 🟪 Purple Callout: Mở rộng nâng cao / Dạng thi chuyên.
- Không để sót rác quảng cáo, liên kết web rác cào tự động.
- Không in hàng nghìn dòng mã HTML thô ra cửa sổ chat; dùng `notion_html_exporter.py` để xuất file HTML.

## Review Focus
1. **Lỗi quy tắc phát âm -s/-es:** Trang cũ copy-paste nhầm quy tắc /iz/ cho cả 3 trường hợp /s/, /z/, /iz/. Phải sửa lại triệt để 3 nhóm âm thanh học chuẩn.
2. **Ngoại lệ phát âm đuôi -ed:** Học sinh thường quên các tính từ có đuôi -ed phát âm là /ɪd/ (*naked, wicked, sacred, beloved...*).
3. **Thiếu chuyên đề Trọng âm (Word Stress):** Đề thi vào 10 luôn có 2 câu trọng âm (từ 2 âm tiết và 3 âm tiết), nhưng Notion chưa có trang nào. Cần tạo trang mới hoàn chỉnh.
4. **Trùng lặp & rời rạc ở Ngữ pháp:** Hiện có nhiều subpage rời rạc cào từ Freetuts/Vietjack. Cần gom nhóm và tinh chỉnh theo ma trận đề thi 36 câu/45 câu.
5. **Cấu trúc Viết lại câu (Sentence Transformation):** Đây là phần tự luận lấy điểm 9-10 nhưng đang bị phân tán trong các bài lý thuyết. Phải có cẩm nang biến đổi câu chuyên biệt.

---

## Task List

### PHẦN 1: TỐI ƯU HÓA & LÀM MỚI CHUYÊN ĐỀ 1 (NGỮ ÂM & IPA)

#### Task 1.1: Sửa lỗi nghiêm trọng & làm mới trang "Phát âm S / ES chuẩn"
- **Notion Page ID:** `26ceb70c-17c5-808d-8f05-eeb481030dcf`
- **Mục tiêu:** Xóa bỏ hoàn toàn lỗi copy-paste nhầm quy tắc /iz/; viết lại 3 nhóm âm chuẩn kèm mẹo thần chú, bẫy Vietlish và bài tập đề thi vào 10.
- [x] **Step 1:** Đọc toàn bộ các block hiện tại của trang `26ceb70c-17c5-808d-8f05-eeb481030dcf`.
- [x] **Step 2:** Chuẩn bị nội dung chuẩn hóa:
  - 🟦 **Nhóm 1 (/s/):** Tận cùng là các âm vô thanh `/p, k, f, t, θ/`. Thần chú: *"Thời phong kiến phương Tây"* hoặc *"Thảo phải khao phở Thúy"*.
  - 🟦 **Nhóm 2 (/ɪz/):** Tận cùng là các âm gió (sibilants) `/s, z, ʃ, tʃ, ʒ, dʒ/` (Chữ cái: *s, ss, ch, sh, x, z, ge, ce*). Thần chú: *"Sông sáng chói sóng xô giáp ghềnh"*.
  - 🟦 **Nhóm 3 (/z/):** Tận cùng là các âm hữu thanh còn lại và nguyên âm.
  - 🟥 **Bẫy Vietlish & Ngoại lệ:** *houses* /ˈhaʊ.zɪz/, *months* /mʌnθs/ vs *clothes* /kləʊðz/, đuôi *-es* trong *goes* /ɡəʊz/, *does* /dʌz/.
  - 🟩 **10 câu trắc nghiệm thực chiến trích từ đề thi Sở GD Quảng Ngãi có đáp án và giải thích.**
- [x] **Step 3:** Xóa các block cũ bị lỗi và append nội dung mới đã định dạng màu sắc sư phạm.
- [x] **Step 4:** Kiểm tra lại trang qua Notion API.

#### Task 1.2: Chuẩn hóa & loại bỏ rác SEO trang "Các phát âm ED"
- **Notion Page ID:** `26ceb70c-17c5-8043-a717-f7090ef8608b`
- **Mục tiêu:** Xóa rác Langmaster; chuẩn hóa 3 nhóm phát âm đuôi -ed kèm bảng tính từ ngoại lệ kinh điển và 10 câu trắc nghiệm đề thi.
- [x] **Step 1:** Đọc và khảo sát toàn bộ các block trang `26ceb70c-17c5-8043-a717-f7090ef8608b`.
- [x] **Step 2:** Cập nhật nội dung theo quy tắc chuẩn:
  - 🟦 **/ɪd/:** Tận cùng là `/t/` và `/d/` (Thần chú: *"Tiền Đô"*).
  - 🟦 **/t/:** Tận cùng là âm vô thanh `/p, k, f, s, ʃ, tʃ/` (Thần chú: *"Chính phủ phát sách không thèm share"* / *"Phí sắm kính phật thoát"*).
  - 🟦 **/d/:** Các âm hữu thanh và nguyên âm còn lại.
  - 🟥 **Bẫy đề thi tuyển sinh 10 (Các tính từ đuôi -ed luôn đọc là /ɪd/):** *naked, wicked, sacred, beloved, hatred, crooked, ragged, learned*.
  - 🟩 **10 câu trắc nghiệm đề thi tuyển sinh 10 có đáp án chi tiết.**
- [x] **Step 3:** Ghi đè/cập nhật nội dung sạch lên Notion.
- [x] **Step 4:** Kiểm tra tính chính xác của trang.

#### Task 1.3: Tinh chỉnh trang "Bảng Phiên Âm IPA chuẩn (International Phonetic Alphabet)"
- **Notion Page ID:** `26ceb70c-17c5-80b7-9f42-c91372922a49`
- **Mục tiêu:** Cấu trúc lại bảng IPA trực quan, loại bỏ các đoạn văn rườm rà, tập trung vào đối chiếu âm Anh - Việt và các lỗi phát âm người Việt thường mắc.
- [x] **Step 1:** Rà soát các block trang `26ceb70c-17c5-80b7-9f42-c91372922a49`.
- [x] **Step 2:** Bổ sung các Callout màu về:
  - Bảng tóm tắt 44 âm: 12 nguyên âm đơn, 8 nguyên âm đôi, 24 phụ âm (8 cặp vô thanh - hữu thanh đối xứng).
  - 🟥 **Bẫy ngữ âm người Việt:** Thói quen nuốt âm cuối (*Ending Sounds* như `/t, d, s, z, k/`), nhầm lẫn âm ngắn/dài (`/i:/` - `/ɪ/`, `/u:/` - `/ʊ/`).
- [x] **Step 3:** Cập nhật nội dung lên Notion.

#### Task 1.4: Tinh chỉnh các trang ngữ âm chuyên sâu (/θ/ - /ð/, /æ/ - /e/)
- **Notion Page IDs:**
  - `Cách phát âm TH không gặp lỗi` (`26ceb70c-17c5-80ac-a20e-cfda6f9f177d`)
  - `CÁCH PHÁT ÂM /æ/ và /e/` (`26ceb70c-17c5-80d9-aae2-f3c17035c264`)
- [x] **Step 1:** Rà soát và cập nhật trang phát âm TH: Phân biệt `/θ/` (*think, thank, thick, breath*) vs `/ð/` (*this, that, there, breathe*).
- [x] **Step 2:** Cập nhật trang `/æ/` và `/e/`: Bảng cặp từ đối lập (*man* vs *men*, *bad* vs *bed*, *pan* vs *pen*).

#### Task 1.5: Khởi tạo trang mới "Quy tắc Trọng âm từ (Word Stress Mastery)"
- **Vị trí:** Subpage mới trực thuộc trang `EnglishDocs` (`26aeb70c-17c5-8060-9c96-e578765d55ad`).
- **Mục tiêu:** Bổ sung phần kiến thức trọng điểm còn thiếu cho đề thi vào 10.
- [x] **Step 1:** Soạn thảo nội dung chuẩn sư phạm:
  - Quy tắc từ 2 âm tiết: Danh từ & Tính từ nhấn âm 1; Động từ nhấn âm 2. Các ngoại lệ hay thi (*machine, mistake, canal, hotel, advice, desert/dessert*).
  - Quy tắc từ 3 âm tiết & Hậu tố (Suffixes):
    - Đuôi nhận trọng âm (*-ee, -eer, -ese, -ique*).
    - Đuôi làm trọng âm rơi vào âm trước nó (*-tion, -sion, -ic, -ity, -ical*).
    - Đuôi không ảnh hưởng trọng âm (*-ful, -less, -able, -er, -ly, -ness, -ment*).
  - 15 câu luyện trọng âm trích từ đề thi vào 10 Sở GD Quảng Ngãi.
- [x] **Step 2:** Tạo trang mới trên Notion bằng MCP.
- [x] **Step 3:** Append nội dung và kiểm tra.

---

### PHẦN 2: LẬP PLANS & XỬ LÝ CHUYÊN ĐỀ 2 (NGỮ PHÁP & BIẾN ĐỔI CÂU)

#### Task 2.1: Chuẩn hóa & Tinh gọn 12 Thì tiếng Anh (English Tenses)
- **Tập hợp subpages:** 12 subpage về các thì + 4 subpage so sánh thì (`26aeb70c-17c5-8018-8f09-f6a9ead9e8d4`).
- [x] **Step 1:** Rà soát nội dung từng thì, loại bỏ rác Freetuts.
- [x] **Step 2:** Thêm ASCII Timeline mô phỏng trục thời gian và công thức chuẩn hóa 3 dạng (+, -, ?).
- [x] **Step 3:** Xây dựng bảng ma trận so sánh các cặp thì kinh điển:
  - Hiện tại hoàn thành vs Quá khứ đơn (Có mốc thời gian cụ thể vs Hành động còn dư âm/kết quả ở hiện tại).
  - Tương lai đơn (*will*) vs Tương lai gần (*be going to*) vs Hiện tại tiếp diễn chỉ kế hoạch.
- [x] **Step 4:** Bổ sung quy tắc phối hợp thì với liên từ thời gian (*when, while, as soon as, by the time, until, since*).

#### Task 2.2: Xây dựng Cẩm nang 10 Cấu trúc Biến đổi câu (Sentence Transformation Mastery)
- **Mục tiêu:** Hệ thống hóa toàn bộ các dạng bài tự luận viết lại câu chắc chắn có mặt trong đề thi vào 10 Quảng Ngãi (`26aeb70c-17c5-8013-8bf1-d5f84e60bc0b`).
- [x] **Step 1:** 1. Câu điều kiện (Type 1, 2, 3, Unless = If not, Without, But for).
- [x] **Step 2:** 2. Câu bị động (Bị động thì cơ bản, Bị động kép với *It is said that / S + is said to V*, Bị động nhờ vả *Have/Get sth done*).
- [x] **Step 3:** 3. Câu gián tiếp (Reported Speech: Đổi ngôi - Lùi thì - Đổi trạng từ, Câu mệnh lệnh, Câu hỏi Yes/No, Câu hỏi Wh-).
- [x] **Step 4:** 4. Cấu trúc kết quả & mục đích (*So...that, Such...that, Too...to, Enough to, In order that / So that*).
- [x] **Step 5:** 5. Cấu trúc nhượng bộ (*Although / Even though / Though* <-> *In spite of / Despite*).
- [x] **Step 6:** 6. Cấu trúc chỉ lý do (*Because / Since / As* <-> *Because of / Due to*).
- [x] **Step 7:** 7. Cấu trúc câu ước (*Wish / If only* ở 3 thì).
- [x] **Step 8:** 8. Cấu trúc gợi ý (*Suggest + V-ing*, *Suggest that S + (should) V-bare*).
- [x] **Step 9:** 9. Cấu trúc so sánh (Chuyển đổi giữa So sánh hơn và So sánh không bằng, So sánh nhất).
- [x] **Step 10:** 10. Cấu trúc thời gian và sở thích (*Spend time doing = It takes time to do; Prefer V-ing to V-ing = Would rather V than V*).

#### Task 2.3: Chuẩn hóa Mệnh đề quan hệ & Rút gọn mệnh đề quan hệ
- **Subpage ID:** `26ceb70c-17c5-809f-bc2d-c9f05d830266` & `26aeb70c-17c5-8017-b5a0-f6d554626b41`
- [x] **Step 1:** Chuẩn hóa bảng đại từ & trạng từ quan hệ (*who, whom, which, that, whose, where, when, why*).
- [x] **Step 2:** Phân biệt rõ Mệnh đề quan hệ xác định vs Không xác định (khi nào dùng dấu phẩy, khi nào không được dùng *that*).
- [x] **Step 3:** 3 dạng rút gọn mệnh đề quan hệ hay ra thi: V-ing (chủ động), V3/ed (bị động), To-V (sau *the first, the only, so sánh nhất*).

#### Task 2.4: Chuẩn hóa Cấu tạo từ & Sự hòa hợp S-V (Word Form & Subject-Verb Agreement)
- **Subpage ID:** `26ceb70c-17c5-80c5-afed-f0a7531b77af`, `26ceb70c-17c5-8002-b2e9-c5f3fc925c7b`...
- [x] **Step 1:** Bảng tiếp đầu ngữ (tiền tố) và tiếp vĩ ngữ (hậu tố) nhận diện Danh - Động - Tính - Trạng.
- [x] **Step 2:** Quy tắc chia động từ với các chủ ngữ đặc biệt (*Each, Every, Either...or, Neither...nor, Not only...but also, A number of vs The number of*).

#### Task 2.5: Chuẩn hóa Danh động từ & Động từ nguyên mẫu (Gerunds & Infinitives: V-ing & To-V)
- **Subpage ID:** `26ceb70c-17c5-802b-818a-c5f8d7002c28`
- [x] **Step 1:** Soạn thảo bản chất cốt lõi (Feynman core: To-V tương lai/chưa xảy ra vs V-ing trải nghiệm/đã xảy ra).
- [x] **Step 2:** Bảng tổng hợp động từ đi với V-ing, To-V, và 6 cặp động từ đổi nghĩa kinh điển (*remember, forget, stop, try, regret, need*).
- [x] **Step 3:** 10 câu trắc nghiệm thực chiến trích từ đề thi vào 10 Sở GD Quảng Ngãi có đáp án toggle.
- [x] **Step 4:** Đồng bộ lên Notion qua `notion_pedagogy_engine.py`.

#### Task 2.6: Chuẩn hóa Câu hỏi đuôi & Trợ động từ (Question Tags Mastery)
- **Subpage ID:** `274eb70c-17c5-8062-8c0e-f8d5428cb752`
- [x] **Step 1:** Xây dựng quy tắc vàng "Trái dấu" (+ ➔ - và - ➔ +).
- [x] **Step 2:** 8 trường hợp đặc biệt chắc chắn gài bẫy (*I am, Let's, Mệnh lệnh, Từ phủ định ngầm never/hardly, Đại từ bất định they/it, I think...*).
- [x] **Step 3:** 10 câu trắc nghiệm câu hỏi đuôi thực chiến có giải thích chi tiết.
- [x] **Step 4:** Đồng bộ lên Notion qua `notion_pedagogy_engine.py`.

---

### PHẦN 3: TỐI ƯU HÓA CHUYÊN ĐỀ TỪ VỰNG TRỌNG TÂM (VOCABULARY MASTERY)

#### Task 3.1: Top 50 Cụm động từ (Phrasal Verbs) Tủ Thi Vào 10
- **Subpage ID:** `26ceb70c-17c5-8006-9227-c2066622f892` (`26ceb70c-17c5-80b8-b2cc-f0a12eda075d`)
- [x] **Step 1:** Tổng hợp 50 cụm động từ tần suất cao nhất phân loại theo gốc động từ (*LOOK, GO, TAKE, TURN, GIVE, COME, PUT, RUN, GET*).
- [x] **Step 2:** Bổ sung IPA, dịch nghĩa cô đọng, ví dụ theo ngữ cảnh đề thi và bẫy hay sai.
- [x] **Step 3:** 10 câu trắc nghiệm phrasal verbs kèm đáp án toggle.
- [x] **Step 4:** Đồng bộ lên Notion bằng chế độ append/replace an toàn qua `notion_pedagogy_engine.py`.

#### Task 3.2: Cẩm nang Từ đồng nghĩa & Trái nghĩa (Synonyms & Antonyms Mastery)
- **Subpage ID:** `26deb70c-17c5-809a-8749-e720654a8f22`
- [x] **Step 1:** Chiến thuật làm dạng bài CLOSEST / OPPOSITE (Kỹ thuật đoán nghĩa theo ngữ cảnh Context Clues).
- [x] **Step 2:** Bảng 40 cặp từ đồng nghĩa - trái nghĩa trọng điểm theo các chủ đề SGK lớp 9.
- [x] **Step 3:** 10 câu trắc nghiệm thực chiến trích từ đề tuyển sinh vào 10 Sở GD Quảng Ngãi.
- [x] **Step 4:** Đồng bộ lên Notion qua `notion_pedagogy_engine.py`.

---

### PHẦN 4: XUẤT BẢN & ĐỒNG BỘ NỘI DUNG (HTML EXPORT)

#### Task 4.1: Kiểm tra và xuất bản HTML hoàn chỉnh
- [x] **Step 1:** Chạy script `notion_html_exporter.py` / `export_english_mastery_booklet.py` để kéo toàn bộ cấu trúc trang `EnglishDocs` sau khi đã tối ưu.
- [x] **Step 2:** Xác nhận file HTML xuất ra giữ nguyên 100% định dạng, màu sắc callouts, toggle và sơ đồ.
- [x] **Step 3:** Báo cáo tổng kết và bàn giao.
