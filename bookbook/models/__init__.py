from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from bookbook.config import MONGO_DB_NAME, MONGO_URL


class MongoDB(object):
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(motor_client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결이 되었습니다.")

    def close(self):
        self.client.close()
        print("DB와 연결이 종료되었습니다.")


mongodb = MongoDB()
