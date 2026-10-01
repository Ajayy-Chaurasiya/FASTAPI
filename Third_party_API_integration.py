from fastapi import FastAPI
import requests

app=FastAPI()


@app.get("/weather")
def get_weather():
    url="https://api.weatherapi.com/v1/current.json"
    #Your FastAPI application sends a GET request to the third-party API.
   
    params={
        "key":"0bba052d14ef4cb387f45942260110",
        "q":"Birgunj"
    }
    
    response=requests.get(url,params=params)
    data=response.json()
    #The response is converted from JSON → Python data (usually a dictionary).
    return data

