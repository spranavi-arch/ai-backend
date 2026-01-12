import streamlit as st
import requests

# ======================================================
# Backend URLs
# ======================================================
BACKEND_URL = "http://localhost:8000"

UPLOAD_URL = f"{BACKEND_URL}/documents/upload"
INDEX_URL = f"{BACKEND_URL}/documents/index"
ASK_URL = f"{BACKEND_URL}/ai/ask"
DOCUMENTS_URL = f"{BACKEND_URL}/documents/all"

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Assistant")
st.caption("OCR → Chunking → Vector Search → LangGraph Agent")

# ======================================================
# Sidebar – Upload Document
# ======================================================
st.sidebar.header("📤 Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

upload_btn = st.sidebar.button("Upload")

if upload_btn:
    if uploaded_file is None:
        st.sidebar.warning("Please upload a file.")
    else:
        with st.spinner("Uploading & extracting text..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                res = requests.post(
                    UPLOAD_URL,
                    files=files,
                    timeout=120
                )

                if res.status_code != 201:
                    st.sidebar.error(res.text)
                else:
                    data = res.json()
                    doc_id = data.get("document_id")

                    st.sidebar.success(f"✅ Document uploaded (ID: {doc_id})")

                    with st.sidebar.expander("📄 Extracted Text"):
                        st.write(data.get("extracted_text", ""))

            except requests.exceptions.RequestException as e:
                st.sidebar.error(str(e))

# ======================================================
# Sidebar – Index Existing Document
# ======================================================
st.sidebar.header("📌 Index Existing Document")

index_doc_id = st.sidebar.number_input(
    "Document ID",
    min_value=1,
    step=1
)

index_btn = st.sidebar.button("Index Document")

if index_btn:
    with st.spinner("Indexing document..."):
        try:
            res = requests.post(
                INDEX_URL,
                json={"document_id": index_doc_id},
                timeout=60
            )

            if res.status_code != 200:
                st.sidebar.error(res.text)
            else:
                st.sidebar.success("✅ Document indexed successfully!")

        except requests.exceptions.RequestException as e:
            st.sidebar.error(str(e))

# ======================================================
# Sidebar – View Documents (Single Click Toggle)
# ======================================================
st.sidebar.header("📂 Uploaded Documents")

show_docs = st.sidebar.checkbox("📄 Show Documents")

if show_docs:
    with st.spinner("Loading documents..."):
        try:
            res = requests.get(DOCUMENTS_URL, timeout=30)

            if res.status_code != 200:
                st.sidebar.error(res.text)
            else:
                docs = res.json()

                if not docs:
                    st.sidebar.info("No documents uploaded yet.")
                else:
                    for doc in docs:
                        st.sidebar.markdown(
                            f"""
**📄 Document ID:** `{doc['id']}`  
**Title:** {doc.get('title', 'N/A')}
---
"""
                        )

        except requests.exceptions.RequestException as e:
            st.sidebar.error(str(e))



# ======================================================
# Main – Ask AI
# ======================================================
st.subheader("💬 Ask Questions")

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_area(
        "Enter your query",
        placeholder="e.g. What is an invoice?"
    )

with col2:
    k = st.number_input(
        "Top-K Chunks",
        min_value=1,
        max_value=10,
        value=5
    )

ask_btn = st.button("Ask AI")

if ask_btn:
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    ASK_URL,
                    json={
                        "query": query,
                        "k": k
                    },
                    timeout=60
                )

                if res.status_code != 200:
                    st.error(res.text)
                else:
                    data = res.json()

                    # -----------------------------
                    # Answer
                    # -----------------------------
                    st.subheader("🧠 Answer")
                    st.write(data.get("answer", ""))

                    # -----------------------------
                    # Metadata
                    # -----------------------------
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Intent", data.get("intent"))
                    c2.metric("Used Web", str(data.get("use_web")))
                    c3.metric("Chunks Used", len(data.get("documents", [])))

                    # -----------------------------
                    # Retrieved Chunks
                    # -----------------------------
                    if data.get("documents"):
                        st.subheader("📚 Retrieved Chunks")

                        for doc in data["documents"]:
                            with st.expander(
                                f"Doc {doc['document_id']} | "
                                f"Chunk {doc['chunk_id']} | "
                                f"Score {doc['score']:.2f}"
                            ):
                                st.write(doc["content"])

            except requests.exceptions.RequestException as e:
                st.error(str(e))
