import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulator Populasi Peternakan", layout="wide")
st.title("Simulator Dinamika Populasi Peternakan (Metode Euler)")
st.markdown("Aplikasi simulasi pertumbuhan populasi ternak menggunakan Persamaan Diferensial Logistik dan Metode Numerik Euler.")

# Sidebar Kontrol Parameter
st.sidebar.header("Pengaturan Parameter (What-If)")
r_val = st.sidebar.slider("Laju Pertumbuhan Ternak (r / bulan)", min_value=0.05, max_value=0.50, value=0.22, step=0.01)
K_val = st.sidebar.slider("Kapasitas Maksimal Kandang (K ekor)", min_value=2000, max_value=10000, value=5000, step=250)
dt_val = st.sidebar.selectbox("Step Size Euler (dt bulan)", options=[1.0, 0.5, 0.1], index=0)

# Load Data
df = pd.read_csv("data_populasi_peternakan.csv")
P0 = df['Populasi_Ternak'].iloc[0]
t_max = df['Bulan'].max()

# Simulasi Euler dengan step size dinamis
t_sim = np.arange(0, t_max + dt_val, dt_val)
P_sim = np.zeros(len(t_sim))
P_sim[0] = P0

for i in range(1, len(t_sim)):
    P_sim[i] = P_sim[i-1] + dt_val * (r_val * P_sim[i-1] * (1 - P_sim[i-1] / K_val))

# Tampilkan Metrik Ringkas
col1, col2, col3 = st.columns(3)
col1.metric("Populasi Awal (Bulan 0)", f"{P0:,} ekor")
col2.metric(f"Prediksi Populasi (Bulan {t_max})", f"{int(P_sim[-1]):,} ekor")
col3.metric("Kapasitas Maksimal Kandang (K)", f"{K_val:,} ekor")

# Plot Grafik
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df['Bulan'], df['Populasi_Ternak'], color='black', label='Data Observasi Peternakan', zorder=5)
ax.plot(t_sim, P_sim, color='#1f77b4', linewidth=2.5, label=f'Simulasi Euler (r={r_val}, K={K_val}, dt={dt_val})')
ax.axhline(K_val, color='red', linestyle='--', label=f'Batas Kapasitas Kandang ({K_val:,} ekor)')
ax.set_xlabel("Waktu (Bulan)")
ax.set_ylabel("Populasi Ternak (Ekor)")
ax.set_title("Perbandingan Data Riil vs Simulasi Pertumbuhan Populasi Ternak")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)
