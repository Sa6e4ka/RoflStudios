from dotenv import load_dotenv
from fastapi import APIRouter
from web3 import Web3
import requests
import os

load_dotenv()
micro_router = APIRouter()

API = os.environ.get("ETHERSCAN")

@micro_router.get("/transactions/{address}&{index}")
def transactions(address: str, index: int):
    API = os.environ.get("ETHERSCAN")
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={API}"

    response = requests.get(url).json()
    result = response['result']

    transactions = [
        {
            "hash" : i["hash"],
            "from" : i["from"],
            "to" : i["to"],
            "value" : f"{round(Web3.from_wei(int(i["value"]), "ether"), 5)} ETH",
            "gas" : f"{i["gas"]} wei",
            "total" : len(result),
        }
        for i in result[index:index+3]
    ]
    return transactions


