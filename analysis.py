import pandas as pd
import matplotlib.pyplot as plt

employees_df = pd.read_csv("employees.csv")
tasks_df = pd.read_csv("tasks.csv")

merge_df = pd.merge(employees_df, tasks_df, on="employee_id", how="left")
print()

tasks_by_employee = tasks_df.groupby("employee_id")["task_id"].count()
print("Количество задач по сотрудникам:")
print(tasks_by_employee.head())
print()

department_tasks = merge_df.groupby("department")["task_id"].count()
print("Количество задач по отделам:")
print(department_tasks)
print()

department_status = (
    merge_df.groupby(["department", "status"])
    .size()
    .unstack(fill_value=0)
)
print("Статусы задач по отделам:")
print(department_status)
print()

#Графики
#1
tasks_df["status"].value_counts().plot(kind="bar")
plt.title("Количество задач по статусам")
plt.xlabel("Статус")
plt.ylabel("Количество задач")
plt.show()

#2
department_tasks.plot(kind="bar")
plt.title("Количество задач по отделам")
plt.xlabel("Отделы")
plt.ylabel("Количество задач")
plt.show()

#3
department_status.plot(kind="bar")
plt.title("Статусы задач по отделам")
plt.xlabel("Отделы")
plt.ylabel("Количество задач")
plt.show()

#4
top_employees = (
    merge_df.groupby("employee_name")["task_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

top_employees.plot(kind="bar")
plt.title("Топ сотрудников по количеству задач")
plt.xlabel("Сотрудники")
plt.ylabel("Количество задач")
plt.show()

