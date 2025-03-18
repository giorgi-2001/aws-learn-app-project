from sqlalchemy import select, delete, update, desc

from .models import Image
from .database import SessionLocal as session_maker


class ImageDAO:
    @classmethod
    async def get_all_images(cls, **filters):
        async with session_maker() as session:
            statement = select(Image).filter_by(**filters).order_by(desc(Image.created_at))
            result = await session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def get_image_by_name(cls, name: str):
        async with session_maker() as session:
            statement = select(Image).where(Image.name == name)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
        
    @classmethod
    async def save_image(cls, img_data: dict):
        async with session_maker() as session:
            async with session.begin():
                new_img = Image(**img_data)
                session.add(new_img)
                await session.commit()
            return img_data["name"]
        
    @classmethod
    async def update_image(cls, img_data: dict):
        async with session_maker() as session:
            async with session.begin():
                statement = (
                    update(Image)
                    .where(Image.name == img_data["name"])
                    .values(img_data)
                )
                await session.execute(statement)
                await session.commit()
            return img_data["name"]

    @classmethod
    async def delete_image(cls, img_name: str):
        async with session_maker() as session:
            async with session.begin():
                statement = (
                    delete(Image)
                    .where(Image.name == img_name)
                )
                await session.execute(statement)
                await session.commit()
            return img_name
