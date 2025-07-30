import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Customer Segmentation Portfolio",
    layout="wide",
    page_icon=":bar_chart:"
)

st.title("Portfolio Saya")
st.header("Data Scientist")

# Sidebar Navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Tentang Saya", "Dashboard", "Machine Learning", "Kontak"])

# Routing
if page == "Tentang Saya":
    import tentang
    tentang.tampilkan_tentang()

elif page == "Dashboard":
    import dashboard
    dashboard.tampilkan_dashboard()

elif page == "Machine Learning":
    import model
    model.tampilkan_model()

elif page == "Kontak":
    import kontak
    kontak.tampilkan_kontak()