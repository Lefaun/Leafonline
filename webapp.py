import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
from googlemaps import Client as GoogleMaps
import time

# Configurar API Key do Google Maps
API_KEY = "AIzaSyDZGdHHwZFKGXMQIy_kkgDv7-oIseNGnsA"
gmaps = GoogleMaps(API_KEY)

# Simulação de Usuários Cadastrados
USUARIOS = {"admin": "1234", "usuario": "senha123"}

# Login
st.sidebar.title("🔑 Login")
username = st.sidebar.text_input("Usuário")
password = st.sidebar.text_input("Senha", type="password")
if st.sidebar.button("Entrar"):
    if username in USUARIOS and USUARIOS[username] == password:
        st.session_state["logado"] = True
        st.session_state["usuario"] = username
        st.session_state["carrinho"] = {}
        st.sidebar.success(f"Bem-vindo, {username}!")
    else:
        st.sidebar.error("Usuário ou senha incorretos!")
        st.stop()

# Verifica login
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.stop()

# Criando abas
aba = st.sidebar.radio("Escolha uma opção:", ["🗺️ Planejar Rota", "🛍️ Loja Sustentável"])

# Planejador de Rota com Google Maps
def calcular_rota(inicio, destino):
    directions = gmaps.directions(inicio, destino, mode="bicycling")
    rota_coords = []
    for step in directions[0]['legs'][0]['steps']:
        rota_coords.append((step['start_location']['lat'], step['start_location']['lng']))
        rota_coords.append((step['end_location']['lat'], step['end_location']['lng']))
    return rota_coords

if aba == "🗺️ Planejar Rota":
    st.title("🚴 Planejador de Rota com Google Maps")
    inicio = st.text_input("Endereço de Partida", "Lisboa, Portugal")
    destino = st.text_input("Endereço de Destino", "Sintra, Portugal")
    if st.button("Calcular Rota"):
        try:
            rota = calcular_rota(inicio, destino)
            st.map(pd.DataFrame(rota, columns=['lat', 'lon']))
        except Exception as e:
            st.error(f"Erro ao calcular a rota: {e}")

with tabs[1]:  # Correção da posição da aba Loja Online
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

    cols = st.columns(3)  # Ajusta a disposição dos produtos

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
        for item, qtd in st.session_state["carrinho"].items():
            preco = next(p["preco"] for p in produtos if p["nome"] == item)
            subtotal = preco * qtd
            total += subtotal
            st.sidebar.write(f"{item} ({qtd}x) - 💲{subtotal:.2f}")

        st.sidebar.write(f"**Total: 💲{total:.2f}**")
        if st.sidebar.button("✅ Finalizar Pedido"):
            st.sidebar.success("Pedido realizado com sucesso! 🌱")
            st.session_state["carrinho"] = {}
    else:
        st.sidebar.write("Seu carrinho está vazio.")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Função para enviar o e-mail
def enviar_email(pedido, total):
    remetente = "seuemail@gmail.com"  # Substitua pelo seu e-mail
    senha = "suasenha"  # Use senha do app se necessário (não use senhas reais diretamente no código)
    destinatario = "seuemail@gmail.com"  # E-mail para onde o pedido será enviado

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Novo Pedido - Loja Sustentável"

    corpo_email = f"""
    Novo pedido recebido! 🛍️

    Produtos:
    {pedido}

    Total: 💲{total:.2f}

    Forma de pagamento: Transferência bancária / MB Way / PayPal
    Endereço de entrega: [Preencher com o endereço do cliente]

    Obrigado por sua compra! 🌱
    """

    msg.attach(MIMEText(corpo_email, "plain"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        return False


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Configuração do e-mail
EMAIL_REMETENTE = "seuemail@gmail.com"  # Substitua pelo seu e-mail
SENHA_EMAIL = "suasenha"  # Use uma senha de aplicativo para maior segurança
EMAIL_DESTINATARIO = "seuemail@gmail.com"  # Para onde o pedido será enviado
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587

def enviar_email(pedido, total, endereco, pagamento):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO
    msg["Subject"] = "Novo Pedido - Loja Sustentável"

    corpo_email = f"""
    🛍️ Novo pedido recebido!

    Produtos:
    {pedido}

    Total: 💲{total:.2f}

    Forma de pagamento: {pagamento}
    Endereço de entrega: {endereco}

    Obrigado por sua compra! 🌱
    """
    msg.attach(MIMEText(corpo_email, "plain"))

    try:
        servidor = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Inicializa o carrinho na sessão
if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = {}


    st.sidebar.title("🛒 Carrinho de Compras")

if st.session_state["carrinho"]:
    total = 0
    pedido = ""
    for item, qtd in st.session_state["carrinho"].items():
        preco = next(p["preco"] for p in produtos if p["nome"] == item)
        subtotal = preco * qtd
        total += subtotal
        pedido += f"{item} ({qtd}x) - 💲{subtotal:.2f}\n"

st.sidebar.write(f"**Total: 💲{total:.2f}**")
endereco = st.sidebar.text_input("📍 Endereço de Entrega")
pagamento = st.sidebar.selectbox("💳 Forma de Pagamento", ["Transferência Bancária", "MB Way", "PayPal"])

if st.sidebar.button("✅ Finalizar Pedido"):
    if endereco:
        if enviar_email(pedido, total, endereco, pagamento):
            st.sidebar.success("Pedido realizado com sucesso! Um e-mail foi enviado. 📩")
            st.session_state["carrinho"] = {}
        else:
            st.sidebar.error("❌ Erro ao enviar e-mail. Tente novamente.")
    else:
        st.sidebar.error("❌ Informe um endereço de entrega.")
else:
    st.sidebar.write("Seu carrinho está vazio.")


#else:
    #st.sidebar.error("❌ Credenciais incorretas")
