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
DOCUMENT_TEXT_URL = f"{BACKEND_URL}/documents/all"  # /documents/{id}

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
# Sidebar – Actions Only
# ======================================================
st.sidebar.header("📤 Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

if st.sidebar.button("Upload"):
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
                res = requests.post(UPLOAD_URL, files=files, timeout=120)
                if res.status_code != 201:
                    st.sidebar.error(res.text)
                else:
                    data = res.json()
                    st.sidebar.success(
                        f"✅ Uploaded (Document ID: {data['document_id']})"
                    )
            except requests.exceptions.RequestException as e:
                st.sidebar.error(str(e))

st.sidebar.divider()

st.sidebar.header("📌 Index Document")

index_doc_id = st.sidebar.number_input(
    "Document ID",
    min_value=1,
    step=1
)

if st.sidebar.button("Index"):
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
# Tabs
# ======================================================
ask_tab, docs_tab = st.tabs(["💬 Ask AI", "📂 Uploaded Documents"])

# ======================================================
# TAB 1 — Ask AI
# ======================================================
with ask_tab:
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

    if st.button("Ask AI"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        ASK_URL,
                        json={"query": query, "k": k},
                        timeout=60
                    )

                    if res.status_code != 200:
                        st.error(res.text)
                    else:
                        data = res.json()

                        st.subheader("🧠 Answer")
                        st.write(data.get("answer", ""))

                        c1, c2, c3 = st.columns(3)
                        c1.metric("Intent", data.get("intent"))
                        c2.metric("Used Web", str(data.get("use_web")))
                        c3.metric(
                            "Chunks Used",
                            len(data.get("documents", []))
                        )

                        if data.get("documents"):
                            st.subheader("📚 Retrieved Chunks")
                            for chunk in data["documents"]:
                                with st.expander(
                                    f"Doc {chunk['document_id']} | "
                                    f"Chunk {chunk['chunk_id']} | "
                                    f"Score {chunk['score']:.2f}"
                                ):
                                    st.write(chunk["content"])

                except requests.exceptions.RequestException as e:
                    st.error(str(e))

# ======================================================
# TAB 2 — Uploaded Documents
# ======================================================
with docs_tab:
    st.subheader("📂 Uploaded Documents")

    if st.button("🔄 Refresh Documents"):
        st.rerun()

    try:
        res = requests.get(DOCUMENTS_URL, timeout=30)

        if res.status_code != 200:
            st.error(res.text)
        else:
            documents = res.json()

            if not documents:
                st.info("No documents uploaded yet.")
            else:
                for doc in documents:
                    with st.expander(
                        f"📄 Document ID {doc['id']} — {doc.get('title', 'Untitled')}"
                    ):
                        st.markdown(
                            f"""
**Filename:** {doc.get('original_filename', 'N/A')}  
"""
                        )

                        try:
                            text_res = requests.get(
                                f"{DOCUMENT_TEXT_URL}/{doc['id']}",
                                timeout=30
                            )

                            if text_res.status_code == 200:
                                st.text_area(
                                    "📄 Extracted Text",
                                    text_res.json().get("content", ""),
                                    height=300,
                                    key=f"doc_text_{doc['id']}"
                                )
                            else:
                                st.warning("Unable to fetch document text.")

                        except requests.exceptions.RequestException:
                            st.warning("Backend not reachable.")

    except requests.exceptions.RequestException as e:
        st.error(str(e))
