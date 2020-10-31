import json


class IIngestor:
    def ingest(self, path: str, data_key: str = "data") -> list:
        raise NotImplementedError


class Ingestor:
    def get(ingestion_format: str) -> IIngestor:
        if ingestion_format == "json":
            return JSONIngestor()
        raise NotImplementedError


class JSONIngestor(IIngestor):
    def ingest(self, path: str, data_key: str = "data") -> list:
        with open(path) as json_file:
            loaded = json.load(json_file)
        if data_key:
            return loaded[data_key]
        return loaded
