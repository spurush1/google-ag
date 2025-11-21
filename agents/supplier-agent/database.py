import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/supplier_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    pestel_data = Column(JSON, nullable=True) # Stores the full PESTEL report
    risk_score = Column(Integer, nullable=True) # 0-100 score
    last_updated = Column(DateTime, default=datetime.utcnow)

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)  # "Engine Component", "Brake System", etc.
    typical_oem_status = Column(String)  # "OEM", "Aftermarket", "Both"
    primary_supplier = Column(String)
    average_price_usd = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    seed_suppliers()
    seed_materials()

def seed_suppliers():
    """Seed supplier data matching Neo4j BOM database"""
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Supplier).count() > 0:
        print("Suppliers already seeded, skipping...")
        db.close()
        return
    
    suppliers_data = [
        # Japanese Suppliers
        {"name": "Denso", "country": "Japan", "risk_score": 15},
        {"name": "Aisin", "country": "Japan", "risk_score": 18},
        {"name": "Toyota Tsusho", "country": "Japan", "risk_score": 20},
        {"name": "NSK", "country": "Japan", "risk_score": 16},
        {"name": "NGK Spark Plugs", "country": "Japan", "risk_score": 14},
        {"name": "Koyo Seiko", "country": "Japan", "risk_score": 19},
        {"name": "NTN Corporation", "country": "Japan", "risk_score": 17},
        
        # German Suppliers
        {"name": "Bosch", "country": "Germany", "risk_score": 22},
        {"name": "Continental AG", "country": "Germany", "risk_score": 24},
        {"name": "ZF Friedrichshafen", "country": "Germany", "risk_score": 23},
        {"name": "Mahle", "country": "Germany", "risk_score": 21},
        {"name": "Schaeffler Group", "country": "Germany", "risk_score": 25},
        
        # American Suppliers
        {"name": "Delphi Technologies", "country": "USA", "risk_score": 28},
        {"name": "BorgWarner", "country": "USA", "risk_score": 26},
        {"name": "Tenneco", "country": "USA", "risk_score": 30},
        {"name": "Dana Incorporated", "country": "USA", "risk_score": 27},
        {"name": "Lear Corporation", "country": "USA", "risk_score": 29},
        {"name": "Aptiv", "country": "USA", "risk_score": 25},
        
        # Other International Suppliers
        {"name": "Magna International", "country": "Canada", "risk_score": 20},
        {"name": "Valeo", "country": "France", "risk_score": 26},
        {"name": "Faurecia", "country": "France", "risk_score": 28},
        {"name": "Hyundai Mobis", "country": "South Korea", "risk_score": 22},
    ]
    
    for supplier_data in suppliers_data:
        supplier = Supplier(**supplier_data)
        db.add(supplier)
    
    db.commit()
    print(f"✅ Seeded {len(suppliers_data)} suppliers to Postgres")
    db.close()

