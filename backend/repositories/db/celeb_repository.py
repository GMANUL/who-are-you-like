from infrastructure.sqlite.connection import sqlite_connection
from persistent.db.celebrity import Celebrity
from sqlalchemy import insert, select, func
from typing import List
from Levenshtein import distance as lev


class CelebRepository:

    def __init__(self) -> None: 
        self.sessionmaker = sqlite_connection()


    async def name_exists(self, celebrity_name: str) -> bool:

        stmt = select(func.count()).where(Celebrity.name.ilike(celebrity_name))
        
        async with self.sessionmaker() as session:
            result = await session.execute(stmt)
            count = result.scalar_one()
        
        return count > 0


    async def put_name(self, celebrity_name: str) -> int:
        
        stmp = insert(Celebrity).values({"name": celebrity_name}).returning(Celebrity.id)

        async with self.sessionmaker() as session:
            result = await session.execute(stmp)
            await session.commit()

            celeb_id = result.scalar_one()
            return celeb_id


    async def get_name(self, celebrity_id: int) -> str | None:

        stmp = select(Celebrity.name).where(Celebrity.id == celebrity_id)

        async with self.sessionmaker() as session:
            resp = await session.execute(stmp)
        
        row = resp.fetchone()
        if row is None:
            return None
        
        return row[0]


    async def name_search(self, search_query: str, max_results: int = 10, max_distance: int = 10) -> List[str]:

        first_letters = search_query[:3].lower()
        stmt = select(Celebrity.name).where(
            func.lower(Celebrity.name).startswith(first_letters)
        ).limit(1000)

        async with self.sessionmaker() as session:
            result = await session.execute(stmt)

        candidates = result.scalars().all()
        
        if not candidates:
            return []
        
        scored = [(name, lev(search_query.lower(), name.lower())) for name in candidates]
        scored.sort(key=lambda x: x[1])
        
        filtered = [name for name, dist in scored if dist <= max_distance]
        
        return filtered[:max_results]
