import os
import csv


class Record:
    # Базовый класс (для наследования)
    def __repr__(self):
        return "Record()"


class DishRecord(Record):  # changed in ORIGINAL
    # Одна запись: №, блюдо, время заказа, время приготовления, отзыв
    def __init__(self, num, dish, order_time, prep_time, review):
        self.num = num
        self.dish = dish
        self.order_time = order_time
        self.prep_time = prep_time
        self.review = review

    def __setattr__(self, name, value):
        # Все записи полей идут через __setattr__
        if name == "num":
            value = int(value)
            if value <= 0:
                raise ValueError("№ должен быть > 0")
        elif name == "dish":
            value = str(value).strip()
            if value == "":
                raise ValueError("Название блюда пустое")
        elif name == "order_time":
            value = str(value).strip()
        elif name == "prep_time":
            value = int(value)
            if value < 0:
                raise ValueError("Время приготовления должно быть >= 0")
        elif name == "review":
            value = str(value).strip()

        object.__setattr__(self, name, value)

    def __repr__(self):
        # Перегрузка repr
        return f"DishRecord({self.num}, {self.dish}, {self.order_time}, {self.prep_time}, {self.review})"

    @staticmethod
    def from_dict(d):
        # Статический метод: из словаря CSV в объект
        return DishRecord(
            d["№"],
            d["наименование блюда"],
            d["время размещения заказа"],
            d["время приготовления"],
            d["отзыв"],
        )

    def to_dict(self):
        return {
            "№": str(self.num),
            "наименование блюда": self.dish,
            "время размещения заказа": self.order_time,
            "время приготовления": str(self.prep_time),
            "отзыв": self.review,
        }


class History:
    headers = ["№", "наименование блюда", "время размещения заказа", "время приготовления", "отзыв"]

    def __init__(self):
        self.items = []

    def __setattr__(self, name, value):
        # Запись свойств через __setattr__
        if name == "items" and not isinstance(value, list):
            raise ValueError("items должен быть списком")
        object.__setattr__(self, name, value)

    def __repr__(self):
        return f"History(size={len(self.items)})"

    def __iter__(self):
        # Итератор
        return iter(self.items)

    def __getitem__(self, index):
        # Доступ по индексу
        return self.items[index]

    def add(self, record):
        self.items.append(record)

    def sort_by_dish(self):
        # Сортировка по строковому полю
        return sorted(self.items, key=lambda x: x.dish.lower())

    def sort_by_prep_time(self):
        # Сортировка по числовому полю
        return sorted(self.items, key=lambda x: x.prep_time)

    def filter_long_cooking(self, minutes):
        # Генератор
        for x in self.items:
            if x.prep_time > minutes:
                yield x

    @staticmethod
    def count_files(path):
        # Статический метод
        c = 0
        for obj in os.scandir(path):
            if obj.is_file():
                c += 1
        return c

    @staticmethod
    def load_csv(filename):
        h = History()
        if not os.path.exists(filename):
            return h

        with open(filename, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    h.add(DishRecord.from_dict(row))
                except:
                    pass
        return h

    def save_csv(self, filename):
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            for x in self.items:
                writer.writerow(x.to_dict())


# ------------------- основной код -------------------

csv_name = "data.csv"

# 1) Подсчет файлов в папке
folder = input("Введите путь к папке: ")
try:
    print("Файлов в папке:", History.count_files(folder))
except:
    print("Не удалось открыть папку")

# 2) Чтение CSV
history = History.load_csv(csv_name)
print("\nИсходные записи:")
for x in history:
    print(x)

# 2.1) Сортировка по строковому полю
print("\nСортировка по блюду:")
for x in history.sort_by_dish():
    print(x)

# 2.2) Сортировка по числовому полю
print("\nСортировка по времени приготовления:")
for x in history.sort_by_prep_time():
    print(x)

# 2.3) Фильтр по критерию
m = int(input("\nПорог времени приготовления: "))
print(f"Блюда, где время > {m}:")
for x in history.filter_long_cooking(m):
    print(x)

# Демонстрация __getitem__
if len(history.items) > 0:
    print("\nПервый элемент history[0]:", history[0])

# 3) Добавить запись и сохранить
ans = input("\nДобавить новую запись? (да/нет): ").strip().lower()
if ans == "да":
    num = input("№: ")
    dish = input("Блюдо: ")
    order_time = input("Время заказа (HH:MM): ")
    prep_time = input("Время приготовления (мин): ")
    review = input("Отзыв: ")

    try:
        history.add(DishRecord(num, dish, order_time, prep_time, review))
        history.save_csv(csv_name)
        print("Сохранено в data.csv")
    except Exception as e:
        print("Ошибка:", e)
else:
    history.save_csv(csv_name)
    print("Файл обновлен без добавления новой записи")# Version 1.0.1
# Change in original
# ORIGINAL CHANGE
# Version 1.0.1
# feature-a change
