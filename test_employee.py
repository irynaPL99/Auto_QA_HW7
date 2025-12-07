import pytest
import uuid
from employee_api import EmployeeApi

"""
Разработать автоматические тесты,
которые проверяют корректность работы API для управления сотрудниками.
Создайте класс EmployeeApi для создания вспомогательных методов.
API Методы
http://5.101.50.27:8000/docs#/
"""

BASE_URL = "http://5.101.50.27:8000"
COMPANY_ID = 1
api = EmployeeApi(BASE_URL)

# 1. Создание нового работника
# Метод: POST
# URL http://5.101.50.27:8000/employee/create
# Описание: Создаёт нового сотрудника, принимает данные в JSON.

def test_create_employee():
    """Создание сотрудника — API не возвращает id, но сотрудник создаётся"""
    before = len(api.get_employee_list_with_company_id(COMPANY_ID))
    email = f"peter_{uuid.uuid4()}@test.example.com"

    result = api.create_employee(
        first_name="Peter",
        last_name="Griffin",
        middle_name="TheGreat",
        company_id=COMPANY_ID,
        email=email,
        phone="+79991234567",
        birthdate="1970-05-05",
        is_active=True
    )

    # API может не вернуть id — это нормально
    after = len(api.get_employee_list_with_company_id(COMPANY_ID))
    assert after == before + 1

    employees = api.get_employee_list_with_company_id(COMPANY_ID)
    new_emp = next(e for e in employees if e["email"] == email)
    assert new_emp["first_name"] == "Peter"
    print(f"Создан сотрудник: {new_emp['id']}")


# 2. Получение информации о работнике
# Метод: GET
# URL http://5.101.50.27:8000/employee/info
# Описание: Получает данные о сотруднике по его ID.

def test_get_employee_info():
    """Получение данных по ID"""
    email = f"anna_{uuid.uuid4()}@test.example.com"
    emp_id = api.create_employee_and_get_id(
        company_id=COMPANY_ID,
        first_name="Anna",
        last_name="Karenina",
        email=email,
        phone="+79995557788"
    )

    info = api.get_employee_info(emp_id)
    assert info["id"] == emp_id
    assert info["email"] == email
    assert info["first_name"] == "Anna"
    print(f"Получена информация по ID {emp_id}")


# 3. Изменение данных о работнике
# Метод: PATCH
# URL http://5.101.50.27:8000/employee/change
# Описание: Позволяет изменить информацию о сотруднике по его ID

def test_update_employee():
    """Обновление данных сотрудника"""
    emp_id = api.create_employee_and_get_id(
        company_id=COMPANY_ID,
        first_name="Old",
        last_name="Name",
        phone="+79991112233"
    )

    updated = api.update_employee(
        emp_id,
        first_name="NewName",
        phone="+79001234567",
        is_active=False
    )

    assert updated["first_name"] == "NewName"
    assert updated["is_active"] is False

    fresh = api.get_employee_info(emp_id)
    assert fresh["first_name"] == "NewName"
    print(f"Сотрудник {emp_id} обновлён")


# def test_delete_employee():
#     """Удаление сотрудника"""
#     emp_id = api.create_employee_and_get_id(company_id=COMPANY_ID)
#
#     before = len(api.get_employee_list_with_company_id(COMPANY_ID))
#     api.delete_employee(emp_id)
#     after = len(api.get_employee_list_with_company_id(COMPANY_ID))
#
#     assert after == before - 1
#     print(f"Сотрудник {emp_id} удалён")


# def test_create_duplicate_email():
#     """Негативный кейс: дубликат email"""
#     email = f"dup_{uuid.uuid4()}@test.example.com"
#     api.create_employee_and_get_id(company_id=COMPANY_ID, email=email)
#
#     # Второй раз — должен не создаться (API вернёт 200, но без создания)
#     before = len(api.get_employee_list_with_company_id(COMPANY_ID))
#     api.create_employee(
#         first_name="Duplicate",
#         last_name="Test",
#         middle_name="X",
#         company_id=COMPANY_ID,
#         email=email,  # тот же email!
#         phone="+79998887766",
#         birthdate="2000-01-01",
#         is_active=True
#     )
#     after = len(api.get_employee_list_with_company_id(COMPANY_ID))
#     assert after == before  # количество не увеличилось
#     print("Дубликат email корректно обработан")