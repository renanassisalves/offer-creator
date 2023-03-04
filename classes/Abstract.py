from abc import ABC, abstractmethod


class OfferProvider(ABC):
    @abstractmethod
    def validarMensagem(self):
        pass
    
    @abstractmethod
    def buscarTituloProduto(self):
        pass
    
    @abstractmethod
    def buscarPrecoProduto(self):
        pass
    
    @abstractmethod
    def buscarCodigoProduto(self):
        pass

    @abstractmethod
    def buscarPaginaProduto(self, codigo):
        pass
    