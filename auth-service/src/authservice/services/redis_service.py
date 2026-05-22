from redis import Redis

class RedisService(Redis):
    def __init__(self, host: str, port: int, db: int):
        Redis.__init__(self, host=host, port=port, db=db)
