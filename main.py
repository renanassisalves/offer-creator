import os
import random

from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import scripts
from config import removerImagensPromo, removerResultados
from config import telegram_api_id, telegram_api_hash
from classes.Magalu import Magalu
# Telegram groups ids
grupoMagalu = -1001217820058
idGrupoLMRStore = -1001230943681
grupoTeste = 783296054


with TelegramClient('session', telegram_api_id, telegram_api_hash) as client:
    @client.on(events.NewMessage(chats=[grupoTeste, grupoMagalu]))
    async def handler(event):
        idMensagem = event.message.id
        print(f"\n\n##New message in group #{idMensagem}")
        mensagem = event.message.message
        await event.message.download_media('./imagens/' + str(idMensagem))

        magalu = Magalu(idMensagem, mensagem)

        if magalu.validarMensagem():

            titulo = magalu.buscarTituloProduto()
            preco = magalu.buscarPrecoProduto().replace(".", "").replace(",", ".")
            codigo = magalu.buscarCodigoProduto()
            link = magalu.buscarPaginaProduto(codigo)

            scripts.gerarImagemAnuncio(idMensagem, titulo, float(preco))
            linkEncurtado = scripts.encurtarLink(link)

            mensagem = scripts.removerCodigoTexto(mensagem)

            mensagemTwitter = "PROMOÇÃO!\n\nLINK DIRETO DA PROMOÇÃO: " + linkEncurtado + \
                              "\n\n #Store #promocao #oferta #cupom\n\n" + mensagem

            mensagem = "PROMOÇÃO!\n\nLINK DIRETO DA PROMOÇÃO: " + linkEncurtado + "\n\n" + mensagem

            canalDivulgacao = await client.get_entity(PeerChannel(idGrupoLMRStore))
            print("\nPublicando promoção no grupo do Telegram...")
            await client.send_message(entity=canalDivulgacao, message=mensagem, file=f"./resultados/{idMensagem}.jpg")

            scripts.tryCatch(scripts.uparTwitter(f"{idMensagem}.jpg", mensagemTwitter))

            if int(removerImagensPromo) == 1:
                os.remove(f"./imagens/{idMensagem}.jpg")
            if int(removerResultados) == 1:
                os.remove(f"./resultados/{idMensagem}.jpg")

    client.run_until_disconnected()
