import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from datetime import datetime
import io
import base64

# ===============================
# KELAS DASAR MENGGUNAKAN INHERITANCE
# ===============================

class DataManager:
    """Kelas dasar untuk manajemen data"""
    def __init__(self, filename):
        self.filename = filename
        self.data = pd.DataFrame()
    
    def load_data(self):
        """Memuat data dari file CSV"""
        try:
            self.data = pd.read_csv(self.filename)
        except FileNotFoundError:
            self.data = pd.DataFrame()
    
    def save_data(self):
        """Menyimpan data ke file CSV"""
        self.data.to_csv(self.filename, index=False)
    
    def get_all_data(self):
        """Mengembalikan semua data"""
        return self.data

class OrganisasiManager(DataManager):
    """Kelas turunan untuk mengelola data organisasi masjid"""
    def __init__(self, filename="data_organisasi.csv"):
        super().__init__(filename)
        self.load_data()
    
    def tambah_anggota(self, nama, jabatan, divisi, gaji, telepon):
        """Menambahkan anggota baru"""
        # Generate ID otomatis
        if self.data.empty:
            new_id = 1
        else:
            new_id = self.data['ID'].max() + 1
            
        new_data = {
            'ID': new_id,
            'Nama': nama,
            'Jabatan': jabatan,
            'Divisi': divisi,
            'Gaji': gaji,
            'Telepon': telepon,
            'Tanggal_Bergabung': datetime.now().strftime("%Y-%m-%d")
        }
        
        if self.data.empty:
            self.data = pd.DataFrame([new_data])
        else:
            self.data = pd.concat([self.data, pd.DataFrame([new_data])], ignore_index=True)
        
        self.save_data()
        return True
    
    def edit_anggota(self, id_anggota, nama, jabatan, divisi, gaji, telepon):
        """Mengedit data anggota"""
        if not self.data.empty and id_anggota in self.data['ID'].values:
            idx = self.data[self.data['ID'] == id_anggota].index[0]
            self.data.at[idx, 'Nama'] = nama
            self.data.at[idx, 'Jabatan'] = jabatan
            self.data.at[idx, 'Divisi'] = divisi
            self.data.at[idx, 'Gaji'] = gaji
            self.data.at[idx, 'Telepon'] = telepon
            self.save_data()
            return True
        return False
    
    def hapus_anggota(self, id_anggota):
        """Menghapus data anggota"""
        if not self.data.empty and id_anggota in self.data['ID'].values:
            self.data = self.data[self.data['ID'] != id_anggota]
            self.save_data()
            return True
        return False

