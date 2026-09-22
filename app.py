import streamlit as st
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from pypdf import PdfReader
from google import genai
from google.genai import errors

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="OmniMind AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supported Model
ACTIVE_MODEL = "gemini-3.6-flash"

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GEMINI_API_KEY")

# --- ULTRA-MODERN COLORFUL NEON-GLASS UI STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Vibrant Dark Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(236, 72, 153, 0.12) 0%, transparent 45%),
                    radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
                    #0b0f19;
        color: #f8fafc;
    }

    /* Branded Hero Header */
    .hero-container {
        padding: 30px;
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(16px);
        margin-bottom: 25px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .logo-badge {
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #06b6d4 100%);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.6);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }

    .hero-desc {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 6px;
    }

    /* Stylish Guide Card */
    .colorful-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    /* Colorful Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(17, 24, 39, 0.6);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 22px;
        border: none;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.35);
    }

    /* Output Card */
    .response-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #10b981;
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.3);
    }

    .response-header {
        font-weight: 700;
        color: #34d399;
        margin-bottom: 12px;
        font-size: 15px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(236, 72, 153, 0.45);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER WITH BRANDED LOGO ---
st.markdown("""
<div class="hero-container">
    <div class="logo-badge">⚡</div>
    <div>
        <h1 class="hero-title">OmniMind Studio AI</h1>
        <div class="hero-desc">Next-Gen Multi-Modal Intelligence • Content, Vision & Document Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Validate API Key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found! Please add it to your .env file.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=api_key)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🎛️ Control Studio")
    creativity = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.4, step=0.1)
    
    st.markdown("---")
    st.markdown("### 🌐 Live Infrastructure")
    st.markdown("🟢 **Model:** `gemini-3.6-flash`")
    st.markdown("🚀 **Engine:** Direct Model API")
    st.markdown("⚡ **Latency:** Sub-second Flash")
    
    st.markdown("---")
    if st.button("🧹 Clear All Output", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# Safe Request Handler
def generate_safe_content(contents, temp=0.4):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=ACTIVE_MODEL,
                contents=contents,
                config={"temperature": temp}
            )
            return response.text
        except errors.APIError as e:
            if e.code in [503, 429]:
                time.sleep(2)
                continue
            raise e
        except Exception as e:
            raise e
    raise Exception("Temporary service spike. Please try again in a few moments.")

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs([
    "✍️ Content & Code",
    "🎨 Vision & OCR",
    "📑 Document Intelligence"
])

# ================= PAGE 1: CONTENT & CODE =================
with tab1:
    st.markdown("""
    <div class="colorful-card">
        <b style="color: #38bdf8; font-size: 16px;">💡 Smart Generation & Coding Studio</b><br>
        <span style="color: #94a3b8;">Generate production code, debug architecture, or draft professional corporate documents.</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        template = st.selectbox(
            "Quick Templates",
            [
                "Custom Prompt",
                "Python Script Builder",
                "Code Debugger & Optimizer",
                "Professional Proposal Email",
                "Executive Summary Generator"
            ]
        )
    
    with col1:
        default_val = "" if template == "Custom Prompt" else f"Create a high quality {template} for: "
        user_input = st.text_area("Your instructions / code snippet:", value=default_val, height=130)

    if st.button("🚀 Generate Solution", key="btn_p1", use_container_width=True):
        if not user_input.strip():
            st.warning("Please enter your prompt.")
        else:
            with st.spinner("OmniMind is synthesizing..."):
                try:
                    res_text = generate_safe_content(user_input, temp=creativity)
                    st.markdown("""
                    <div class="response-card">
                        <div class="response-header">✨ Generated Output</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(res_text)
                    
                    # 1-Click Download Button
                    st.download_button(
                        label="📥 Download Output (.txt)",
                        data=res_text,
                        file_name="omnimind_output.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Execution Error: {e}")

# ================= PAGE 2: VISION & OCR =================
with tab2:
    st.markdown("""
    <div class="colorful-card">
        <b style="color: #f472b6; font-size: 16px;">🎨 Multi-Modal Vision & Parsing Studio</b><br>
        <span style="color: #94a3b8;">Upload charts, diagrams, bills, or designs for instant extraction and contextual insight.</span>
    </div>
    """, unsafe_allow_html=True)

    col_img, col_act = st.columns([1, 1])
    with col_img:
        uploaded_img = st.file_uploader("Upload Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], key="p2_uploader")
        if uploaded_img:
            image_obj = Image.open(uploaded_img)
            st.image(image_obj, caption="Preview", use_container_width=True)

    with col_act:
        vision_prompt = st.text_area(
            "Inspection Instruction:",
            value="Extract all visible text, recognize the layout, and explain the key information clearly.",
            height=130
        )
        run_vision = st.button("🔍 Run Visual Inspection", key="btn_p2", use_container_width=True)

    if run_vision:
        if not uploaded_img:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Analyzing pixels & textual components..."):
                try:
                    res_text = generate_safe_content([vision_prompt, image_obj], temp=0.2)
                    st.markdown("""
                    <div class="response-card">
                        <div class="response-header">🎯 Visual Intelligence Report</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(res_text)

                    st.download_button(
                        label="📥 Download Inspection Report (.txt)",
                        data=res_text,
                        file_name="vision_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Vision Error: {e}")

# ================= PAGE 3: DOCUMENT INTELLIGENCE =================
with tab3:
    st.markdown("""
    <div class="colorful-card">
        <b style="color: #34d399; font-size: 16px;">📑 Enterprise PDF Grounding Studio</b><br>
        <span style="color: #94a3b8;">Direct PDF context ingestion with zero hallucination. Ask questions straight against document facts.</span>
    </div>
    """, unsafe_allow_html=True)

    doc_file = st.file_uploader("Upload Document (PDF)", type=["pdf"], key="p3_uploader")
    
    if doc_file:
        st.success("✅ PDF loaded into memory context.")
        doc_query = st.text_input("What would you like to verify or extract?", placeholder="e.g., Summarize Section 3 and list all mentioned deadlines.")

        if st.button("⚡ Query Document Facts", key="btn_p3", use_container_width=True):
            if not doc_query.strip():
                st.warning("Please type a question regarding this document.")
            else:
                with st.spinner("Extracting text and verifying facts..."):
                    try:
                        reader = PdfReader(doc_file)
                        extracted = ""
                        for p in reader.pages:
                            t = p.extract_text()
                            if t:
                                extracted += t + "\n"

                        if not extracted.strip():
                            st.error("No readable text found. If this is a scanned photo PDF, use Page 2 (Vision & OCR).")
                        else:
                            grounded_prompt = f"""
                            You are a strict Enterprise Document Analyst.
                            Answer the user's question solely based on the context below.
                            If the answer is not contained in the text, respond: "Information not found in the uploaded document."

                            [CONTEXT]:
                            {extracted}

                            [QUERY]:
                            {doc_query}
                            """
                            res_text = generate_safe_content(grounded_prompt, temp=0.1)
                            st.markdown("""
                            <div class="response-card">
                                <div class="response-header">📋 Grounded Document Analysis</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(res_text)

                            st.download_button(
                                label="📥 Download Answer (.txt)",
                                data=res_text,
                                file_name="document_answer.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Document Error: {e}")