import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.db.database import SessionLocal
from app.models.models import FundMaster, FundNAV
from etl.fetchers.amfi_nav import fetch_amfi_nav_data

def run_etl_pipeline():
    """
    Executes automated ETL pipeline to update NAVs and stock holdings.
    """
    print("Starting Portfolio Intelligence ETL Pipeline...")
    db = SessionLocal()
    
    # 1. Update AMFI NAVs
    nav_data = fetch_amfi_nav_data()
    print(f"Fetched {len(nav_data)} NAV records from AMFI.")
    
    funds = db.query(FundMaster).all()
    updated_count = 0
    
    today = date.today()
    for f in funds:
        if f.scheme_code in nav_data:
            nav_val = nav_data[f.scheme_code]
            # Check if today's entry already exists
            existing = db.query(FundNAV).filter(
                FundNAV.scheme_code == f.scheme_code,
                FundNAV.nav_date == today
            ).first()
            
            if not existing:
                db.add(FundNAV(scheme_code=f.scheme_code, nav_date=today, nav=nav_val))
                updated_count += 1
                
    db.commit()
    db.close()
    print(f"ETL Pipeline completed. Updated {updated_count} fund NAVs for {today}.")

if __name__ == "__main__":
    run_etl_pipeline()
