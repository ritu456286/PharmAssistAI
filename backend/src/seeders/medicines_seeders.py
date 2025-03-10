import os
import pandas as pd
from src.models.db.medicine import Medicine

def seed_medicines(session):
    """Seed the medicines table with data from CSV."""
    
    # Get the absolute path of the project's root directory (PharmAssistAI)
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Construct the correct absolute path to resources/medicines_ds.csv
    csv_file_path = r"C:\Users\Sachin Kansal\Desktop\programs\Projects\Projects_GENAI\PharmAssistAI\resources\medicines_ds.csv"

    # Convert to absolute path (for debugging)
    csv_file_path = os.path.abspath(csv_file_path)

    print(f"📂 Loading CSV from: {csv_file_path}")  # Debugging line

    # Check if file exists
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"🚨 CSV file not found at: {csv_file_path}")

    # Load CSV
    df = pd.read_csv(csv_file_path)
    df["expiry_date"] = pd.to_datetime(df["expiry_date"]).dt.date  # Convert to date object before inserting
    # Select only the top 100 rows
    df_top100 = df.head(300)

    medicines = [
        Medicine(
            name=row["name"],
            dosage=row.get("dosage", ""),
            quantity=row.get("quantity", 0),
            price=row.get("price", 0.0),
            expiry_date=row.get("expiry_date", None)
        )
        for _, row in df_top100.iterrows()
    ]

    session.add_all(medicines)
    session.commit()
    print("✅ Seeded top 100 medicines successfully!")
