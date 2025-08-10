import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

st.set_page_config(layout="wide")
sns.set_style("whitegrid")

def map_cluster_labels_auto(rfm_df):
    stats = rfm_df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    r_min_cluster = stats['Recency'].idxmin()
    r_max_cluster = stats['Recency'].idxmax()
    f_min_cluster = stats['Frequency'].idxmin()
    f_max_cluster = stats['Frequency'].idxmax()
    m_min_cluster = stats['Monetary'].idxmin()
    m_max_cluster = stats['Monetary'].idxmax()

    cluster_map = {}
    for c in stats.index:
        if (c == r_min_cluster) and (c == f_max_cluster) and (c == m_max_cluster):
            cluster_map[c] = 'Loyal Customer'
        elif (c == r_max_cluster) and (c == f_min_cluster) and (c == m_min_cluster):
            cluster_map[c] = 'At Risk Customer'
        else:
            cluster_map[c] = 'Occasional Customer'
    return cluster_map

def tampilkan_model():
    st.title("Customer Segmentation dengan RFM & KMeans")

    uploaded = st.file_uploader("Upload dataset RFM CSV (harus ada kolom Recency, Frequency, Monetary)", type=['csv'])
    if uploaded is None:
        st.info("Silakan upload file CSV untuk mulai.")
        return

    try:
        rfm_df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Error membaca file CSV: {e}")
        return

    required_cols = {'Recency', 'Frequency', 'Monetary'}
    if not required_cols.issubset(rfm_df.columns):
        st.error(f"File harus berisi kolom: {required_cols}")
        return

    st.subheader("Preview Data")
    st.dataframe(rfm_df.head())

    # Scaling dan PCA - fit sekali dan simpan ke session_state
    if 'scaler' not in st.session_state or 'pca' not in st.session_state:
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_df[['Recency', 'Frequency', 'Monetary']])
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(rfm_scaled)

        st.session_state.scaler = scaler
        st.session_state.pca = pca
        st.session_state.rfm_scaled = rfm_scaled
        st.session_state.pca_result = pca_result
    else:
        scaler = st.session_state.scaler
        pca = st.session_state.pca
        rfm_scaled = st.session_state.rfm_scaled
        pca_result = st.session_state.pca_result

    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    st.subheader("Evaluasi Jumlah Cluster")
    max_k = st.slider("Pilih Max K", min_value=3, max_value=10, value=5)

    if st.button("Hitung SSE dan Silhouette"):
        sse = []
        sil = []
        for k in range(2, max_k + 1):
            km = KMeans(n_clusters=k, random_state=10, n_init=10)
            km.fit(pca_df)
            sse.append(km.inertia_)
            try:
                sil.append(silhouette_score(pca_df, km.labels_))
            except:
                sil.append(np.nan)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(x=range(2, max_k + 1), y=sse, marker='o', linestyle='--', label='Inertia/SSE', ax=ax)
        ax.set_xlabel('Number of Clusters (k)')
        ax.set_ylabel('Inertia / SSE')

        ax2 = ax.twinx()
        sns.lineplot(x=range(2, max_k + 1), y=sil, marker='o', linestyle='--', color='green', label='Silhouette Score', ax=ax2)
        ax2.set_ylabel('Silhouette Score')

        ax.set_title('SSE & Silhouette Score per K')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Jalankan KMeans")
    k_choice = st.slider("Pilih jumlah cluster (k)", min_value=2, max_value=max_k, value=3)

    if st.button("Jalankan Clustering"):
        km = KMeans(n_clusters=k_choice, random_state=10, n_init=10)
        labels = km.fit_predict(pca_df)
        rfm_df['Cluster'] = labels

        cluster_map = map_cluster_labels_auto(rfm_df)
        rfm_df['ClusterName'] = rfm_df['Cluster'].map(cluster_map)

        st.session_state.km = km
        st.session_state.cluster_map = cluster_map
        st.session_state.rfm_df = rfm_df

        st.success(f"KMeans selesai dengan k={k_choice}")
        st.write("Distribusi cluster:")
        st.dataframe(rfm_df['ClusterName'].value_counts().rename_axis('ClusterName').reset_index(name='count'))

        palette = {'Loyal Customer': 'green', 'At Risk Customer': 'red', 'Occasional Customer': 'gold'}
        pca_df['ClusterName'] = rfm_df['ClusterName']

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='ClusterName', palette=palette, s=70, ax=ax)
        ax.set_title(f"PCA Visualization dengan k={k_choice}")
        ax.legend(title='Cluster')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Profil RFM per Cluster")
        profile = rfm_df.groupby('ClusterName').agg({
            'Recency': ['mean', 'median', 'min', 'max'],
            'Frequency': ['mean', 'median', 'min', 'max'],
            'Monetary': ['mean', 'median', 'min', 'max'],
            'Cluster': 'count'
        }).round(2)
        profile.columns = ['_'.join(col).strip() for col in profile.columns.values]
        st.dataframe(profile)

        st.subheader("Distribusi RFM per Cluster")
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for i, col in enumerate(['Recency', 'Frequency', 'Monetary']):
            sns.boxenplot(x='ClusterName', y=col, data=rfm_df, palette=palette, ax=axes[i])
            axes[i].set_title(f'Distribusi {col} per Cluster')
            axes[i].set_xlabel('')
            axes[i].set_ylabel(col)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Proporsi Cluster")
        cluster_size = rfm_df['ClusterName'].value_counts().reset_index()
        cluster_size.columns = ['ClusterName', 'count']
        cluster_size['prop'] = (cluster_size['count'] / cluster_size['count'].sum() * 100).round(2)

        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(x='ClusterName', y='count', data=cluster_size, palette=palette, ax=ax)
        for i, p in enumerate(ax.patches):
            ax.text(p.get_x() + p.get_width()/2, p.get_height(), f"{cluster_size['prop'][i]}%", ha='center', va='bottom', fontweight='bold')
        ax.set_title("Proporsi Cluster")
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Simulasi Prediksi Cluster dari Nilai RFM")
    if 'km' not in st.session_state or 'cluster_map' not in st.session_state:
        st.info("Jalankan clustering terlebih dahulu untuk mengaktifkan prediksi.")
        return

    rfm_df = st.session_state.rfm_df

    r_min, r_max = int(rfm_df['Recency'].min()), int(rfm_df['Recency'].max())
    f_min, f_max = int(rfm_df['Frequency'].min()), int(rfm_df['Frequency'].max())
    m_min, m_max = int(rfm_df['Monetary'].min()), int(rfm_df['Monetary'].max())

    c1, c2, c3 = st.columns(3)
    with c1:
        R_val = st.slider("Recency (R)", r_min, r_max, int((r_min + r_max) / 2))
    with c2:
        F_val = st.slider("Frequency (F)", f_min, f_max, int((f_min + f_max) / 2))
    with c3:
        M_val = st.slider("Monetary (M)", m_min, m_max, int((m_min + m_max) / 2))

    if st.button("Prediksi Cluster dari Input RFM"):
        scaler = st.session_state.scaler
        pca = st.session_state.pca
        km = st.session_state.km
        cluster_map = st.session_state.cluster_map

        rfm_input = np.array([[R_val, F_val, M_val]])
        rfm_scaled_input = scaler.transform(rfm_input)
        pca_input = pca.transform(rfm_scaled_input)
        pred_cluster = km.predict(pca_input)[0]
        pred_label = cluster_map.get(pred_cluster, f"Cluster {pred_cluster}")

        st.success(f"Hasil prediksi: **{pred_label}** (Cluster ID: {pred_cluster})")
        if pred_label == 'Loyal Customer':
            st.info("💚 Loyal: Recency rendah (baru), Frequency tinggi, Monetary tinggi — fokus retention & upsell.")
        elif pred_label == 'At Risk Customer':
            st.warning("⚠️ At Risk: Recency tinggi (lama), Frequency rendah, Monetary rendah — butuh re-engagement.")
        else:
            st.info("💛 Occasional: RFM sedang — strategi tingkatkan frekuensi & nilai.")
