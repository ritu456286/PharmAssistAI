from src.configs.db_con import SessionLocal, initialize_db
from src.seeders.medicines_seeders import seed_medicines
from src.seeders.alerts_seeders import seed_alerts


initialize_db()


def seed_all():
    session = SessionLocal()
    seed_medicines(session)
    seed_alerts(session)
    print("✅ Seeding Completed Successfully")

if __name__ == "__main__":
    seed_all()