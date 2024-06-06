from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Record:
    project: str
    tier: str
    status: str
    tasks: int
    funding: int
    category: str
    listed: datetime
    updated: datetime
    chains: List[str]
    protocols: List[str]