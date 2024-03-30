import asyncio
import pandas as pd

from backend.DataBase.database import Database


class ModelInfoDb(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, model: str = None):
        if model:
            model_id = (await self.cursor.execute("SELECT id FROM crane_model WHERE model=(%s)", (model,)))
            await self.cursor.execute("SELECT * FROM model_info WHERE id=(%s)", (model_id,))
        else:
            await self.cursor.execute("SELECT * FROM crane_model "
                                      "LEFT JOIN model_info "
                                      "ON crane_model.id=model_info.model_id")

        data = await self.cursor.fetchall()
        data = pd.DataFrame(data)
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO model_info(model_id, crane_type, load_moment, boom_length, "
                                  "lifting_capacity_max, lifting_capacity_end, height_anker, height_anker_support,"
                                  "height_anker_C38, height_anker_C45, height_anker_C60) "
                                  " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')", values)

    async def delete(self, model: tuple):
        model_id = (await self.cursor.execute("SELECT id FROM crane_model WHERE model=(%s)", (model,)))
        await self.cursor.execute("DELETE FROM model_info WHERE model_id=(%s)", (model_id,))
        await self.cursor.execute("DELETE FROM crane_model WHERE model=(%s)", (model,))

    async def update(self, model: str, values: dict):
        model_id = (await self.cursor.execute("SELECT id FROM crane_model WHERE model=(%s)", (model,)))
        script = "UPDATE model_info SET "
        script += ", ".join([f"{key} = '{value}'" for key, value in values.items()])
        script += f" WHERE model_id = {model_id}"
        await self.cursor.execute(script)


if __name__ == "__main__":
    db = ModelInfoDb()
    res = asyncio.get_event_loop().run_until_complete(db.update(model='test', values={'crane_type': 'value', }))
    print(res)
