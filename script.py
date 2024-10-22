import json
import random as r
import time
import copy

with open("micro_products.json", "r", encoding="UTF-8") as file:
    data = json.load(file)


def algo(settings: dict) -> dict:
    box = []
    primary_tags = tuple(copy.deepcopy(settings["tags"]))

    def get_snack(
        tag="Любое",
        forbidden_tags=[],
        type="Основной",
        max_price=settings["max_price_per_snack"],
    ):
        r.shuffle(data)

        for snack in data:
            price = float(snack["Цена"].split()[0].strip())
            if price <= max_price:
                if tag in snack["Теги"] or tag == "Любое":
                    if not (set(forbidden_tags) & set(snack["Теги"])):

                        if snack["Тип"] == type:
                            if snack not in box:
                                return snack
        return None

    def find_closest_extras(items, k):

        n = len(items)
        dp = [0] * (k + 1)
        selected_items = [None] * (k + 1)

        for i in range(n):
            name, price = list(items.items())[i]
            for j in range(k, price - 1, -1):
                if dp[j] < dp[j - price] + price:
                    dp[j] = dp[j - price] + price
                    selected_items[j] = name
        closest_sum = max(dp)
        closest_index = dp.index(closest_sum)

        result = []
        while closest_index > 0 and selected_items[closest_index] is not None:
            result.append(selected_items[closest_index])
            closest_index -= items[selected_items[closest_index]]

        return result

    def generate_box(settings=settings):
        global box
        box = []
        main_snacks_amount = settings["main_snacks_amount"]

        bev_amount = settings["beverages_amount"]

        index = 0

        current_sum = 0

        if settings["tags"]:
            settings["tags"].append("Любое")
            available_tags = list(set(settings["tags"]))
            while len(settings["tags"]) < main_snacks_amount:

                tag = available_tags[r.randint(0, len(available_tags) - 1)]

                settings["tags"].append(tag)
        else:
            settings["tags"] = ["Любое"] * main_snacks_amount
        start_time = time.time()
        while main_snacks_amount:
            if time.time() - start_time > 2:

                return False
            snack = get_snack(
                tag=settings["tags"][index],
                forbidden_tags=settings["forbidden_tags"],
                type="Основной",
            )
            if snack:
                box.append(snack)
                main_snacks_amount -= 1
                index += 1
                current_sum += float(snack["Цена"].split()[0].strip())
            else:
                settings["tags"][index % main_snacks_amount] = "Любое"

        for _ in range(bev_amount):
            beverage = get_snack(type="Напиток")
            if beverage:
                box.append(beverage)
                current_sum += float(beverage["Цена"].split()[0].strip())
            else:
                break

        extras = {}
        for ind in range(len(data)):
            if data[ind]["Тип"] == "Дополнительный" and (
                not (set(settings["forbidden_tags"]) & set(data[ind]["Теги"]))
            ):
                extras[ind] = int(data[ind]["Цена"].split()[0].strip())

        k = min(settings["upper_sum"] - current_sum, settings["sum_of_extras"])
        if current_sum > settings["upper_sum"]:
            return False

        extras = find_closest_extras(extras, int(k))

        for sn in extras:
            box.append(data[sn])
            current_sum += float(data[sn]["Цена"].split()[0].strip())

        return box, current_sum

    def main():
        box = generate_box()

        if not box:
            return False

        # Переменные для хранения данных
        main_snacks = []
        extra_snacks = []
        beverages = []
        is_extra = False
        is_beverage = False
        sum_main, sum_bev, sum_extras = 0, 0, 0

        # Обрабатываем содержимое бокса
        for snack in box[0]:
            price = float(snack["Цена"].split()[0].strip())
            snack_info = {
                "name": snack["Название"],
                "price": price,
                "type": snack["Тип"],
            }

            if snack["Тип"] == "Напиток":
                beverages.append(snack_info)
                sum_bev += price
                if not is_beverage:
                    is_beverage = True

            elif snack["Тип"] == "Дополнительный":
                extra_snacks.append(snack_info)
                sum_extras += price
                if not is_extra:
                    is_extra = True

            else:
                main_snacks.append(snack_info)
                sum_main += price

        # Структурируем результат
        response = {
            "main_snacks": main_snacks,
            "extra_snacks": extra_snacks,
            "beverages": beverages,
            "summary": {
                "sum_main": sum_main,
                "sum_beverages": sum_bev,
                "sum_extras": sum_extras,
                "total": box[1],
            },
        }

        return response

    def main_main():
        max_attempts, attempts, success = 25, 0, False

        while not success and attempts < max_attempts:

            success = main()
            if not success:
                box = []
                settings["tags"] = list(primary_tags)
                attempts += 1
            else:
                return success

        if not success:
            print(f"Ошибка: не удалось собрать бокс за {max_attempts} попыток.")

    return main_main()
