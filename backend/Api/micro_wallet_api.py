from dotenv import load_dotenv
from fastapi import APIRouter
from web3 import Web3
import requests
import os

load_dotenv()
micro_router = APIRouter(prefix="/api")

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


@micro_router.get("/get_gas")
def get_gas():
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={API}"

    response = requests.get(url).json()

    result = {
        "SafeGasPrice":response['result']['SafeGasPrice'],
        "ProposeGasPrice":response['result']['ProposeGasPrice'],
        "FastGasPrice":response['result']['FastGasPrice']
    }

    return result