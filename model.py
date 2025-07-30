import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

def tampilkan_model():
    st.title("Customer Segmentation (RFM + PCA + K-Means)")

    uploaded_file = st.file_uploader("Upload Dataset RFM (CSV)", type=["csv"])
    if not uploaded_file:
        st.info("Silakan upload file. Pastikan data sudah terbagi menjadi RFM dan bersih dari outlier")
        return

    # Baca dataset
    df = pd.read_csv(uploaded_file)

    # Konversi ke datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # --- FILTER ---
    st.sidebar.header("Filter Data")
    # Filter tanggal
    if 'Date' in df.columns:
        min_date, max_date = df['Date'].min(), df['Date'].max()
        start_date, end_date = st.sidebar.date_input("Rentang Tanggal",
                                                     [min_date, max_date])
        df = df[(df['Date'] >= pd.to_datetime(start_date)) &
                (df['Date'] <= pd.to_datetime(end_date))]
    # Filter negara
    if 'Country' in df.columns:
        countries = st.sidebar.multiselect("Pilih Negara", df['Country'].unique(),
                                           default=df['Country'].unique())
        df = df[df['Country'].isin(countries)]

    # --- TABS ---
    tab1, tab2 = st.tabs(["EDA", "Clustering"])

    # ================= TAB 1: EDA =================
    with tab1:
        st.subheader("Data Setelah Filter")
        st.write(df.head())

        st.subheader("Statistik Deskriptif")
        st.write(df[['Recency', 'Frequency', 'Monetary']].describe())

        # Boxplot per variabel
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.boxplot(y='Recency', data=df, ax=axes[0])
        axes[0].set_title('Recency')
        sns.boxplot(y='Frequency', data=df, ax=axes[1])
        axes[1].set_title('Frequency')
        sns.boxplot(y='Monetary', data=df, ax=axes[2])
        axes[2].set_title('Monetary')
        st.pyplot(fig)

    # ================= TAB 2: CLUSTERING =================
    with tab2:
        # Load pipeline (scaler + PCA + kmeans)
        pipeline = joblib.load("pipeline_rfm.pkl")

        X = df[['Recency', 'Frequency', 'Monetary']]
        df['Cluster'] = pipeline.predict(X)

        st.subheader("Ringkasan Cluster (Mean)")
        cluster_summary = df.groupby('Cluster')[['Recency','Frequency','Monetary']].mean().round(2)
        st.write(cluster_summary)

        # PCA scatter plot
        X_pca = pipeline.named_steps['pca'].transform(
            pipeline.named_steps['scaler'].transform(X)
        )
        df_pca = pd.DataFrame(X_pca, columns=['pc1', 'pc2'])
        df_pca['Cluster'] = df['Cluster']

        fig1, ax1 = plt.subplots()
        sns.scatterplot(x='pc1', y='pc2', hue='Cluster', palette='Set2', data=df_pca, ax=ax1)
        ax1.set_title('Hasil Clustering (PCA 2D)')
        st.pyplot(fig1)

        # Pie chart proporsi cluster
        cluster_counts = df['Cluster'].value_counts().sort_index()
        fig2, ax2 = plt.subplots()
        ax2.pie(cluster_counts, labels=cluster_counts.index, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.subheader("Proporsi Cluster")
        st.pyplot(fig2)

        # Boxplot RFM per cluster
        st.subheader("Distribusi RFM per Cluster")
        fig3, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.boxplot(x='Cluster', y='Recency', data=df, palette='Set2', ax=axes[0])
        sns.boxplot(x='Cluster', y='Frequency', data=df, palette='Set2', ax=axes[1])
        sns.boxplot(x='Cluster', y='Monetary', data=df, palette='Set2', ax=axes[2])
        axes[0].set_title("Recency")
        axes[1].set_title("Frequency")
        axes[2].set_title("Monetary")
        st.pyplot(fig3)
