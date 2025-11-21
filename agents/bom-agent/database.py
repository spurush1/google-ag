import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

driver = GraphDatabase.driver(URI, auth=AUTH)

def get_db():
    return driver.session()

def seed_bom_data():
    """
    Seeds the Neo4j database with a realistic Car BOM structure.
    """
    cypher_query = """
    MERGE (car:Part {name: "Sedan Car", type: "Product"})
    
    MERGE (engine:Part {name: "V6 Engine", type: "Assembly"})
    MERGE (chassis:Part {name: "Chassis Platform", type: "Assembly"})
    MERGE (transmission:Part {name: "Automatic Transmission", type: "Assembly"})
    MERGE (wheels:Part {name: "Alloy Wheels", type: "Assembly"})
    
    MERGE (car)-[:COMPOSED_OF]->(engine)
    MERGE (car)-[:COMPOSED_OF]->(chassis)
    MERGE (car)-[:COMPOSED_OF]->(transmission)
    MERGE (car)-[:COMPOSED_OF]->(wheels)
    
    // Engine Components
    MERGE (piston:Part {name: "Piston", type: "Component"})
    MERGE (spark_plug:Part {name: "Spark Plug", type: "Component"})
    MERGE (crankshaft:Part {name: "Crankshaft", type: "Component"})
    
    MERGE (engine)-[:COMPOSED_OF]->(piston)
    MERGE (engine)-[:COMPOSED_OF]->(spark_plug)
    MERGE (engine)-[:COMPOSED_OF]->(crankshaft)
    
    // Transmission Components
    MERGE (gearbox:Part {name: "Gearbox Housing", type: "Component"})
    MERGE (clutch:Part {name: "Clutch Plate", type: "Component"})
    
    MERGE (transmission)-[:COMPOSED_OF]->(gearbox)
    MERGE (transmission)-[:COMPOSED_OF]->(clutch)
    
    // Suppliers (Linking to Agent 1 concepts)
    MERGE (bosch:Supplier {name: "Bosch", country: "Germany"})
    MERGE (denso:Supplier {name: "Denso", country: "Japan"})
    MERGE (magna:Supplier {name: "Magna", country: "Canada"})
    
    MERGE (spark_plug)-[:SUPPLIED_BY]->(bosch)
    MERGE (piston)-[:SUPPLIED_BY]->(denso)
    MERGE (gearbox)-[:SUPPLIED_BY]->(magna)
    """
    
    with driver.session() as session:
        try:
            session.run(cypher_query)
            print("BOM Data Seeded Successfully.")
        except Exception as e:
            print(f"Error seeding BOM data: {e}")

def close_db():
    driver.close()
