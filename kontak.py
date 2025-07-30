import streamlit as st

def tampilkan_kontak():
    st.title("Kontak")
    st.write("""
    Saya selalu terbuka untuk diskusi tentang proyek data science, kolaborasi, atau kesempatan kerja.  
    Jangan ragu untuk menghubungi saya melalui salah satu saluran berikut:
    """)

    # --- CSS untuk kartu ---
    st.markdown("""
    <style>
    .contact-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .contact-icon {
        font-size: 30px;
        margin-right: 15px;
        color: #2b6cb0;
    }
    .contact-header {
        font-size: 22px;
        font-weight: bold;
        color: #2b6cb0;
    }
    .contact-text {
        font-size: 16px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Kartu LinkedIn ---
    st.markdown("""
    <div class="contact-card">
        <div style="display:flex;align-items:center;">
            <span class="contact-icon">🔗</span>
            <div>
                <div class="contact-header"><a href="https://www.linkedin.com/in/bayusadewaazyumardi/" target="_blank">LinkedIn</a></div>
                <div class="contact-text">Terhubung dengan saya untuk jaringan profesional dan pembaruan karir.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Kartu GitHub ---
    st.markdown("""
    <div class="contact-card">
        <div style="display:flex;align-items:center;">
            <span class="contact-icon">💻</span>
            <div>
                <div class="contact-header"><a href="https://github.com/bayusadewa1" target="_blank">GitHub</a></div>
                <div class="contact-text">Lihat proyek open source dan repositori kode saya di GitHub.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Info tambahan ---
    st.subheader("Informasi Kontak Lainnya")
    st.markdown("""
    - 📧 **Email**: [bayu.sdwa.43@gmail.com](mailto:bayu.sdwa.43@gmail.com)  
    - 📱 **Telepon**: +62 819-9369-5432  
    - 🌐 **Website**: *coming soon*
    """)

    # --- Form kontak ---
    st.subheader("Formulir Kontak")
    with st.form("contact_form"):
        name = st.text_input("Nama Lengkap")
        email = st.text_input("Alamat Email")
        message = st.text_area("Pesan Anda")
        submitted = st.form_submit_button("Kirim Pesan")
        if submitted:
            st.success(f"Terima kasih {name}! Pesan Anda telah terkirim. Saya akan segera menghubungi Anda kembali.")