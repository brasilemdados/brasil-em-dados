import json
from pathlib import Path
import requests
import csv


class InformacoesCamara:
    """Classe responsável por obter e armazenar informações da API da Câmara.

    Esta classe consulta endpoints da API da Câmara dos Deputados e salva
    alguns dados localmente em arquivos CSV.

    Attributes:
        url_api (str): URL base da API da Câmara.
    """

    def __init__(self, url_api: str):
        """Inicializa a classe com a URL base da API.

        Args:
            url_api (str): URL base da API da Câmara dos Deputados.
        """
        if not url_api or not isinstance(url_api, str):
            raise ValueError("url_api deve ser uma string não vazia.")
        self.url_api: str = url_api

    def _legislaturas(self) -> Path:
        """Consulta as legislaturas na API e salva os IDs em arquivo CSV.

        O método realiza uma requisição ao endpoint de legislaturas, extrai
        os identificadores retornados em `dados` e os salva no arquivo
        `csv`.

        Raises:
            requests.RequestException: Se ocorrer erro na requisição HTTP.
            OSError: Se ocorrer erro ao criar ou escrever o arquivo.
        """
        uri = f"{self.url_api}/legislaturas?pagina=1&itens=60"
        local = Path("db/csv")
        local.mkdir(parents=True, exist_ok=True)
        caminho_arquivo: Path = local / "legislaturas.csv"

        try:
            response = requests.get(url=uri, timeout=60)
            response.raise_for_status()

            dados = response.json().get("dados", [])
            ids_legislaturas: list[str] = [
                str(object=item["id"]) for item in dados if "id" in item
            ]

            if not ids_legislaturas:
                print("Aviso: Nenhum dado encontrado na API.")
                return caminho_arquivo

            with open(file=caminho_arquivo, mode="w", encoding="utf-8") as arquuivo:
                arquuivo.write(",".join(ids_legislaturas))

            return caminho_arquivo

        except requests.RequestException as erro:
            raise RuntimeError(f"Erro na comunicação com a API: {erro}")
        except Exception as erro:
            raise RuntimeError(f"Erro inesperado: {erro}")