def seed_materials():
    """Seed materials/parts data"""
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Material).count() > 0:
        print("Materials already seeded, skipping...")
        db.close()
        return
    
    materials_data = [
        # Engine Components
        {"name": "Piston Assembly", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "Denso", "average_price_usd": 45.0},
        {"name": "Spark Plug", "category": "Engine Component", "typical_oem_status": "Both", "primary_supplier": "NGK Spark Plugs", "average_price_usd": 12.0},
        {"name": "Fuel Injector", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "Bosch", "average_price_usd": 85.0},
        {"name": "Crankshaft", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "Denso", "average_price_usd": 450.0},
        {"name": "Camshaft", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "Aisin", "average_price_usd": 320.0},
        {"name": "Timing Chain", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "Aisin", "average_price_usd": 95.0},
        {"name": "Oil Pump", "category": "Engine Component", "typical_oem_status": "Both", "primary_supplier": "Aisin", "average_price_usd": 120.0},
        {"name": "Turbocharger", "category": "Engine Component", "typical_oem_status": "OEM", "primary_supplier": "BorgWarner", "average_price_usd": 1200.0},
        {"name": "Intercooler", "category": "Engine Component", "typical_oem_status": "Both", "primary_supplier": "Denso", "average_price_usd": 350.0},
        
        # Transmission Components
        {"name": "Torque Converter", "category": "Transmission Component", "typical_oem_status": "OEM", "primary_supplier": "Aisin", "average_price_usd": 450.0},
        {"name": "Clutch Plate", "category": "Transmission Component", "typical_oem_status": "Both", "primary_supplier": "Aisin", "average_price_usd": 180.0},
        {"name": "Gearbox Housing", "category": "Transmission Component", "typical_oem_status": "OEM", "primary_supplier": "Magna International", "average_price_usd": 850.0},
        {"name": "Transmission Fluid", "category": "Transmission Component", "typical_oem_status": "Both", "primary_supplier": "Aisin", "average_price_usd": 25.0},
        
        # Brake System
        {"name": "Brake Disc Rotor", "category": "Brake System", "typical_oem_status": "Both", "primary_supplier": "Continental AG", "average_price_usd": 65.0},
        {"name": "Brake Pad", "category": "Brake System", "typical_oem_status": "Both", "primary_supplier": "Bosch", "average_price_usd": 45.0},
        {"name": "Brake Caliper", "category": "Brake System", "typical_oem_status": "OEM", "primary_supplier": "Continental AG", "average_price_usd": 180.0},
        {"name": "ABS Control Module", "category": "Brake System", "typical_oem_status": "OEM", "primary_supplier": "Bosch", "average_price_usd": 420.0},
        {"name": "Brake Master Cylinder", "category": "Brake System", "typical_oem_status": "OEM", "primary_supplier": "Bosch", "average_price_usd": 150.0},
        
        # Suspension
        {"name": "Shock Absorber", "category": "Suspension", "typical_oem_status": "Both", "primary_supplier": "ZF Friedrichshafen", "average_price_usd": 95.0},
        {"name": "Coil Spring", "category": "Suspension", "typical_oem_status": "Both", "primary_supplier": "Mubea", "average_price_usd": 55.0},
        {"name": "Control Arm", "category": "Suspension", "typical_oem_status": "OEM", "primary_supplier": "Magna International", "average_price_usd": 120.0},
        {"name": "Ball Joint", "category": "Suspension", "typical_oem_status": "Both", "primary_supplier": "NSK", "average_price_usd": 35.0},
        {"name": "Sway Bar", "category": "Suspension", "typical_oem_status": "OEM", "primary_supplier": "ZF Friedrichshafen", "average_price_usd": 85.0},
        
        # Electrical
        {"name": "Battery 12V", "category": "Electrical", "typical_oem_status": "Both", "primary_supplier": "Delphi Technologies", "average_price_usd": 180.0},
        {"name": "Alternator", "category": "Electrical", "typical_oem_status": "Both", "primary_supplier": "Denso", "average_price_usd": 280.0},
        {"name": "Starter Motor", "category": "Electrical", "typical_oem_status": "Both", "primary_supplier": "Bosch", "average_price_usd": 220.0},
        {"name": "Engine Control Unit (ECU)", "category": "Electrical", "typical_oem_status": "OEM", "primary_supplier": "Denso", "average_price_usd": 650.0},
        {"name": "Wiring Harness", "category": "Electrical", "typical_oem_status": "OEM", "primary_supplier": "Lear Corporation", "average_price_usd": 320.0},
        
        # Other Components
        {"name": "Alloy Wheel 18in", "category": "Wheels & Tires", "typical_oem_status": "Both", "primary_supplier": "Alcoa", "average_price_usd": 250.0},
        {"name": "Tire 225/50R18", "category": "Wheels & Tires", "typical_oem_status": "Aftermarket", "primary_supplier": "Michelin", "average_price_usd": 180.0},
        {"name": "Radiator", "category": "Cooling System", "typical_oem_status": "Both", "primary_supplier": "Denso", "average_price_usd": 220.0},
        {"name": "AC Compressor", "category": "Climate Control", "typical_oem_status": "OEM", "primary_supplier": "Denso", "average_price_usd": 380.0},
        {"name": "Fuel Pump", "category": "Fuel System", "typical_oem_status": "Both", "primary_supplier": "Bosch", "average_price_usd": 140.0},
        {"name": "Exhaust Manifold", "category": "Exhaust System", "typical_oem_status": "OEM", "primary_supplier": "Faurecia", "average_price_usd": 280.0},
        {"name": "Catalytic Converter", "category": "Exhaust System", "typical_oem_status": "OEM", "primary_supplier": "Tenneco", "average_price_usd": 520.0},
        {"name": "Muffler", "category": "Exhaust System", "typical_oem_status": "Both", "primary_supplier": "Tenneco", "average_price_usd": 180.0},
        {"name": "LED Headlight Assembly", "category": "Lighting", "typical_oem_status": "OEM", "primary_supplier": "Valeo", "average_price_usd": 450.0},
        {"name": "LED Taillight Assembly", "category": "Lighting", "typical_oem_status": "OEM", "primary_supplier": "Valeo", "average_price_usd": 320.0},
    ]
    
    for material_data in materials_data:
        material = Material(**material_data)
        db.add(material)
    
    db.commit()
    print(f"✅ Seeded {len(materials_data)} materials to Postgres")
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
