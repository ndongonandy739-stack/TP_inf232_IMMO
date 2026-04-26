import streamlit as st
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.set_page_config(page_title="ImmoAnalytics Pro", page_icon="🏘️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏘️ ImmoAnalytics : Collecte & Analyse Descriptive")
st.markdown("---")

file = "immo_data.csv"
if not os.path.exists(file):
    df_init = pd.DataFrame(columns=["Date", "Surface", "Prix"])
    df_init.to_csv(file, index=False)

with st.sidebar:
    st.header("📥 Collecte des données")
    st.info("Remplissez les informations pour enrichir la base de données en ligne.")
    with st.form("form_collecte", clear_on_submit=True):
        surf = st.number_input("Surface du bien (m²)", min_value=1, help="Ex: 50")
        prix = st.number_input("Prix demandé (FCFA)", min_value=1000, step=5000)
        submitted = st.form_submit_button("Enregistrer la donnée")
        
        if submitted:
            date_now = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")
            df_new = pd.DataFrame([[date_now, surf, prix]], columns=["Date", "Surface", "Prix"])
            df_new.to_csv(file, mode='a', header=False, index=False)
            st.success("Donnée ajoutée avec succès !")

data = pd.read_csv(file)

if len(data) >= 3:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prix Moyen", f"{data['Prix'].mean():,.0f} FCFA")
    with col2:
        st.metric("Surface Moyenne", f"{data['Surface'].mean():.1f} m²")
    with col3:
        st.metric("Nombre d'entrées", len(data))

    st.markdown("---")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📈 Tendance du Marché")
        X = data[['Surface']]
        y = data['Prix']
        model = LinearRegression().fit(X, y)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(X, y, color="#007bff", alpha=0.6, label="Données réelles")
        ax.plot(X, model.predict(X), color="#ff4b4b", linewidth=2, label="Ligne de régression")
        ax.set_xlabel("Surface (m²)")
        ax.set_ylabel("Prix (FCFA)")
        ax.legend()
        st.pyplot(fig)

    with c2:
        st.subheader("📋 Dernières données")
        st.dataframe(data.tail(10), use_container_width=True)
        
    st.write(f"💡 **Analyse :** Actuellement, chaque mètre carré supplémentaire augmente le prix d'environ **{model.coef_[0]:,.0f} FCFA**.")

else:
    st.warning("⚠️ L'application est prête, mais elle a besoin d'au moins 3 entrées de données pour générer l'analyse descriptive et graphique.")
    st.image("https://via.placeholder.com/800x400.png?text=En+attente+de+données+de+collecte...")

