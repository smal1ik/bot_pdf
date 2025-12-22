from app.database.models import User, async_session
from sqlalchemy import select, BigInteger, update, delete, func, case, insert, or_


async def add_user(tg_id: BigInteger, first_name: str, username: str, full_name: str, click_id: str):
    """
    Функция добавляет пользователя в БД
    """
    if not click_id:
        click_id = None
    async with async_session() as session:
        session.add(User(
            tg_id=tg_id,
            first_name=first_name,
            username=username,
            full_name=full_name,
            click_id=click_id)
        )
        await session.commit()


async def get_user(tg_id: BigInteger) -> User:
    """
    Получаем пользователя по tg_id
    """
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result


async def user_subscribe(tg_id: BigInteger):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(subscribed=True))
        await session.commit()


async def get_statistics():
    stats = {}
    async with async_session() as session:
        stats['total_users'] = await session.scalar(select(func.count(User.tg_id)))
        stats['total_click_id'] = (await session.execute(
            select(User.click_id, func.count(User.tg_id))
            .where(User.click_id != None)
            .group_by(User.click_id)
            )).fetchall()
        return stats

