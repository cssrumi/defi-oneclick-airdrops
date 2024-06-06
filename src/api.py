from datetime import datetime
from typing import List, Dict

from cachetools.func import ttl_cache
import requests

from record import Record
from serializer import Serializer


class API:
    _API_FIND_ALL_URL = 'https://defi.oneclick.fi/api/v2/airdrops?query=&sort=tier&order=desc&page=1&limit=0'

    @ttl_cache(maxsize=1, ttl=10 * 60)
    @staticmethod
    def all() -> dict:
        return requests.get(API._API_FIND_ALL_URL).json()

    @staticmethod
    def items() -> dict:
        return API.all()['items']

    @staticmethod
    def chains() -> dict:
        return API.all()['chains']

    @staticmethod
    def protocols() -> dict:
        return API.all()['protocols']

    @staticmethod
    def total() -> int:
        return API.all()['total']


class DefiOneclickAirdropsService:

    def __init__(self, serializer: Serializer):
        self.__chains = self._create_chains_map()
        self.__protocols = self._create_protocols_map()
        self.__serializer = serializer

    @staticmethod
    def _create_chains_map() -> Dict[str, str]:
        return {item['id']: item['name'] for item in API.chains()}

    @staticmethod
    def _create_protocols_map() -> Dict[str, str]:
        return {item['id']: item['name'] for item in API.protocols()}

    def _map_record(self, item: dict) -> Record:
        project = item['name']
        tier = item['tier']
        status = item['status']
        tasks = item['tasksCount']
        funding = item['funding']
        category = item['type']['name'] if item['type'] else None
        listed = datetime.fromisoformat(item['createdAt'])
        updated = datetime.fromisoformat(item['updatedAt'])
        chains = [self.__chains[chain_id] for chain_id in item['chains']]
        protocols = [self.__protocols[protocol_id] for protocol_id in item['protocols']]
        return Record(project, tier, status, tasks, funding, category, listed, updated, chains, protocols)

    def _get_records(self) -> List[Record]:
        return [self._map_record(item) for item in API.items()]

    def create_excel_file(self):
        records = self._get_records()
        self.__serializer.to_excel(records)
