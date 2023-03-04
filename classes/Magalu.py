import googleapiclient
import configparser
import re
import requests
from bs4 import BeautifulSoup

from classes.Abstract import OfferProvider


class Magalu(OfferProvider):
    def __init__(self, idMensagem, mensagem):
        self.idMensagem = idMensagem
        self.mensagem = mensagem
        self.titulo = self.buscarTituloProduto()

    def validarMensagem(self):
        # Implementação de validações adicionais
        return True

    def buscarTituloProduto(self):
        try:
            titulo = self.mensagem.split('\n', 1)[0]
            return titulo
        except:
            print("Erro ao buscar título do produto")
            return False

    def buscarPrecoProduto(self):
        try:
            resultado = re.search(r"por\s?R?\$\s?(\d+.?\d+,\d+).*", self.mensagem, re.IGNORECASE)
            return resultado.group(1)
        except:
            print("Erro ao buscar preço do produto")
            return False

    def buscarCodigoProduto(self):
        try:
            resultado = re.search(r"código\s?:\s?(.*)", self.mensagem, re.IGNORECASE)
            return resultado.group(1)
        except:
            print("Erro ao buscar código do produto")
            return False

    def buscarPaginaProduto(self, codigo):
        try:
            __URL = f"https://www.magazinevoce.com.br/magazinelmreletronicos/busca/{codigo}/"
            request = requests.get(__URL)

            soup = BeautifulSoup(request.text, 'html.parser')

            link = soup.find("a", {"class": "g-img-wrapper"})
            link = link.get("href")
        except Exception as e:
            print(f"Erro ao buscar link da loja do produto {self.titulo}:\nErro: {e}")
            return False
        return str("https://www.magazinevoce.com.br" + link)