from infrastructure.sqlite.connection import sqlite_connection
from persistent.db.celebrity import Celebrity
from sqlalchemy import insert, select, func
from typing import List

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


    async def name_search(self, search_query: str, max_results: int = 10) -> List[str]:

        stmt = (select(Celebrity.name).where(Celebrity.name.ilike(f"%{search_query}%")).limit(max_results))

        async with self.sessionmaker() as session:
            result = await session.execute(stmt)

        candidates = result.scalars().all()
        return candidates
