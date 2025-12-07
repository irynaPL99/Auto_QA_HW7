import requests
import uuid


class EmployeeApi:
    """Класс для взаимодействия с тестовым API сотрудников"""

    def __init__(self, url: str):
        self.url = url.rstrip("/")

    def get_employee_list_with_company_id(self, company_id: int):
        resp = requests.get(f"{self.url}/employee/list/{company_id}")
        assert resp.status_code == 200, f"Ошибка: {resp.status_code} {resp.text}"
        return resp.json()

    def create_employee(self, first_name, last_name, middle_name, company_id,
                        email, phone, birthdate, is_active):
        employee = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "company_id": company_id,
            "email": email,
            "phone": phone,
            "birthdate": birthdate,
            "is_active": is_active
        }
        resp = requests.post(f"{self.url}/employee/create", json=employee)
        assert resp.status_code == 200, f"Ошибка создания: {resp.status_code} {resp.text}"
        return resp.json()

    def get_employee_info(self, employee_id: int):
        resp = requests.get(f"{self.url}/employee/info", params={"id": employee_id})
        assert resp.status_code == 200, f"Ошибка получения: {resp.status_code}"
        return resp.json()

    def update_employee(self, employee_id: int, **kwargs):
        resp = requests.patch(
            f"{self.url}/employee/change",
            params={"id": employee_id},
            json=kwargs
        )
        assert resp.status_code == 200, f"Ошибка обновления: {resp.status_code} {resp.text}"
        return resp.json()

    def delete_employee(self, employee_id: int):
        resp = requests.delete(f"{self.url}/employee/delete", params={"id": employee_id})
        assert resp.status_code == 200, f"Ошибка удаления: {resp.status_code}"
        return resp.json()

    # Умный помощник: создаёт и возвращает id, даже если API не отдаёт его
    def create_employee_and_get_id(self, company_id: int, **partial_data):
        email = partial_data.get("email", f"auto_{uuid.uuid4()}@test.example.com")
        full_data = {
            "first_name": partial_data.get("first_name", "Auto"),
            "last_name": partial_data.get("last_name", "Test"),
            "middle_name": partial_data.get("middle_name", "Generated"),
            "company_id": company_id,
            "email": email,
            "phone": partial_data.get("phone", "+79990000001"),
            "birthdate": partial_data.get("birthdate", "1990-01-01"),
            "is_active": partial_data.get("is_active", True)
        }
        self.create_employee(**full_data)

        employees = self.get_employee_list_with_company_id(company_id)
        employee = next((e for e in employees if e["email"] == email), None)
        assert employee is not None, f"Не найден созданный сотрудник с email {email}"
        return employee["id"]