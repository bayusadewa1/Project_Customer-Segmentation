import streamlit as st

def tampilkan_tentang():
    st.title("Tentang Saya")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/300", caption="Foto Profil", width=200)
    
    with col2:
        st.write("""
        ### Hai, saya Bayu Sadewa Azyumardi
        
        Saya merupakan seorang Data Scientist dengan pengalaman dalam analisis data, machine learning, 
        dan pengembangan model prediktif. Saya memiliki passion untuk mengubah data menjadi wawasan 
        yang dapat ditindaklanjuti dan membantu pengambilan keputusan bisnis.
        
        **Latar Belakang Pendidikan:**
        - Sarjana Manajemen, Universitas Gunadarma
        - Bootcamp Data Science, dibimbing
        
        **Keahlian:**
        - Python (Pandas, NumPy, Scikit-learn)
        - Machine Learning (Supervised & Unsupervised)
        - Visualisasi Data (Matplotlib, Seaborn, Plotly)
        - SQL & Database Management
        - Streamlit & Dashboard Development
        
        **Mengapa Saya Memilih Karir Data Science:**
        Saya ingin menjadi data scientist karena bidang ini memiliki prospek kerja dan pertumbuhan 
        karir yang sangat bagus. Saya tertarik dengan kemampuan untuk mengekstrak wawasan berharga 
        dari data dan membuat solusi berbasis data yang berdampak nyata.
        
        **Proses Belajar:**
        Saya mempelajari skill teknis melalui bootcamp intensif dan terus mengembangkan pengetahuan 
        melalui proyek-proyek praktis dan pembelajaran mandiri. Saya percaya dalam pembelajaran 
        seumur hidup dan selalu mencari tantangan baru untuk meningkatkan kemampuan saya.
        """)