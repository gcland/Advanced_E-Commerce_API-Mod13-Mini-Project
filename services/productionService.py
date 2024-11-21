from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import db
from models.production import Production
from models.product import Product
from models.schemas.productionSchema import productions_schema

def save(production_data):
    with Session(db.engine) as session:
        with session.begin():
            new_production = Production(product_id=production_data['product_id'], employee_id=production_data['employee_id'], quantity_produced = production_data['quantity_produced'], date_produced = production_data['date_produced'])
            session.add(new_production)
            session.commit()

        session.refresh(new_production)
        return new_production

def get():
    with Session(db.engine) as session:
        with session.begin():
            productions = session.query(Production).all()
            json_productions = productions_schema.jsonify(productions).json
            return json_productions
        
def employee_performance(): 
# Calculates total quantity of products each employee has produced
# Grouped results by employee id
    with Session(db.engine) as session:
        with session.begin():
            statement = session.query(Production.employee_id, func.sum(Production.quantity_produced).label('total_quantity')).group_by(Production.employee_id)
            print(statement)
            results = statement.all()
            return results
        
def total_produced(date): 
# Calculates total quantity of products on specific date
# Grouped results by product_id
    with Session(db.engine) as session:
        with session.begin():
            print('Date for query:', date)
            query = select(Production.product_id.label('product_id'), func.sum(Production.quantity_produced).label('total_produced')).select_from(Production).join(Product).where(Production.date_produced == date).group_by(Production.product_id)
            print(query)
            result = db.session.execute(query).all()
            return result