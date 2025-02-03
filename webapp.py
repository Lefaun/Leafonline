import streamlit as st
import pandas as pd
from googlemaps import Client as GoogleMaps
import pydeck as pdk
import os
import os
from googlemaps import Client as GoogleMaps

API_KEY = os.getenv("AIzaSyA_g2SB__pcNFESWTfuO6Ek1xlns9VWrZg")
if not API_KEY:
    raise ValueError("API Key do Google Maps não encontrada! Defina a variável de ambiente 'GOOGLE_MAPS_API_KEY'.")

gmaps = GoogleMaps(API_KEY)

# Simulação de Usuários Cadastrados
USUARIOS = {"admin": "1234", "usuario": "senha123"}

# Login
if "logado" not in st.session_state or not st.session_state["logado"]:
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Entrar"):
        if username in USUARIOS and USUARIOS[username] == password:
            st.session_state["logado"] = True
            st.session_state["usuario"] = username
            st.session_state["carrinho"] = {}
            st.sidebar.success(f"Bem-vindo, {username}!")
            st.experimental_rerun()
        else:
            st.sidebar.error("Usuário ou senha incorretos!")
            st.stop()
else:
    st.sidebar.success(f"Bem-vindo de volta, {st.session_state['usuario']}!")

# Abas do aplicativo
aba = st.sidebar.radio("Escolha uma opção:", ["🗺️ Planejar Rota", "🛍️ Loja Sustentável"])

# Função para calcular rota
def calcular_rota(inicio, destino):
    directions = gmaps.directions(inicio, destino, mode="bicycling")
    rota_coords = []
    for step in directions[0]['legs'][0]['steps']:
        rota_coords.append({
            'lat': step['start_location']['lat'],
            'lon': step['start_location']['lng']
        })
        rota_coords.append({
            'lat': step['end_location']['lat'],
            'lon': step['end_location']['lng']
        })
    return rota_coords

# Aba Planejador de Rota
if aba == "🗺️ Planejar Rota":
    st.title("🚴 Planejador de Rota com Google Maps")
    inicio = st.text_input("Endereço de Partida", "Lisboa, Portugal")
    destino = st.text_input("Endereço de Destino", "Sintra, Portugal")
    
    if st.button("Calcular Rota"):
        if not API_KEY:
            st.error("❌ A API Key do Google Maps não está configurada.")
        else:
            try:
                rota = calcular_rota(inicio, destino)
                if rota:
                    df_rota = pd.DataFrame(rota)

                    # Exibir o mapa com visualização 3D usando pydeck
                    view_state = pdk.ViewState(
                        latitude=df_rota['lat'].mean(),
                        longitude=df_rota['lon'].mean(),
                        zoom=12,
                        pitch=60,  # Inclinação para visão 3D
                        bearing=0
                    )

                    layer = pdk.Layer(
                        'PathLayer',
                        data=df_rota,
                        get_path='[["lat", "lon"]]',
                        get_color=[0, 100, 200],
                        width_scale=5,
                        width_min_pixels=3,
                        rounded=True
                    )

                    st.pydeck_chart(pdk.Deck(
                        map_style='mapbox://styles/mapbox/satellite-streets-v11',  # Visão de satélite com ruas
                        initial_view_state=view_state,
                        layers=[layer]
                    ))

                    st.success("Rota calculada e exibida com sucesso!")
                else:
                    st.warning("⚠️ Nenhuma rota encontrada para os endereços fornecidos.")
            except Exception as e:
                st.error(f"Erro ao calcular a rota: {e}")

# Aba Loja Sustentável
elif aba == "🛍️ Loja Sustentável":
    st.title("🛍️ Loja Sustentável")

    # Lista de produtos
    produtos = [
        {"nome": "Cesta Orgânica", "preco": 12.99, "img": "https://via.placeholder.com/150"},
        {"nome": "Sabonete Natural", "preco": 7.50, "img": "https://via.placeholder.com/150"},
        {"nome": "Bolsa Ecológica", "preco": 15.00, "img": "https://via.placeholder.com/150"},
        {"nome": "Kit Bambu", "preco": 9.99, "img": "https://via.placeholder.com/150"},
        {"nome": "Mel Orgânico", "preco": 18.50, "img": "https://via.placeholder.com/150"},
        {"nome": "Horta Caseira", "preco": 25.00, "img": "https://via.placeholder.com/150"},
        {"nome": "Cosméticos Naturais", "preco": 19.99, "img": "https://via.placeholder.com/150"},
        {"nome": "Chá Artesanal", "preco": 10.99, "img": "https://via.placeholder.com/150"},
        {"nome": "Velas Ecológicas", "preco": 14.50, "img": "https://via.placeholder.com/150"},
    ]

    # Inicializar carrinho
    st.session_state.setdefault("carrinho", {})

    def adicionar_ao_carrinho(produto):
        if produto in st.session_state["carrinho"]:
            st.session_state["carrinho"][produto] += 1
        else:
            st.session_state["carrinho"][produto] = 1

    cols = st.columns(3)

    for i, produto in enumerate(produtos):
        with cols[i % 3]:
            st.image(produto["img"], caption=produto["nome"])
            st.write(f"💲 {produto['preco']:.2f}")
            if st.button(f"🛒 Adicionar {produto['nome']}", key=produto["nome"]):
                adicionar_ao_carrinho(produto["nome"])
                st.success(f"{produto['nome']} adicionado ao carrinho!")

    # Exibir Carrinho
    st.sidebar.title("🛒 Carrinho de Compras")
    if st.session_state["carrinho"]:
        total = 0
        pedido = ""
        for item, qtd in st.session_state["carrinho"].items():
            preco = next(p["preco"] for p in produtos if p["nome"] == item)
            subtotal = preco * qtd
            total += subtotal
            pedido += f"{item} ({qtd}x) - 💲{subtotal:.2f}\n"
            st.sidebar.write(f"{item} ({qtd}x) - 💲{subtotal:.2f}")

        st.sidebar.write(f"**Total: 💲{total:.2f}**")

        endereco = st.sidebar.text_input("📍 Endereço de Entrega")
        pagamento = st.sidebar.selectbox("💳 Forma de Pagamento", ["Transferência Bancária", "MB Way", "PayPal"])

        if st.sidebar.button("✅ Finalizar Pedido"):
            if endereco:
                st.sidebar.success("Pedido realizado com sucesso! 📩")
                st.session_state["carrinho"] = {}
            else:
                st.sidebar.error("❌ Informe um endereço de entrega.")
    else:
        st.sidebar.write("Seu carrinho está vazio.")

