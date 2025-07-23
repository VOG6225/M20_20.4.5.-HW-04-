import os
import json

# ***************************************************************************************************
# Задание:
# Вам нужно считать данные из файла, обработать их и найти с помощью данных следующую информацию:
#
# Какой номер самого дорого заказа за июль?
# Какой номер заказа с самым большим количеством товаров?
# В какой день в июле было сделано больше всего заказов?
# Какой пользователь сделал самое большое количество заказов за июль?
# У какого пользователя самая большая суммарная стоимость заказов за июль?
# Какая средняя стоимость заказа была в июле?
# Какая средняя стоимость товаров в июле?
#
# ***************************************************************************************************
# Структура JSON
# 'Номер заказа':
# {
#     'date': 'Дата заказа',
#     'user_id': id клиента,
# 'quantity': количество
# товаров
# в
# заказе,
# 'price': стоимость
# заказа
# },
#
# 'Номер заказа':
# {
#     'date': 'Дата заказа',
#     'user_id': id клиента,
# 'quantity': количество
# товаров
# в
# заказе,
# 'price': стоимость
# заказа
# }
#
# Преобразуем данные из файла JSON в словарь
# ***************************************************************************************************

with open("orders_july_2023.json", "r", encoding="utf-8") as file:
    translator = json.load(file)


# Какой номер самого дорого заказа за июль?

max_price = 0
max_order = ''

# цикл по заказам

for key_order, value in translator.items():
    for key, value in value.items():
        if key == "price":
            if value > max_price:
                max_price = value
                max_order = key_order

print(f'Номер заказа с самой большой стоимостью: {max_order}, стоимость заказа: {max_price}')

# Какой номер самого дорого заказа за июль?
max_price_july = 0
max_order_july = ''

for order_id, order_data in translator.items():
    if 'date' in order_data:
        # Проверяем, заканчивается ли дата на цифру 7
        if order_data['date'][-1] == '7':
            if 'price' in order_data:
                current_price = order_data['price']
                if current_price > max_price_july:
                    max_price_july = current_price
                    max_order_july = order_id

print(f'Номер самого дорого заказа за июль: {max_order_july}, стоимость: {max_price_july}')

# В какой день в июле было сделано больше всего заказов?

days_list = []

# Собираем все подходящие дни
for order in translator.values():
    if 'date' in order:
        date_str = order['date']
        if date_str and len(date_str) >= 10 and date_str[-1] == '7':
            parts = date_str.split('-')
            if len(parts) == 3:
                days_list.append(parts[1])  # Добавляем только день из всей даты

# Проверка данных
if not days_list:
    print("Нет подходящих заказов")
else:
    day_counts = {}
    for day in days_list:
        if day in day_counts:
            day_counts[day] += 1
        else:
            day_counts[day] = 1

    # Находим максимальное количество заказов
    max_count = max(day_counts.values())

    # Собираем все дни с максимальным количеством заказов
    popular_days = [day for day, count in day_counts.items() if count == max_count]

    # Сортируем дни
    popular_days_sorted = sorted(popular_days)
    most_popular_day = popular_days_sorted[0]

    print(f"Самый популярный день заказов: {most_popular_day} июля, (заказов: {max_count})")



# Какой пользователь сделал самое большое количество заказов за июль?


user_orders = {}


for order_data in translator.values():
    # Проверка полей
    if 'user_id' in order_data and 'date' in order_data:
        date_str = order_data['date']

        # Проверка, что дата в июле
        if date_str and date_str[-1] == '7':
            user_id = order_data['user_id']

            # Увеличиваем счетчик заказов
            if user_id in user_orders:
                user_orders[user_id] += 1
            else:
                user_orders[user_id] = 1

max_orders = max(user_orders.values())

top_users = [user for user, orders in user_orders.items() if orders == max_orders]

# Сортируем
top_users_sorted = sorted(top_users)

print(f"Пользователь с наибольшим количеством заказов за июль: ID - {top_users_sorted[0]}, количество заказов: {max_orders}")


#У какого пользователя самая большая суммарная стоимость заказов за июль?


user_total_spent = {}

# Перебор заказов
for order_data in translator.values():

    # проверка полей
    if all(key in order_data for key in ['user_id', 'date', 'price']):
        date_str = order_data['date']

        # Проверка на июль
        if date_str and date_str[-1] == '7':
            user_id = order_data['user_id']
            price = float(order_data['price'])  # Цену в число

            # Добавляем стоимость заказа к сумме пользователя
            if user_id in user_total_spent:
                user_total_spent[user_id] += price
            else:
                user_total_spent[user_id] = price


max_spent = max(user_total_spent.values())

top_spenders = [user for user, total in user_total_spent.items() if total == max_spent]

top_spenders_sorted = sorted(top_spenders)


print(f"Пользователь с наибольшей стоимость заказов за июль: ID - {top_spenders_sorted[0]}, сумма заказов: {max_spent:.2f}")



# Какая средняя стоимость заказа была в июле? Какая средняя стоимость товаров в июле?

total_orders = 0          # Общее количество заказов
total_price = 0.0         # Общая сумма всех заказов
total_quantity = 0        # Общее количество товаров
total_items_price = 0.0   # Общая стоимость всех товаров

# перебор заказов по словарю
for order_data in translator.values():
    # проверка полей
    if all(key in order_data for key in ['date', 'price', 'quantity']):
        date_str = order_data['date']

        # Проверка на июль
        if date_str and date_str[-1] == '7':
            #Преобразуем данные к числовому формату

            price = float(order_data['price'])
            quantity = int(order_data['quantity'])

            # Считаем общие показатели
            total_orders += 1
            total_price += price
            total_quantity += quantity
            total_items_price += price  # Если price - это стоимость всех товаров в заказе

# Ср. стоимость заказа
avg_order_price = total_price / total_orders

# Сред стоимость товара
avg_item_price = total_items_price / total_quantity

print(f"Средняя стоимость заказа в июле: {avg_order_price:.2f} руб.")
print(f"Средняя стоимость товара в июле: {avg_item_price:.2f} руб.")