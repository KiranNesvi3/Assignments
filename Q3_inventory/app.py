from fastapi import FastAPI , Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db,init_db,Inventory,Purchase

app = FastAPI()

@app.post("/buy_ticket")
def buy_ticket(db:Session = Depends(get_db)):
    try:
        item = db.query(Inventory).filter(Inventory.id ==1).with_for_update().first()
        if not item:
            raise HTTPException(status_code=404,detail="Item not found")
        if item.count>0:
            item.count-=1
            purchase = Purchase(item_id=1,timestamp=datetime.utcnow())
            db.add(purchase)
            db.commit()
            return {"status:","success","remaining:",item.count}
        else:
            db.rollback()
            raise HTTPException(status_code=410,detail="sold out")
    except Exception as e:
        db.rollback()
        if isinstance(e,HTTPException):
            raise e
        print(f"Error:{e}")
        raise HTTPException(status_code=500,detail="internal server error")

