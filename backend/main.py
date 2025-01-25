from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table



app = FastAPI()

# Middleware pro povolení CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Povolit pouze frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapování názvů typů na SQLAlchemy třídy
SQLALCHEMY_TYPES = {
    "Integer": Integer,
    "String": String,
}


# Cesta ke složce s moduly
MODULES_DIR = "modules"

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

# Cesta ke složce s moduly
MODULES_DIR = "modules"

def load_table_definitions():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
        print("Modules directory created.")

    for foldername in os.listdir(MODULES_DIR):
        folder_path = os.path.join(MODULES_DIR, foldername)
        table_path = os.path.join(folder_path, "table.json")
        if os.path.isdir(folder_path):
            print(f"Checking folder: {foldername}")
            if os.path.exists(table_path):
                print(f"Found table configuration: {table_path}")
                with open(table_path, "r") as file:
                    table_config = json.load(file)
                    print(f"Loaded table configuration: {table_config}")

                    # Dynamicky vytvoř tabulku
                    columns = []
                    for col in table_config["columns"]:
                        column_type = SQLALCHEMY_TYPES.get(col["type"])
                        if not column_type:
                            raise ValueError(f"Neznámý typ sloupce: {col['type']}")
                        columns.append(
                            Column(
                                col["name"],
                                column_type,
                                primary_key=col.get("primary_key", False),
                                nullable=col.get("nullable", True),
                            )
                        )
                    table = Table(table_config["table_name"], metadata, *columns)
                    metadata.create_all(bind=engine)
                    print(f"Table {table_config['table_name']} created.")
            else:
                print(f"No table.json found in {foldername}")




@app.on_event("startup")
def startup_event():
    load_table_definitions()


# Funkce pro načtení modulů ze složky
def load_modules_from_folder():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)  # Vytvoří složku, pokud neexistuje

    modules = []
    for foldername in os.listdir(MODULES_DIR):
        folder_path = os.path.join(MODULES_DIR, foldername)
        config_path = os.path.join(folder_path, "config.json")
        if os.path.isdir(folder_path) and os.path.exists(config_path):
            with open(config_path, "r") as file:
                config = json.load(file)
                modules.append({"id": len(modules) + 1, "name": config.get("name", "Unknown")})
    return modules

@app.get("/modules")
def get_modules():
    return load_modules_from_folder()
