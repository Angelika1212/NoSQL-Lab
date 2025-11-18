from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['labwork3']


def select_by_country(country, leader):
    return leader.find_one({"country": country})


def select_by_board_date(date, leader):
    return list(leader.find({"leader.board_date": date}))


def select_by_role(role, leader):
    return list(leader.find({"leader.role": {"$regex": role, "$options": "i"}}))


def select_by_date_range(start_year, end_year, leader):
    return list(leader.find({"leader.board_date": {"$gte": start_year, "$lte": end_year}}))


def get_role_statistics(leader):
    pipeline = [{"$group": {"_id": "$leader.role", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}]
    return list(leader.aggregate(pipeline))


if __name__ == "__main__":
    labwork3 = get_database()
    leaders = labwork3["leaders"]

    print("1. Поиск главы по названию страны:")
    print(select_by_country("Ирландия", leaders)['leader']['name'])

    print("2. Получение всех глав, вступивших в должность в определенный год:")
    print(select_by_board_date(2025, leaders)[0]['leader']['name'])

    print("3. Поиск всех глав, которые занимают определенную должность:")
    print(select_by_role("Президент", leaders)[0]['leader']['name'])

    print("4. Статистика по должностям:")
    results = get_role_statistics(leaders)

    for item in results:
        print(item['_id'] + ": " + str(item['count']))

    print("5. Получить всех глав, год вступления в должность которых попадает в диапазон:")
    print(select_by_date_range(1988, 2015, leaders)[0]['leader']['name'])

    labwork3.client.close()