class VisualisasiManager:
    """Kelas untuk mengelola visualisasi data"""
    def grafik_gaji_divisi(self, data):
        """Membuat grafik gaji per divisi"""
        if data.empty:
            return None
        
        fig = px.pie(data, values='Gaji', names='Divisi', 
                     title='Distribusi Anggaran per Divisi',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    def grafik_struktur_organisasi(self, data):
        """Membuat grafik struktur organisasi"""
        if data.empty:
            return None
        
        jabatan_count = data['Jabatan'].value_counts()
        fig = px.bar(x=jabatan_count.index, y=jabatan_count.values,
                     title='Jumlah Anggota per Jabatan',
                     labels={'x': 'Jabatan', 'y': 'Jumlah'},
                     color=jabatan_count.values,
                     color_continuous_scale='Viridis')
        return fig

# ===============================
# APLIKASI UTAMA
# ===============================

class AplikasiMasjidAshobirin:
    def __init__(self):
        self.org_manager = OrganisasiManager()
        self.viz_manager = VisualisasiManager()
        self.setup_page()
    
    def setup_page(self):
        """Mengatur konfigurasi halaman"""
        st.set_page_config(
            page_title="Masjid Ashobirin - Sistem Organisasi",
            page_icon="🕌",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS untuk styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #2E86AB;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #A23B72;
            margin-bottom: 1rem;
        }
        .card {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            border-left: 5px solid #2E86AB;
            margin-bottom: 1rem;
        }
        .stButton button {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def sidebar_navigation(self):
        """Menampilkan sidebar navigation"""
        with st.sidebar:
            # PERBAIKAN: Gunakan URL gambar yang valid, bukan path lokal
            st.image("C:/Users/Rizky asifau/OneDrive/Pictures/images.jpg", 
                    use_container_width=True)
            
            selected = option_menu(
                menu_title="Menu Navigasi",
                options=["🏠 Beranda", "👥 Struktur Organisasi", "💰 Anggaran", "📊 Data & Laporan", "⚙️ Kelola Data"],
                icons=["house", "people", "cash-coin", "bar-chart", "gear"],
                menu_icon="menu-app",
                default_index=0,
                styles={
                    "container": {"padding": "5px", "background-color": "#f8f9fa"},
                    "icon": {"color": "#2E86AB", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
                    "nav-link-selected": {"background-color": "#2E86AB"},
                }
            )
        return selected
    
    def halaman_beranda(self):
        """Menampilkan halaman beranda"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="main-header">🕌 Masjid Ashobirin</div>', unsafe_allow_html=True)
            st.markdown("### Sistem Manajemen Organisasi & Keuangan")
            
            st.markdown("""
            <div class="card">
            <h4>🎯 Visi & Misi</h4>
            <p>Menjadi masjid yang menjadi pusat peradaban Islam, 
            mendukung kegiatan keagamaan, sosial, dan pendidikan 
            untuk kemaslahatan umat.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # PERBAIKAN: Gunakan URL gambar yang valid
            st.image("C:/Users/Rizky asifau/OneDrive/Pictures/images.jpg", 
                    use_container_width=True, caption="Masjid Ashobirin")
        
        # Statistik Cepat
        st.markdown("---")
        st.markdown("### 📈 Statistik Cepat")
        
        data = self.org_manager.get_all_data()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_anggota = len(data) if not data.empty else 0
            st.metric("Total Anggota", total_anggota)
        
        with col2:
            total_gaji = data['Gaji'].sum() if not data.empty else 0
            st.metric("Total Anggaran", f"Rp {total_gaji:,.0f}")
        
        with col3:
            avg_gaji = data['Gaji'].mean() if not data.empty else 0
            st.metric("Rata-rata Gaji", f"Rp {avg_gaji:,.0f}")
        
        with col4:
            divisi_count = data['Divisi'].nunique() if not data.empty else 0
            st.metric("Jumlah Divisi", divisi_count)
    
    def halaman_struktur(self):
        """Menampilkan struktur organisasi"""
        st.markdown('<div class="sub-header">👥 Struktur Organisasi Masjid Ashobirin</div>', unsafe_allow_html=True)
        
        data = self.org_manager.get_all_data()
        
        if not data.empty:
            # Tampilkan grafik struktur
            fig = self.viz_manager.grafik_struktur_organisasi(data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Tampilkan data dalam bentuk cards
            st.markdown("### 📋 Daftar Anggota Organisasi")
            
            for _, row in data.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.markdown(f"**{row['Nama']}**")
                        st.markdown(f"*{row['Jabatan']} - {row['Divisi']}*")
                    with col2:
                        st.markdown(f"📞 {row['Telepon']}")
                    with col3:
                        st.markdown(f"💰 Rp {row['Gaji']:,.0f}")
                    st.markdown("---")
        else:
            st.info("📝 Belum ada data organisasi. Silakan tambah data di menu 'Kelola Data'.")
    
    def halaman_anggaran(self):
        """Menampilkan informasi anggaran"""
        st.markdown('<div class="sub-header">💰 Analisis Anggaran Organisasi</div>', unsafe_allow_html=True)
        
        data = self.org_manager.get_all_data()
        
        if not data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Grafik pie distribusi anggaran
                fig_pie = self.viz_manager.grafik_gaji_divisi(data)
                if fig_pie:
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Tabel ringkasan anggaran per divisi
                st.markdown("### 📊 Ringkasan Anggaran per Divisi")
                summary = data.groupby('Divisi').agg({
                    'Gaji': ['sum', 'count']
                }).round(0)
                summary.columns = ['Total Gaji', 'Jumlah Anggota']
                summary['Rata-rata Gaji'] = (summary['Total Gaji'] / summary['Jumlah Anggota']).round(0)
                
                st.dataframe(summary.style.format({
                    'Total Gaji': 'Rp {:.0f}',
                    'Rata-rata Gaji': 'Rp {:.0f}'
                }), use_container_width=True)
            
            # Detail anggaran
            st.markdown("### 📋 Detail Anggaran per Anggota")
            display_data = data[['Nama', 'Jabatan', 'Divisi', 'Gaji']].copy()
            display_data['Gaji'] = display_data['Gaji'].apply(lambda x: f"Rp {x:,.0f}")
            st.dataframe(display_data, use_container_width=True)
            
        else:
            st.warning("Tidak ada data anggaran untuk ditampilkan.")
    
    def halaman_laporan(self):
        """Menampilkan laporan dan data"""
        st.markdown('<div class="sub-header">📊 Laporan & Analisis Data</div>', unsafe_allow_html=True)
        
        data = self.org_manager.get_all_data()
        
        if not data.empty:
            # Filter data
            col1, col2 = st.columns(2)
            with col1:
                divisi_filter = st.multiselect(
                    "Pilih Divisi:",
                    options=data['Divisi'].unique(),
                    default=data['Divisi'].unique()
                )
            with col2:
                jabatan_filter = st.multiselect(
                    "Pilih Jabatan:",
                    options=data['Jabatan'].unique(),
                    default=data['Jabatan'].unique()
                )
            
            # Filter data
            filtered_data = data[
                (data['Divisi'].isin(divisi_filter)) & 
                (data['Jabatan'].isin(jabatan_filter))
            ]
            
            # Tampilkan metrik
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Anggota Filter", len(filtered_data))
            with col2:
                st.metric("Total Anggaran Filter", f"Rp {filtered_data['Gaji'].sum():,.0f}")
            with col3:
                st.metric("Rata-rata Gaji", f"Rp {filtered_data['Gaji'].mean():,.0f}")
            
            # Ekspor data
            st.markdown("### 💾 Ekspor Data")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Download Data sebagai CSV"):
                    csv = filtered_data.to_csv(index=False)
                    st.download_button(
                        label="Klik untuk Download CSV",
                        data=csv,
                        file_name=f"data_organisasi_masjid_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📊 Download Data sebagai Excel"):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        filtered_data.to_excel(writer, index=False, sheet_name='Organisasi')
                    st.download_button(
                        label="Klik untuk Download Excel",
                        data=output.getvalue(),
                        file_name=f"data_organisasi_masjid_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.ms-excel"
                    )
            
        else:
            st.info("Belum ada data untuk dianalisis.")
    
    def halaman_kelola_data(self):
        """Halaman untuk mengelola data (CRUD)"""
        st.markdown('<div class="sub-header">⚙️ Kelola Data Organisasi</div>', unsafe_allow_html=True)
        
        # Tab untuk operasi CRUD
        tab1, tab2, tab3 = st.tabs(["➕ Tambah Anggota", "✏️ Edit Anggota", "🗑️ Hapus Anggota"])
        
        with tab1:
            self.form_tambah_anggota()
        
        with tab2:
            self.form_edit_anggota()
        
        with tab3:
            self.form_hapus_anggota()
        
        # Tampilkan data saat ini
        st.markdown("### 📋 Data Saat Ini")
        data = self.org_manager.get_all_data()
        if not data.empty:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("Belum ada data organisasi.")
    
    def form_tambah_anggota(self):
        """Form untuk menambah anggota baru"""
        with st.form("form_tambah", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nama = st.text_input("Nama Lengkap *", placeholder="Masukkan nama lengkap")
                jabatan = st.selectbox("Jabatan *", 
                    ["Ketua", "Wakil Ketua", "Sekretaris", "Bendahara", "Koordinator", "Anggota"])
                divisi = st.selectbox("Divisi *",
                    ["Takmir", "Dakwah", "Pendidikan", "Sosial", "Remaja", "Umum"])
            
            with col2:
                gaji = st.number_input("Gaji/Biaya Operasional (Rp) *", 
                    min_value=0, value=5000000, step=100000)
                telepon = st.text_input("Nomor Telepon", placeholder="08xxxxxxxxxx")
            
            st.markdown("**Wajib diisi*")
            submitted = st.form_submit_button("💾 Simpan Data")
            
            if submitted:
                if nama and jabatan and divisi:
                    if self.org_manager.tambah_anggota(nama, jabatan, divisi, gaji, telepon):
                        st.success("✅ Data anggota berhasil ditambahkan!")
                        st.rerun()
                else:
                    st.error("❌ Harap isi semua field yang wajib!")
    
    def form_edit_anggota(self):
        """Form untuk mengedit data anggota"""
        data = self.org_manager.get_all_data()
        
        if not data.empty:
            pilihan_anggota = st.selectbox(
                "Pilih Anggota untuk Edit:",
                options=data['ID'].values,
                format_func=lambda x: f"{data[data['ID']==x]['Nama'].iloc[0]} (ID: {x})"
            )
            
            if pilihan_anggota:
                anggota_data = data[data['ID'] == pilihan_anggota].iloc[0]
                
                with st.form("form_edit"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nama = st.text_input("Nama Lengkap", value=anggota_data['Nama'])
                        jabatan = st.selectbox("Jabatan", 
                            ["Ketua", "Wakil Ketua", "Sekretaris", "Bendahara", "Koordinator", "Anggota"],
                            index=["Ketua", "Wakil Ketua", "Sekretaris", "Bendahara", "Koordinator", "Anggota"].index(anggota_data['Jabatan']))
                        divisi = st.selectbox("Divisi",
                            ["Takmir", "Dakwah", "Pendidikan", "Sosial", "Remaja", "Umum"],
                            index=["Takmir", "Dakwah", "Pendidikan", "Sosial", "Remaja", "Umum"].index(anggota_data['Divisi']))
                    
                    with col2:
                        gaji = st.number_input("Gaji/Biaya Operasional (Rp)", 
                            min_value=0, value=int(anggota_data['Gaji']), step=100000)
                        telepon = st.text_input("Nomor Telepon", value=anggota_data['Telepon'])
                    
                    submitted = st.form_submit_button("✏️ Update Data")
                    
                    if submitted:
                        if nama and jabatan and divisi:
                            if self.org_manager.edit_anggota(pilihan_anggota, nama, jabatan, divisi, gaji, telepon):
                                st.success("✅ Data anggota berhasil diupdate!")
                                st.rerun()
                        else:
                            st.error("❌ Harap isi semua field yang wajib!")
        else:
            st.info("Belum ada data untuk diedit.")
    
    def form_hapus_anggota(self):
        """Form untuk menghapus data anggota"""
        data = self.org_manager.get_all_data()
        
        if not data.empty:
            pilihan_hapus = st.selectbox(
                "Pilih Anggota untuk Dihapus:",
                options=data['ID'].values,
                key="hapus_select",
                format_func=lambda x: f"{data[data['ID']==x]['Nama'].iloc[0]} (ID: {x})"
            )
            
            if pilihan_hapus:
                anggota_data = data[data['ID'] == pilihan_hapus].iloc[0]
                
                st.warning(f"⚠️ Anda akan menghapus data: **{anggota_data['Nama']}** ({anggota_data['Jabatan']} - {anggota_data['Divisi']})")
                
                if st.button("🗑️ Hapus Permanen", type="primary"):
                    if self.org_manager.hapus_anggota(pilihan_hapus):
                        st.success("✅ Data anggota berhasil dihapus!")
                        st.rerun()
        else:
            st.info("Belum ada data untuk dihapus.")
    
    def run(self):
        """Menjalankan aplikasi utama"""
        selected = self.sidebar_navigation()
        
        # PERBAIKAN: Gunakan if statement yang benar
        if selected == "🏠 Beranda":
            self.halaman_beranda()
        elif selected == "👥 Struktur Organisasi":
            self.halaman_struktur()
        elif selected == "💰 Anggaran":
            self.halaman_anggaran()
        elif selected == "📊 Data & Laporan":
            self.halaman_laporan()
        elif selected == "⚙️ Kelola Data":
            self.halaman_kelola_data()

# ===============================
# MENJALANKAN APLIKASI
# ===============================

if __name__ == "__main__":
    app = AplikasiMasjidAshobirin()
    app.run()