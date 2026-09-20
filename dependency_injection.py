from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
class order(BaseModel):
    name:str
    employid:int
    password:str

# Reusable authentication .. here function is looking for token i.e mysecrettoken
#header means some more informartion along with request , if header is not given then it is none
def verify_token(token: str = Header(None)):
    if token != "Ajay123":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return "Authorized User"
#if token is given mysecrettoken then he/she is authorized user 

@app.post("/orders")
def create_order(orders:order,user:str=Depends(verify_token)): #depends will automatically use verify_token result
    return {                        #if user = authorized then it will execute otherwise exception   
        "Employee details":orders,
        "message": "Order created",
        "user": user
         }


# GET
@app.get("/profile")
def profile(user=Depends(verify_token)):
    return {
        "method":"Get",
        "user": user
    }


# POST


# PUT
@app.put("/orders/{order_id}")
def update_order(order_id: int, user=Depends(verify_token)):
    return {
        "method": "PUT",
        "order_id": order_id,
        "message": "Order updated",
        "user": user
    }



# DELETE
@app.delete("/orders/{order_id}")
def delete_order(order_id: int, user=Depends(verify_token)):
    return {
        "method": "DELETE",
        "order_id": order_id,
        "message": "Order deleted",
        "user": user
    }