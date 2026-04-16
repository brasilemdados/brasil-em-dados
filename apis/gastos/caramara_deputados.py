from pathlib import Path
import requests


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

        def get_lesgislaturas(self) -> None:
            """Consulta as legislaturas na API e salva os IDs em arquivo CSV.

            O método realiza uma requisição ao endpoint de legislaturas, extrai
            os identificadores retornados em `dados` e os salva no arquivo
            `csv`.

            Raises:
                requests.RequestException: Se ocorrer erro na requisição HTTP.
                OSError: Se ocorrer erro ao criar ou escrever o arquivo.
            """
            uri = f"{url_api}/legislaturas?pagina=1&itens=60"
            local: str = "db/csv/"
            response: dict = requests.get(uri).json()
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as erro:
                raise requests.exceptions.HTTPError(
                    f"Erro na requisição get em: {uri}"
                ) from erro
            ids_deputados: list[int] = [
                deputado["id"] for deputado in response.get("dados", [])
            ]
            try:
                with open(file=f"{local}legislaturas.csv", mode="w") as csv:
                    csv.write(",".join(map(str, ids_deputados)))
            except OSError as erro:
                raise FileNotFoundError(f"Não foi encontrado o {local}") from erro
