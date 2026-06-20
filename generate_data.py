from faker import Faker
from datetime import timedelta
import pandas as pd
import random

fake = Faker("ru_RU")

employees = []

departments = [
    "Продажи",
    "Поддержка",
    "Разработка",
    "Аналитика",
    "Маркетинг"
]

for employee_id in range(1, 51):
    gender = random.choice(["male", "female"])

    if gender == "male":
        full_name = f"{fake.last_name_male()} {fake.first_name_male()}"
    else:
        full_name = f"{fake.last_name_female()} {fake.first_name_female()}"

    employees.append({
        "employee_id": employee_id,
        "employee_name": full_name,
        "department": random.choice(departments)
    })

employees_df = pd.DataFrame(employees)

employees_df.to_csv("employees.csv", index=False, encoding="utf-8-sig")


tasks = []

for task_id in range(1, 501):
    created_date = fake.date_between(start_date="-6M", end_date="now")
    deadline = created_date + timedelta(days=random.randint(1, 30))
    completed_date = created_date + timedelta(days=random.randint(1, 10))

    chance = random.random()
    if chance < 0.2:
        status = "В работе"
        completed_date = None
    elif completed_date > deadline:
        status = "Просрочено"
    else: status = "Выполнено"

    tasks.append({
        "task_id": task_id,
        "employee_id": random.choice(employees)["employee_id"],
        "created_date": created_date,
        "due_date": deadline,
        "completed_date": completed_date,
        "status": status
    })



tasks_df = pd.DataFrame(tasks)

tasks_df.to_csv("tasks.csv", index=False, encoding="utf-8-sig")