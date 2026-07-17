import dotenv
import os

dotenv.load_dotenv()

class Config:
    def __init__(self):
        self.allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")
        self.database_url = os.getenv("DATABASE_URL")
        self.jwt_secret = os.getenv("JWT_SECRET")
        self.role_name_admin = os.getenv("ROLE_NAME_ADMIN")
        self.role_name_user = os.getenv("ROLE_NAME_USER")
        self.kafka_brokers = os.getenv("KAFKA_BROKERS")
        self.kafka_cluster_id = os.getenv("KAFKA_CLUSTER_ID")
        self.kafka_client_id = os.getenv("KAFKA_CLIENT_ID")
        self.kafka_user_topic = os.getenv("KAFKA_USER_TOPIC")

        self.redis_host = os.getenv("REDIST_HOST")
        self.redis_port = os.getenv("REDIS_PORT")
        self.redis_db = os.getenv("REDIS_DB")

config = Config()
