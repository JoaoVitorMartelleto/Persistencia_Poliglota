import streamlit as st
import pandas as pd
import os

from db_sqlite import criar_conexao_sqlite, criar_tabelas, inserir_estado, inserir_cidade, listar_cidades
import db_mongo as dbm

# Initialize DBs
conn = criar_conexao_sqlite()
criar_tabelas(conn)

st.set_page_config(page_title="Persistência Poliglota", layout="wide")
st.title("Persistência Poliglota: SQLite + MongoDB (Geoprocessamento)")

with st.sidebar:
    st.subheader("Config")
    st.write("MongoDB URI (env var MONGODB_URI)")

st.header("1) Cadastrar Estado e Cidade (SQLite)")
with st.form("form_cidade"):
    estado = st.text_input("Estado")
    cidade = st.text_input("Cidade")
    btn = st.form_submit_button("Inserir cidade")
    if btn:
        if not estado or not cidade:
            st.error("Preencha estado e cidade")
        else:
            estado_id = inserir_estado(conn, estado)
            inserir_cidade(conn, cidade, estado_id)
            st.success(f"Cidade '{cidade}' inserida no estado '{estado}'")

st.header("2) Cadastrar Local (MongoDB)")
cidades = listar_cidades(conn)
cidade_options = [f"{c['cidade']} - {c['estado'] or ''}" for c in cidades]
cidade_sel = st.selectbox("Selecione a cidade (SQLite)", options=cidade_options) if cidade_options else None

with st.form("form_local"):
    nome_local = st.text_input("Nome do local")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição")
    btn_local = st.form_submit_button("Inserir local")
    if btn_local:
        if not nome_local or cidade_sel is None:
            st.error("Preencha o nome do local e selecione a cidade")
        else:
            cidade_text = cidade_sel.split(" - ")[0]
            try:
                inserted_id = dbm.inserir_local(nome_local, cidade_text, lat, lon, descricao)
                st.success(f"Local inserido: {inserted_id}")
            except Exception as e:
                st.error(f"Erro ao inserir local no MongoDB: {e}")

st.header("3) Consultar locais por cidade")
if cidades:
    cidade_consulta = st.selectbox("Cidade para consultar", [c['cidade'] for c in cidades], key="consulta")
    if st.button("Buscar locais"):
        locais = dbm.buscar_locais_por_cidade(cidade_consulta)
        st.write(f"Encontrados {len(locais)} locais em {cidade_consulta}")
        if locais:
            df = pd.DataFrame([{
                "nome_local": l["nome_local"],
                "descricao": l.get("descricao",""),
                "lat": l["coordenadas"]["coordinates"][1],
                "lon": l["coordenadas"]["coordinates"][0]
            } for l in locais])
            st.dataframe(df)
            st.map(df[["lat","lon"]])
else:
    st.info("Nenhuma cidade cadastrada ainda.")

st.header("4) Buscar locais por proximidade (a partir de uma coordenada)")
orig_lat = st.number_input("Origem - latitude", key="orig_lat", value=-7.11532, format="%.6f")
orig_lon = st.number_input("Origem - longitude", key="orig_lon", value=-34.861, format="%.6f")
raio_km = st.number_input("Raio (km)", value=10.0)
if st.button("Buscar próximos"):
    try:
        locais_prox = dbm.buscar_locais_proximos_geo(orig_lat, orig_lon, raio_km)
    except Exception:
        st.warning("Consulta geoespacial falhou — usando fallback (cálculo local).")
        locais_prox = dbm.buscar_locais_proximos_fallback(orig_lat, orig_lon, raio_km)

    st.write(f"{len(locais_prox)} locais dentro de {raio_km} km")
    if locais_prox:
        df2 = pd.DataFrame([{
            "nome_local": l["nome_local"],
            "dist_km": round(l.get("_dist_km", 0), 3) if "_dist_km" in l else None,
            "lat": l["coordenadas"]["coordinates"][1],
            "lon": l["coordenadas"]["coordinates"][0]
        } for l in locais_prox])
        st.dataframe(df2)
        st.map(df2[["lat","lon"]])
