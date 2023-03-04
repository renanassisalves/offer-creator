import os
import random
import textwrap

import moviepy.editor as mpy
import numpy as np
import tweepy
from PIL import Image, ImageDraw, ImageFont
from cuttpy import Cuttpy
from instagrapi import Client
from telethon import functions
from telethon.sync import TelegramClient

from config import *


def buscarInfosChatsDisponiveis(api_id, api_hash):
    with TelegramClient('name', api_id, api_hash) as client:
        result = client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer='username',
            limit=500,
            hash=0
        ))

        for chat in result.chats:
            print(chat)


def recortarImagem(imagem):
    threshold = 100
    dist = 10
    img = imagem.convert('RGBA')
    # np.asarray(img) is read only. Wrap it in np.array to make it modifiable.
    arr = np.array(np.asarray(img))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = ((r > threshold)
            & (g > threshold)
            & (b > threshold)
            & (np.abs(r - g) < dist)
            & (np.abs(r - b) < dist)
            & (np.abs(g - b) < dist)
            )
    arr[mask, 3] = 0
    img = Image.fromarray(arr, mode='RGBA')
    return img


def arredondarBordas(imagem, raio):
    circle = Image.new('L', (raio * 2, raio * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, raio * 2, raio * 2), fill=255)
    alpha = Image.new('L', imagem.size, 255)
    w, h = imagem.size
    alpha.paste(circle.crop((0, 0, raio, raio)), (0, 0))
    alpha.paste(circle.crop((0, raio, raio, raio * 2)), (0, h - raio))
    alpha.paste(circle.crop((raio, 0, raio * 2, raio)), (w - raio, 0))
    alpha.paste(circle.crop((raio, raio, raio * 2, raio * 2)), (w - raio, h - raio))
    imagem.putalpha(alpha)
    return imagem


def removerCodigoTexto(texto):
    split = texto.split("\n")
    textoFinal = ""
    for linha in split:
        if "Código" in linha:
            pass
        elif "CÓDIGO" in linha:
            pass
        elif "CÓdigo" in linha:
            pass
        elif "CÓDigo" in linha:
            pass
        elif "CÓDIgo" in linha:
            pass
        elif "CÓDIGo" in linha:
            pass
        else:
            textoFinal += linha + "\n"

    return textoFinal


