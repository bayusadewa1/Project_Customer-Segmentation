import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def tampilkan_dashboard():
    st.title("Dashboard Analisis E-Commerce")
    st.write("Visualisasi transaksi e-commerce berdasarkan dataset yang diunggah.")

    uploaded_file = st.file_uploader("data clean (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Pastikan kolom Date dalam format datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        # ================== FILTER ==================
        st.sidebar.header("Filter Data")

        # Filter tanggal
        if 'Date' in df.columns:
            min_date, max_date = df['Date'].min(), df['Date'].max()
            date_range = st.sidebar.date_input(
                "Pilih Periode Tanggal",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # Filter country
        if 'Country' in df.columns:
            countries = ["All"] + sorted(df['Country'].unique())
            selected_country = st.sidebar.selectbox("Pilih Country", countries)
            if selected_country != "All":
                df = df[df['Country'] == selected_country]

        # ================== TABS ==================
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Univariate", "Bivariate", "Multivariate"])

        # ========== OVERVIEW ==========
        with tab1:
            st.header("Overview Data")

            st.subheader("Preview Data")
            st.dataframe(df.head())

            st.subheader("Ringkasan Statistik")
            st.write(df.describe())

            if 'Date' in df.columns:
                start_date_df, end_date_df = df['Date'].min(), df['Date'].max()
                period = end_date_df - start_date_df
                st.subheader("Periode Transaksi (Setelah Filter)")
                st.write(f"Start: {start_date_df}")
                st.write(f"End: {end_date_df}")
                st.write(f"Period: {period}")

            # Top 10 Countries
            st.subheader("Top 10 Countries by Transaction Frequency")
            fig, ax = plt.subplots(figsize=(14, 5))
            sns.countplot(y=df['Country'],
                          order=df['Country'].value_counts().iloc[:10].index, ax=ax)
            ax.bar_label(ax.containers[0], padding=3)
            st.pyplot(fig)

            # Top 10 Products
            st.subheader("Top 10 Products with The Most Purchases")
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.countplot(y=df['ProductName'],
                          order=df['ProductName'].value_counts().iloc[:10].index, ax=ax)
            ax.bar_label(ax.containers[0], padding=3)
            st.pyplot(fig)

        # ========== UNIVARIATE ==========
        with tab2:
            st.header("Univariate Analysis")

            if {'Price', 'Quantity', 'Revenue'}.issubset(df.columns):
                st.subheader("Summary Statistic (Numeric)")
                st.write(df[['Price','Quantity','Revenue']].describe().round(2))

            st.subheader("Summary Statistic (Categorical)")
            st.write(df[['TransactionNo','ProductNo','ProductName','CustomerNo',
                         'Country','DayOfWeek','Month','Year']].describe().round(2))

            st.subheader("Distribution of Numerical Variables")
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            for i, col in enumerate(['Price','Quantity','Revenue']):
                sns.boxplot(y=df[col], ax=axes[i])
                axes[i].set_title(f'Boxplot of {col}')
            st.pyplot(fig)

            st.subheader("Top 10 TransactionNo & CustomerNo")
            cols = ['TransactionNo','CustomerNo']
            fig, ax = plt.subplots(1, 2, figsize=(16, 5))
            for i in range(len(cols)):
                sns.countplot(y=df[cols[i]],
                              order=df[cols[i]].value_counts().iloc[:10].index,
                              ax=ax[i])
                ax[i].bar_label(ax[i].containers[0])
                ax[i].set_title(f'Distribution of {cols[i]}')
            st.pyplot(fig)

            st.subheader("Distribution of Day, Month, Year")
            cats = ['DayOfWeek','Month','Year']
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            for i in range(len(cats)):
                sns.countplot(x=cats[i], data=df, ax=axes[i])
                axes[i].bar_label(axes[i].containers[0], padding=3)
                axes[i].set_title(f'Distribution of {cats[i]}')
            st.pyplot(fig)

        # ========== BIVARIATE ==========
        with tab3:
            st.header("Bivariate Analysis")

            if 'Date' in df.columns:
                st.subheader("Sales Trend Over Time")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(x='Date', y='Revenue', data=df, ci=None, ax=ax)
                ax.set_title('Sales Trend Over Time')
                st.pyplot(fig)

            st.subheader("Monthly Average Sales Performance")
            monthly_avg = df.groupby('Month')['Revenue'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.lineplot(x='Month', y='Revenue', data=monthly_avg, marker='o', ax=ax)
            ax.set_xticks(range(1, 13))
            st.pyplot(fig)

            st.subheader("Monthly Average Product Price & Quantity")
            monthly_avg = df.groupby('Month')[['Price','Quantity']].mean().reset_index()
            fig, axes = plt.subplots(2, 1, figsize=(8, 6))
            sns.lineplot(x='Month', y='Price', data=monthly_avg, marker='o', ax=axes[0])
            axes[0].set_title('Monthly Average Product Price')
            sns.lineplot(x='Month', y='Quantity', data=monthly_avg, marker='o', ax=axes[1])
            axes[1].set_title('Monthly Average Product Quantity')
            st.pyplot(fig)

            st.subheader("Daily Average Sales Performance")
            avg_daily = df.groupby('DayOfWeek')['Revenue'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.lineplot(x='DayOfWeek', y='Revenue', data=avg_daily, marker='o', ax=ax)
            ax.set_xticks(range(7))
            ax.set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
            st.pyplot(fig)

            st.subheader("Top 10 Countries with Highest Sales")
            country_sales = df.groupby('Country', as_index=False)['Revenue'].sum()
            top10 = country_sales.sort_values('Revenue', ascending=False).iloc[:10]
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x='Revenue', y='Country', data=top10, ax=ax)
            labels = [f'{v/1_000_000:.1f}M' if v>=1_000_000 else f'{v/1_000:.0f}K' for v in top10['Revenue']]
            ax.bar_label(ax.containers[0], labels=labels, padding=3)
            st.pyplot(fig)

        # ========== MULTIVARIATE ==========
        with tab4:
            st.header("Multivariate Analysis")
            st.subheader("Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='YlOrBr', fmt='.2f', ax=ax)
            st.pyplot(fig)

            st.subheader("Pairplot of Numerical Variables")
            g = sns.pairplot(df[['Price','Quantity','Revenue']], diag_kind='kde',
                             plot_kws=dict(color='#DAA520'), diag_kws=dict(color='#DAA520'))
            st.pyplot(g)