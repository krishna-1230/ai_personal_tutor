import streamlit as st
from PIL import Image
import PyPDF2
import io
import requests
import google.generativeai as genai

# --- Gemini API Setup ---
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash-preview-05-20"

# --- Session State for Q&A History ---
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# --- Sidebar Navigation ---
pages = ["Ask Tutor", "Session History"]
page = st.sidebar.radio("Navigate", pages)

# --- Helper: Extract text from PDF ---
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- Helper: Gemini Vision API Call ---
def gemini_ask(prompt, image=None, pdf_text=None):
    model = genai.GenerativeModel(MODEL_NAME)
    if image:
        response = model.generate_content([
            prompt,
            image
        ])
    elif pdf_text:
        response = model.generate_content([
            prompt + "\n" + pdf_text
        ])
    else:
        response = model.generate_content([prompt])
    return response.text

# --- Helper: Gemini TTS API Call ---
# def gemini_tts(text):
#     tts_model = "models/gemini-2.5-flash-preview-tts"
#     model = genai.GenerativeModel(tts_model)
#     response = model.generate_content(
#         [text],
#         generation_config={"response_mime_type": "audio/wav"}
#     )
#     # Extract audio bytes from the response
#     audio_data = response.parts[0].data if hasattr(response.parts[0], 'data') else None
#     return audio_data

# --- Ask Tutor Page ---
if page == "Ask Tutor":
    st.title("📚 Multi-Modal Personal Tutor")
    st.write("Upload a math/physics question (image or PDF), or ask a follow-up question.")

    uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])
    user_question = st.text_area("Or type your question here:")
    submit = st.button("Ask Tutor")

    if submit:
        answer = None
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                pdf_text = extract_text_from_pdf(uploaded_file)
                answer = gemini_ask(user_question or "Explain this question.", pdf_text=pdf_text)
            else:
                image = Image.open(uploaded_file)
                answer = gemini_ask(user_question or "Explain this question.", image=image)
        elif user_question.strip():
            answer = gemini_ask(user_question)
        else:
            st.warning("Please upload a file or enter a question.")
        if answer:
            st.session_state.qa_history.append({"question": user_question or "[File Upload]", "answer": answer})
            st.markdown(f"**Tutor:** {answer}")

    # Add TTS button if there is an answer
    # TODO: Re-enable TTS (speech) feature in the future
    # if st.session_state.qa_history:
    #     last_answer = st.session_state.qa_history[-1]["answer"]
    #     if st.button("🔊 Read Out Answer"):
    #         audio_bytes = gemini_tts(last_answer)
    #         if audio_bytes:
    #             st.audio(audio_bytes, format="audio/wav")
    #         else:
    #             st.error("TTS audio could not be generated.")

# --- Session History Page ---
elif page == "Session History":
    st.title("🕑 Session Q&A History")
    if st.session_state.qa_history:
        for i, qa in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {qa['question']}")
            st.markdown(f"**A{i}:** {qa['answer']}")
            st.markdown("---")
    else:
        st.info("No Q&A history yet. Ask something on the 'Ask Tutor' page!") 