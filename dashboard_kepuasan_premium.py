
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Kepuasan Siswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Kepuasan Siswa")
st.markdown("### Analisis dan Visualisasi Data Survei Kepuasan")

st.divider()

# Upload File
uploaded_file = st.file_uploader(
    "📂 Upload File Excel Survei (format .xlsx)",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # Statistik Dasar
    jumlah_responden = df.shape[0]
    jumlah_pertanyaan = df.shape[1]
    rata_per_soal = df.mean()
    rata_total = df.values.mean()

    # Kategori Kepuasan
    if rata_total >= 4:
        kategori = "Sangat Puas"
    elif rata_total >= 3:
        kategori = "Puas"
    elif rata_total >= 2:
        kategori = "Cukup"
    else:
        kategori = "Kurang Puas"

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📌 Ringkasan", "📊 Grafik", "📄 Data", "📝 Kesimpulan"]
    )

    # TAB 1 - Ringkasan
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Responden", jumlah_responden)
        col2.metric("Jumlah Pertanyaan", jumlah_pertanyaan)
        col3.metric("Rata-rata Total", round(rata_total, 2))

        st.success(f"Tingkat Kepuasan: {kategori}")

        soal_tertinggi = rata_per_soal.idxmax()
        soal_terendah = rata_per_soal.idxmin()

        st.write("### 🔎 Analisis Soal")
        st.write(f"✅ Skor tertinggi: **{soal_tertinggi}**")
        st.write(f"⚠ Skor terendah: **{soal_terendah}**")

    # TAB 2 - Grafik
    with tab2:
        st.subheader("Grafik Rata-rata Skor per Soal")

        fig, ax = plt.subplots()
        ax.bar(rata_per_soal.index, rata_per_soal.values)
        ax.set_ylabel("Rata-rata Skor")
        ax.set_xlabel("Pertanyaan")
        ax.set_title("Rata-rata Skor per Soal")
        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.subheader("Distribusi Rata-rata")

        fig2, ax2 = plt.subplots()
        ax2.pie(rata_per_soal, labels=rata_per_soal.index, autopct='%1.1f%%')
        ax2.set_title("Distribusi Rata-rata per Soal")

        st.pyplot(fig2)

    # TAB 3 - Data
    with tab3:
        st.subheader("Data Responden")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Data (CSV)",
            data=csv,
            file_name="hasil_survei_kepuasan.csv",
            mime="text/csv"
        )

    # TAB 4 - Kesimpulan
    with tab4:
        st.write("### Kesimpulan Otomatis")

        st.write(f"""
        Berdasarkan hasil survei dari **{jumlah_responden} responden**, 
        diperoleh rata-rata skor keseluruhan sebesar **{round(rata_total,2)}** 
        yang termasuk kategori **{kategori}**.

        Pertanyaan dengan skor terendah (**{soal_terendah}**) 
        perlu menjadi perhatian untuk peningkatan kualitas layanan.
        """)

else:
    st.info("Silakan upload file Excel untuk menampilkan dashboard.")
