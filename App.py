import streamlit as st
import urllib.parse
import base64

# Cấu hình Streamlit
st.set_page_config(page_title="Tự động tìm kiếm Sci-Hub", layout="centered")

# === Load ảnh nền ===
# Giả sử file ảnh a1.png tồn tại trong cùng thư mục
# Nếu không, cần cung cấp đường dẫn đúng hoặc xử lý lỗi
try:
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    img_base64 = get_base64_image("a1.png")
except FileNotFoundError:
    img_base64 = "" # Không có ảnh nền nếu file không tìm thấy
    st.warning("Không tìm thấy file ảnh nền 'a1.png'. Bỏ qua ảnh nền.")

# === CSS giao diện đẹp + ảnh nền ===
st.markdown(
    f"""
    <style>
    html, body, .stApp {{
        margin: 0;
        padding: 0;
        height: 100%;
    }}

    body {{
        background-image: url("{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: 50% 50%;
    }}

    header {{
        visibility: hidden;
        height: 0px;
    }}

    .stApp {{
        backdrop-filter: blur(8px);
        background-color: rgba(0, 0, 0, 0.4);
        color: #fff;
    }}

    h1, h2, h3, h4, h5, h6, label, .stText, .stMarkdown {{
        color: #ffffff !important;
    }}

    textarea, .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        font-weight: 500;
    }}

    .stButton > button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #aaa;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# === Giao diện người dùng ===
st.title("Tự động mở nhiều từ khoá trên Sci-Hub")

keywords_input = st.text_area(
    "Nhập từ khóa/DOI/PMID tại đây (mỗi dòng là 1 mục):",
    placeholder="Mỗi từ khoá, DOI hoặc PMID là 1 dòng nha mọi người",
    height=200
)

# === Nút tạo danh sách link tìm kiếm ===
if st.button("🔍Đã nhập đủ (Tạo liên kết Sci-Hub)"):
    keywords = [kw.strip() for kw in keywords_input.splitlines() if kw.strip()]
    if not keywords:
        st.warning("⚠️ Vui lòng nhập ít nhất một từ khóa, DOI hoặc PMID.")
    else:
        st.session_state.links = [
            {
                "keyword": kw,
                # Thay đổi URL đích sang Sci-Hub
                # Sci-Hub thường nhận truy vấn trực tiếp sau tên miền
                "url": f"https://www.sci-hub.se/{urllib.parse.quote_plus(kw)}"
            }
            for kw in keywords
        ]
        st.success(f"Đã tạo {len(st.session_state.links)} liên kết Sci-Hub. Hãy ấn nút bên dưới để mở tất cả trong tab mới.")
        st.info("Lưu ý: Sci-Hub hoạt động tốt nhất với DOI hoặc PMID. Kết quả tìm kiếm theo từ khóa có thể không như mong đợi.")

# === Nếu đã có link thì hiển thị nút mở tất cả và danh sách ===
if 'links' in st.session_state and st.session_state.links:
    if st.button("🚀 Mở tất cả liên kết trong tab mới"):
        all_scripts = "\n".join([
            f'<script>window.open("{item["url"]}", "_blank", "noopener")</script>'
            for item in st.session_state.links
        ])
        st.components.v1.html(all_scripts, height=0)

    # Giữ nguyên cảnh báo về pop-up và hình ảnh minh họa
    st.warning("""⚠️Lưu ý nếu lúc sử dụng web này mà thông báo hiện biểu tượng chặn mở tab mới (như hình dưới). Hãy chọn 'Allow pop-ups' để cho phép tự động mở trang mới tài liệu. ⚠️
Ngoài ra ai sử dụng web bằng điện thoại app Chrome, Sarafi,... thì sẽ hiện thông báo cho phép mở trang thì mọi người nhớ chọn cho phép nhé""")
    # Giả sử file ảnh a2.png tồn tại trong cùng thư mục
    try:
        st.image("a2.png", caption="Hình minh họa pop-up bị chặn", width=600)
    except FileNotFoundError:
        st.warning("Không tìm thấy file ảnh minh họa 'a2.png'.")

