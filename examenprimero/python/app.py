import json
import os

# ============================
# MODEL: Employee
# ============================
class Employee:
    def __init__(self, emp_id, name, salary, salary13=0):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
        self.salary13 = salary13

    def to_dict(self):
        return {
            "id": self.emp_id,
            "name": self.name,
            "salary": self.salary,
            "salary13": self.salary13
        }

    @staticmethod
    def from_dict(data):
        return Employee(
            emp_id=data["id"],
            name=data["name"],
            salary=data["salary"],
            salary13=data.get("salary13", 0)
        )


# ============================
# FILE MANAGER
# ============================
class FileManager:
    FILE = "employees.json"

    @staticmethod
    def load():
        if not os.path.exists(FileManager.FILE):
            return []
        with open(FileManager.FILE, "r") as file:
            data = json.load(file)
            return [Employee.from_dict(e) for e in data]

    @staticmethod
    def save(employee_list):
        with open(FileManager.FILE, "w") as file:
            json.dump([e.to_dict() for e in employee_list], file, indent=4)


# ============================
# BONUS CALCULATOR
# ============================
class BonusCalculator:
    @staticmethod
    def calculate_13_salary(employee):
        """Décimo tercer sueldo = total / 12"""
        employee.salary13 = round(employee.salary / 12, 2)
        return employee.salary13


# ============================
# MENU
# ============================
class Menu:
    def __init__(self):
        self.employees = FileManager.load()

    def show(self):
        while True:
            print("\n========= EMPLOYEE MANAGER =========")
            print("1. Add employee")
            print("2. List employees")
            print("3. Calculate 13th salary")
            print("4. Remove employee")
            print("5. Exit")
            option = input("Select option: ")

            if option == "1":
                self.add_employee()
            elif option == "2":
                self.list_employees()
            elif option == "3":
                self.calculate_13_salary()
            elif option == "4":
                self.remove_employee()
            elif option == "5":
                FileManager.save(self.employees)
                print("Bye!")
                break
            else:
                print("Invalid option!")

    # -------------------------
    # CRUD METHODS
    # -------------------------
    def add_employee(self):
        try:
            emp_id = input("ID: ")
            name = input("Name: ")
            salary = float(input("Salary: "))

            emp = Employee(emp_id, name, salary)
            self.employees.append(emp)
            FileManager.save(self.employees)

            print("Employee added!")
        except:
            print("Error adding employee.")

    def list_employees(self):
        if not self.employees:
            print("No employees found.")
            return

        for e in self.employees:
            print(f"ID: {e.emp_id} | Name: {e.name} | Salary: {e.salary} | 13th Salary: {e.salary13}")

    def calculate_13_salary(self):
        emp_id = input("Employee ID: ")
        emp = next((e for e in self.employees if e.emp_id == emp_id), None)

        if not emp:
            print("Employee not found.")
            return

        amount = BonusCalculator.calculate_13_salary(emp)
        FileManager.save(self.employees)

        print(f"13th salary calculated: {amount}")

    def remove_employee(self):
        emp_id = input("Employee ID: ")
        self.employees = [e for e in self.employees if e.emp_id != emp_id]
        FileManager.save(self.employees)
        print("Employee removed.")


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    Menu().show()
