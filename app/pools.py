from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3

@dataclass
class Pool:
    id: str
    name: str
    chain: str
    protocol: str
    assets: List[str]
    tvl: float
    apy: float

class PoolsDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.pools = []

    def filter_pools(
        self,
        chain: Optional[str] = None,
        asset: Optional[str] = None,
        min_tvl: Optional[float] = None,
        max_tvl: Optional[float] = None,
        min_apy: Optional[float] = None,
    ) -> List[Pool]:
        filtered_pools = self.pools

        if chain:
            filtered_pools = [p for p in filtered_pools if p.chain.lower() == chain.lower()]

        if asset:
            filtered_pools = [
                p for p in filtered_pools if asset.lower() in [a.lower() for a in p.assets]
            ]

        if min_tvl is not None:
            filtered_pools = [p for p in filtered_pools if p.tvl >= min_tvl]

        if max_tvl is not None:
            filtered_pools = [p for p in filtered_pools if p.tvl <= max_tvl]

        if min_apy is not None:
            filtered_pools = [p for p in filtered_pools if p.apy >= min_apy]

        return filtered_pools

    def close(self):
        self.conn.close()
