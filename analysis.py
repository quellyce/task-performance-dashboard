import pandas as pd
import matplotlib.pyplot as plt

employees_df = pd.read_csv("employees.csv")
tasks_df = pd.read_csv("tasks.csv")

merge_df = pd.merge(employees_df, tasks_df, on="employee_id", how="left")

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

# Графики
# 1. Количество задач по статусам
tasks_df["status"].value_counts().plot(kind="bar")
plt.title("Количество задач по статусам")
plt.xlabel("Статус")
plt.xticks(rotation=0)
plt.ylabel("Количество задач")
plt.tight_layout()
plt.show()

# 2. Количество задач по отделам
department_tasks.plot(kind="bar")
plt.title("Количество задач по отделам")
plt.xlabel("Отделы")
plt.xticks(rotation=0)
plt.ylabel("Количество задач")
plt.tight_layout()
plt.show()

# 3. Статусы задач по отделам
department_status.plot(kind="bar")
plt.title("Статусы задач по отделам")
plt.xlabel("Отделы")
plt.xticks(rotation=0)
plt.ylabel("Количество задач")
plt.tight_layout()
plt.show()

# 4. Топ сотрудников по количеству задач
top_employees = (
    merge_df.groupby("employee_name")["task_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

ax = top_employees.plot(kind="barh")
plt.title("Топ сотрудников по количеству задач")
plt.xlabel("Количество задач")
plt.ylabel("Сотрудники")
plt.tight_layout()
ax.invert_yaxis()
ax.bar_label(ax.containers[0])
plt.show()

# Какой сотрудник выполняет больше всего просроченных задач?
overdue = (
    tasks_df[tasks_df["status"] == "Просрочено"]
    .groupby("employee_id")
    .size()
    .sort_values(ascending=False)
)
top_overdue = overdue.reset_index(name="overdue_tasks")
top_overdue = top_overdue.merge(employees_df, on="employee_id")
top_overdue = top_overdue[["employee_name", "department", "overdue_tasks"]]
print("Топ-10 сотрудников по просроченным задачам:")
print(top_overdue.head(10))
print()

# Топ-5 сотрудников по просроченным задачам
top_5 = top_overdue.head(5)
ax = top_5.plot(
    kind="barh",
    x="employee_name",
    y="overdue_tasks",
    legend=False,
    title="Топ-5 сотрудников по просроченным задачам"
)
plt.xlabel("Количество просроченных задач")
plt.ylabel("Сотрудник")
plt.tight_layout()
ax.invert_yaxis()
plt.show()

# В каких отделах в сумме больше всего просроченных задач
overdue_tasks_department = (
    top_overdue[["department", "overdue_tasks"]]
    .groupby("department")
    .sum()
    .sort_values(by="overdue_tasks", ascending=False)
)
print("Отдел с наибольшим количеством просроченных задач:")
print(overdue_tasks_department.head(1))
print()

# Всего задач по отделам
department_total = merge_df.groupby("department").size()
print("Всего задач по отделам:")
print(department_total)
print()

# Просроченных задач по отделам
department_overdue = (
    merge_df[merge_df["status"] == "Просрочено"]
    .groupby("department")
    .size()
    .reindex(department_total.index, fill_value=0)
)
print("Просроченных задач по отделам:")
print(department_overdue)
print()

# Процент просроченных задач по отделам
overdue_percent = round(
    (department_overdue / department_total * 100),
    1
)

# Рейтинг отделов по доле просроченных задач
top_overdue_percent = overdue_percent.sort_values(ascending=False)

print("Рейтинг отделов по доле просроченных задач:")
print(top_overdue_percent.astype(str) + "%")
print()

# График рейтинга отделов по проценту просрочек
top_overdue_percent.plot(kind="bar")
plt.title("Доля просроченных задач по отделам")
plt.xlabel("Отделы")
plt.xticks(rotation=0)
plt.ylabel("Доля просроченных задач, %")
plt.tight_layout()
plt.show()