import streamlit as st
from groq import Groq

# Show title and description.
st.title("💬 Chatbot dengan Groq API")
st.write(
    "Ini chatbot sederhana menggunakan model Llama 3 dari Groq. "
    "Untuk menggunakan aplikasi ini, masukkan API Key dari Groq."
)

# Input API Key dari user
groq_api_key = st.text_input("Groq API Key", type="password")
if not groq_api_key:
    st.info("Masukkan API Key Groq Anda untuk melanjutkan.", icon="🗝️")
else:
    # Membuat client Groq
    client = Groq(api_key=groq_api_key)

    # Menyimpan pesan di session_state supaya tidak hilang
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan pesan lama
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input chat
    if prompt := st.chat_input("Apa kabar?"):
        # Simpan prompt user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate jawaban dari Groq API
        stream = client.chat.completions.create(
            model="llama3-8b-8192",   # Pilih model, bisa juga "mixtral-8x7b-32768" kalau mau
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream jawaban
        full_response = ""
        for chunk in stream:
            full_response += chunk.choices[0].delta.content or ""

        with st.chat_message("assistant"):
            st.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})