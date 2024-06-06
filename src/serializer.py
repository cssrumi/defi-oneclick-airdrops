import datetime
from typing import List

import pandas as pd

from record import Record


class Serializer:

    @classmethod
    def to_excel(cls, records: List[Record], sheet='sheet', filename=None):
        raise NotImplementedError()

    @classmethod
    def default_file_name(cls) -> str:
        return 'defi-oneclick-airdrops-' + datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S") + '.xlsx'

    @staticmethod
    def default() -> 'Serializer':
        return PandasSerializer()


class PandasSerializer(Serializer):
    __FIELDS = list(Record.__dict__['__annotations__'].keys())

    @staticmethod
    def _to_data_frame(records: List[Record]) -> pd.DataFrame:
        data = [PandasSerializer._map_record(record) for record in records]
        df = pd.DataFrame(data, columns=PandasSerializer.__FIELDS)
        date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
        for date_column in date_columns:
            df[date_column] = df[date_column].dt.date
        return df

    @staticmethod
    def _map_record(record: Record):
        return [record.__getattribute__(field) for field in PandasSerializer.__FIELDS]

    @classmethod
    def to_excel(cls, records: List[Record], sheet='sheet', filename=None):
        filename = filename if filename else cls.default_file_name()
        df = cls._to_data_frame(records)
        df.to_excel(filename, sheet_name=sheet, index=False)
