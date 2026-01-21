import streamlit as st
import urllib.parse
import base64
import re

# ───────────────────────── 0. UI & ảnh nền ─────────────────────────
st.set_page_config(page_title="Tự động mở DOI/PMID trên Sci-Hub", layout="centered")

def img_to_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

bg_data = img_to_b64("a1.png")          # (tùy chọn) đặt BACKGROUND
st.markdown(f"""
<style>
html,body,.stApp{{height:100%;margin:0}}
body{{background:url("data:image/png;base64,{bg_data}") center/cover fixed}}
.stApp{{backdrop-filter:blur(6px);background:rgba(0,0,0,.35);color:#fff}}
h1,h2,h3,h4,h5,h6,label,.stMarkdown{{color:#fff!important}}
textarea{{background:rgba(255,255,255,.9)!important;color:#000;font-weight:500}}
.stButton>button{{background:#fff!important;color:#000!important;font-weight:600}}
</style>
""", unsafe_allow_html=True)

# ───────────────────────── 1. Hàm tiện ích ─────────────────────────
SCI_HUB = "https://sci-hub.box"          # thay mirror nếu cần

def clean(q: str) -> str:
    q = q.strip()
    q = re.sub(r"https?://doi\.org/", "", q, flags=re.I)
    if q.lower().startswith("doi:"):
        q = q[4:]
    return q

def make_url(q: str) -> str:
    return f"{SCI_HUB}/{urllib.parse.quote(clean(q), safe='/')}"

# ───────────────────────── 2. Giao diện ─────────────────────────
st.title("Tự động mở nhiều DOI/PMID trên Sci-Hub")

raw = st.text_area(
    "Nhập DOI/PMID (mỗi dòng một mục):",
    height=200,
    placeholder="10.1007/978-1-61779-624-1_9\nPMID: 12345678",
)

if st.button("🔍  Tạo liên kết Sci-Hub"):
    entries = [e for e in (i.strip() for i in raw.splitlines()) if e]
    if not entries:
        st.warning("⚠️ Vui lòng nhập ít nhất một DOI/PMID.")
    else:
        st.session_state.links = [{"kw": e, "url": make_url(e)} for e in entries]
        st.success(f"Đã tạo {len(entries)} liên kết.")

# ───────────────────────── 3. Mở đồng loạt các tab ─────────────────────────
if "links" in st.session_state and st.session_state.links:
    if st.button("🚀  Mở tất cả trong tab mới (đồng thời)"):
        # JS: mỗi DOI → 1 tab, tất cả thực thi ngay lập tức
        urls = ",".join(f'"{d["url"]}"' for d in st.session_state.links)
        js = f"""
        <script>
        const sciHubHome = "{SCI_HUB}";
        const targets = [{urls}];

        targets.forEach(target => {{
            // ① mở about:blank để giữ handle tab
            const tab = window.open("about:blank", "_blank");
            // ② nạp trang chủ Sci-Hub để nhận cookie
            tab.location = sciHubHome;
            // ③ sau 1,2 s chuyển luôn tới DOI
            setTimeout(() => {{ tab.location = target; }}, 1200);
        }});
        </script>
        """
        st.components.v1.html(js, height=0)

    st.warning("Nếu trình duyệt chặn pop-up, hãy **Allow pop-ups** để code hoạt động.")

    try:
        st.image("a2.png", caption="Cho phép pop-up để tự mở tab", width=600)
    except FileNotFoundError:
        pass
