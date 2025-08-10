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
        
        ---
        ### Project Background
        E-commerce telah menjadi penggerak utama transformasi digital, memungkinkan jangkauan pasar lebih luas 
        dan biaya distribusi lebih rendah.
        
        Perusahaan ritel online di Inggris yang menjual hadiah & perlengkapan rumah ingin meningkatkan strategi 
        pemasaran dan pengalaman pelanggan.
        
        Dengan data transaksi 1 tahun (Des 2018 – Des 2019), perusahaan perlu memahami perilaku pelanggan 
        dan mengelompokkan mereka dalam segmen yang relevan.
        
        **Problem Statement:**
        Perusahaan ritel online belum memiliki pemahaman mendalam mengenai perilaku pelanggan sehingga strategi 
        pemasaran masih bersifat umum dan kurang efektif. Diperlukan segmentasi pelanggan berbasis analisis data 
        (EDA, RFM, K-Means) untuk mendukung strategi pemasaran yang lebih terarah dan personal.
        
        **Tujuan Bisnis:**
        - Menggunakan EDA & K-Means Clustering untuk menemukan pola pelanggan.
        - Menerapkan RFM (Recency, Frequency, Monetary) untuk memahami perilaku pelanggan.
        - Memberikan rekomendasi strategis untuk pemasaran & retensi pelanggan.
        - Mendukung strategi personalisasi & efisiensi biaya pemasaran guna meningkatkan penjualan & loyalitas pelanggan.
        """)