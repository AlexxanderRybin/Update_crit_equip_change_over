import psycopg
import pandas as pd
from sqlalchemy import Connection, create_engine, types, text, Engine
from datetime import datetime

if 'psycopg' in globals():
    driver = 'psycopg'
elif 'psycopg2' in globals():
    driver = 'psycopg2'
else:
    driver = None

conn_string = f'postgresql+{driver}://OPF_user:OPFo3o32023@yuzdc1-n-v70419.sakhalin2.ru:5432/ODS'
engine = create_engine(conn_string)
SCHEMA = 'opf_w_db'
PERM_USER = 'TDM_user'
pob_actual_excel = '//sakhalin2.ru/SE/OPF/Dept_02/OPF Operations/AU-OP-2 Maintenance - Integrated Planning/Planning Dept Projects/Проект#4 - График переключений критических агрегатов vs ТОиР/Major Equipment changeover.xlsx'

db_struct = {
    "Visualization": 
    {
        "name": "critical_equipment_changeover",
        "columns_types": {
            "Date": types.Date,
            "tag_name": types.Text,
            "state": types.Text,
        },
    },
}

def update_data(db_struct: dict[str, dict[str, str]], connection: Connection | Engine, schema: str) -> None:
    
    for k, v in db_struct.items():
        print(f'Uploading list "{k}" into table "{v["name"]}"')
        reestr = pd.read_excel(pob_actual_excel, 
                               sheet_name=k, usecols=list(v["columns_types"].keys()), converters=v["converters"] if "converters" in v else None)
        print(reestr)
        reestr.to_sql(v["name"], connection, schema=schema, if_exists='replace', index=False, dtype=v["columns_types"])
        print(f'Uploading of the list "{k}" into table "{v["name"]}" completed')

def grant_sel_permissions(engine: Engine, user: str, db_struct: dict[str, dict[str, str]], schema: str):
    print(f"Granting permissions to Spotfier service-user: {user}:")
    with engine.connect() as connection:
        try:
            for _, table in db_struct.items():
                data = {"schema": str(schema), "table": str(table["name"]), "user": str(user)}
                statement = text('GRANT SELECT ON TABLE :_schema.:_table TO ":_user"')
                __ = connection.execute(statement=statement, parameters={"_schema": data["schema"], "_table": data["table"], "_user": data["user"]})
                print(__)
                print(f"SELECT permissions granted to user {data['user']} for table {data['table']}")
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(e.__traceback__)

if __name__ == '__main__':
    update_data(db_struct=db_struct, connection=engine, schema=SCHEMA)
    grant_sel_permissions(engine=engine, db_struct=db_struct, schema=SCHEMA, user=PERM_USER)
    print('All opeations completed successfully')

