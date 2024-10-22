from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from script import algo
import requests
import os

load_dotenv()
micro_router = APIRouter(prefix="/api")

API = os.environ.get("ETHERSCAN")
PINATA = os.environ.get("JWT")


class SnackBoxRequest(BaseModel):
    upper_sum: int
    main_snacks_amount: int
    sum_of_extras: int
    beverages_amount: int
    tags: list[str] = []
    forbidden_tags: list[str] = []
    max_price_per_snack: int


@micro_router.get("/transactions/{address}&{index}")
def transactions(address: str, index: int):
    API = os.environ.get("ETHERSCAN")
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={API}"

    response = requests.get(url).json()
    result = response["result"]

    transactions = [
        {
            "hash": i["hash"],
            "from": i["from"],
            "to": i["to"],
            "value": f"{i["value"]} wei",
            "gas": f"{i["gas"]} wei",
            "total": len(result),
        }
        for i in result[index : index + 3]
    ]
    return transactions


@micro_router.get("/get_gas")
def get_gas():
    url = (
        f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={API}"
    )

    response = requests.get(url).json()

    result = {
        "SafeGasPrice": response["result"]["SafeGasPrice"],
        "ProposeGasPrice": response["result"]["ProposeGasPrice"],
        "FastGasPrice": response["result"]["FastGasPrice"],
    }

    return result


@micro_router.get("/pinata")
def get_pinata_jwt():
    return PINATA


@micro_router.post("/process_snack_box")
def process_snack_box(request_data: SnackBoxRequest):
    # Преобразование данных в настройки для алгоритма
    settings = {
        "upper_sum": request_data.upper_sum,
        "main_snacks_amount": request_data.main_snacks_amount,
        "sum_of_extras": request_data.sum_of_extras,
        "beverages_amount": request_data.beverages_amount,
        "tags": request_data.tags,
        "forbidden_tags": request_data.forbidden_tags,
        "max_price_per_snack": request_data.max_price_per_snack,
    }

    try:
        # Обработка с помощью функции `algo`
        response = algo(settings=settings)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