def gerarImagemAnuncio(idMensagem, titulo, preco):
    listaFundos = os.listdir(f"./fundos/")
    numeroRandom = random.randint(0, len(listaFundos) - 1)

    fundo = Image.open(f'./fundos/{listaFundos[numeroRandom]}')
    imagemProduto = Image.open(f'./imagens/{idMensagem}.jpg')
    larguraImagemProduto, alturaImagemProduto = imagemProduto.size

    dimensaoQuadradoToleravel = 617
    if larguraImagemProduto > dimensaoQuadradoToleravel or alturaImagemProduto > dimensaoQuadradoToleravel:
        if larguraImagemProduto / dimensaoQuadradoToleravel > alturaImagemProduto / dimensaoQuadradoToleravel:
            fatorResize = dimensaoQuadradoToleravel / larguraImagemProduto
        else:
            fatorResize = dimensaoQuadradoToleravel / alturaImagemProduto
        imagemProduto = imagemProduto.resize(
            (int(larguraImagemProduto * fatorResize), int(alturaImagemProduto * fatorResize)))

    imagemProduto = arredondarBordas(imagemProduto, round(larguraImagemProduto * 0.1))
    mockup = Image.open(f'./image_schemas/schema_instagram_feito.png')
    bolota = Image.open(f'./image_schemas/bolota_preco.png')
    resultado = Image.open(f'./image_schemas/schema_instagram_feito.png')

    larguraResultado, alturaResultado = resultado.size
    larguraFundo, alturaFundo = fundo.size
    larguraImagemProduto, alturaImagemProduto = imagemProduto.size
    larguraMockup, alturaMockup = mockup.size
    larguraBolota, alturaBolota = bolota.size

    if larguraResultado > fundo.width or alturaResultado > fundo.height:
        if larguraResultado / fundo.width > alturaResultado / fundo.height:
            fatorResize = larguraResultado / fundo.width
        else:
            fatorResize = alturaResultado / fundo.height
        fundo = fundo.resize(
            (int(larguraFundo * fatorResize), int(alturaFundo * fatorResize)))
        larguraFundo, alturaFundo = fundo.size

    resultado.paste(fundo, (
        int(larguraResultado) - int(larguraFundo), (int(alturaResultado) - int(alturaFundo))))

    resultado.paste(mockup, (
        int(larguraResultado) - int(larguraMockup), (int(alturaResultado) - int(alturaMockup))), mask=mockup)

    fatorResize = 0.75
    imagemProduto = imagemProduto.resize(
        (int(larguraImagemProduto * fatorResize), int(alturaImagemProduto * fatorResize)))
    larguraImagemProduto, alturaImagemProduto = imagemProduto.size

    resultado.paste(imagemProduto, (
        int(larguraResultado / 2) - int(larguraImagemProduto / 2),
        (int(alturaResultado / 2.2)) - int(alturaImagemProduto / 2)),
                    mask=imagemProduto)

    resultado.paste(bolota, (
        int(larguraResultado) - int(larguraMockup), (int(alturaResultado) - int(alturaMockup))), mask=bolota)
    # enhance = ImageEnhance.Brightness(resultado)
    # resultado = enhance.enhance(0.7)

    fonteTitulo = ImageFont.truetype('./fontes/Insanibu.ttf', 70)
    fontePrecoCortado = ImageFont.truetype('./fontes/Insanibu.ttf', 30)
    fontePreco = ImageFont.truetype('./fontes/Insanibu.ttf', 50)

    precoCortado = f'{(preco * 1.2):,.2f}'
    precoFinal = f'{preco:,.2f}'

    textoPrecoCortado = f"De  R${precoCortado}      Por:"
    textoPreco = f"R${precoFinal} à vista"
    textoTitulo = titulo[:55]
    resultadoEditavel = ImageDraw.Draw(resultado)

    x = int(larguraResultado / 5)
    y = 60

    for line in textwrap.wrap(textoTitulo, width=20):
        resultadoEditavel.text((x, y), line, font=fonteTitulo, fill="#fd6803", stroke_fill="#000000", stroke_width=6)
        y += 70

    resultadoEditavel.text((int(larguraResultado * 0.10), 600), textoPrecoCortado, font=fontePrecoCortado,
                           fill="#FFFFFF", stroke_fill="#00FF00", stroke_width=2)

    shape = [(int(larguraResultado * 0.14), 618), (int(larguraResultado * 0.29), 622)]
    resultadoEditavel.rectangle(shape, fill="#00FF00")

    resultadoEditavel.text((int(larguraResultado * 0.05), 650), textoPreco, font=fontePreco,
                           fill="#fd6803", stroke_fill="#FFFFFF", stroke_width=4)

    resultado = resultado.convert('RGB')
    resultado.save(f'./resultados/{idMensagem}.jpg', quality=95)


def uparInstagram(nomeArquivoImagem, titulo):
    print("Enviando anúncio para o Instagram...\n")
    cliente = Client()
    cliente.login(loginInstagram, senhaInstagram)
    media = cliente.photo_upload(
        f"./resultados/{nomeArquivoImagem}", titulo,
        extra_data={
            "custom_accessibility_caption": "Promoção",
            "like_and_view_counts_disabled": 0,
            "disable_comments": 0,
        }
    )


def uparTwitter(nomeArquivoImagem, mensagem):
    print("Enviando anúncio para o Twitter...\n")
    auth = tweepy.OAuth1UserHandler(consumerKeyTwitter, consumerKeySecretTwitter,
                                    accessTokenTwitter, accessTokenSecretTwitter)
    api = tweepy.API(auth)

    api.update_status_with_media(mensagem[:270], filename=f"./resultados/{nomeArquivoImagem}")


def gerarVideoYoutube():
    try:
        os.remove(diretorioVideo)
    except:
        pass
    clip = mpy.ImageSequenceClip("./resultados/", fps=0.40)
    audio = (mpy.AudioFileClip("./sounds/music.mp3")  # or any other format
             .set_duration(clip.duration))
    clip.audio = audio
    clip.write_videofile(diretorioVideo)  # or any other format


def uparVideoYoutube(titulo, descricao):
    print("\nEnviando anúncio para o Youtube...\n")
    os.system(f'python upload_video.py --file="{diretorioVideo}" '
              f'--title="{titulo}" --description="{descricao}" --keywords="promoção, oferta, desconto, cupom, barato" '
              f'--category="22" --privacyStatus="public"')


def encurtarLink(link):
    shortener = Cuttpy(cuttlyApiKey)

    response = shortener.shorten(link)

    return response.shortened_url


def tryCatch(funcao):
    try:
        funcao
    except Exception as e:
        print(f"Erro ao realizar a função {funcao}\nErro: {e}")
        pass
