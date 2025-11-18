const fs = require("fs");
const readline = require("readline");

// ==========================================
// MODEL: Employee
// ==========================================
class Employee {
    constructor(id, name, salary, salary13 = 0) {
        this.id = id;
        this.name = name;
        this.salary = salary;
        this.salary13 = salary13;
    }
}

// ==========================================
// FILE MANAGER
// ==========================================
class FileManager {
    static FILE = "employees.json";

    static load() {
        if (!fs.existsSync(this.FILE)) {
            return [];
        }
        let data = JSON.parse(fs.readFileSync(this.FILE));
        return data.map(e => new Employee(e.id, e.name, e.salary, e.salary13));
    }

    static save(employees) {
        fs.writeFileSync(this.FILE, JSON.stringify(employees, null, 4));
    }
}

// ==========================================
// BONUS CALCULATOR
// ==========================================
class BonusCalculator {
    static calculate13Salary(employee) {
        employee.salary13 = parseFloat((employee.salary / 12).toFixed(2));
        return employee.salary13;
    }
}

// ==========================================
// MENU SYSTEM
// ==========================================
class Menu {
    constructor() {
        this.employees = FileManager.load();
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }

    show() {
        console.log("\n========= EMPLOYEE MANAGER =========");
        console.log("1. Add employee");
        console.log("2. List employees");
        console.log("3. Calculate 13th salary");
        console.log("4. Remove employee");
        console.log("5. Exit");

        this.rl.question("Select option: ", option => {
            switch (option) {
                case "1": this.addEmployee(); break;
                case "2": this.listEmployees(); break;
                case "3": this.calculate13Salary(); break;
                case "4": this.removeEmployee(); break;
                case "5":
                    FileManager.save(this.employees);
                    console.log("Bye!");
                    this.rl.close();
                    break;
                default:
                    console.log("Invalid option");
                    this.show();
            }
        });
    }

    // =====================
    // CRUD
    // =====================
    addEmployee() {
        this.rl.question("ID: ", id => {
            this.rl.question("Name: ", name => {
                this.rl.question("Salary: ", salary => {
                    let emp = new Employee(id, name, parseFloat(salary));
                    this.employees.push(emp);
                    FileManager.save(this.employees);
                    console.log("Employee added!");
                    this.show();
                });
            });
        });
    }

    listEmployees() {
        if (this.employees.length === 0) {
            console.log("No employees found.");
        } else {
            this.employees.forEach(e => {
                console.log(`ID: ${e.id} | Name: ${e.name} | Salary: ${e.salary} | 13th Salary: ${e.salary13}`);
            });
        }
        this.show();
    }

    calculate13Salary() {
        this.rl.question("Employee ID: ", id => {
            let emp = this.employees.find(e => e.id === id);
            if (!emp) {
                console.log("Employee not found.");
                return this.show();
            }

            let amount = BonusCalculator.calculate13Salary(emp);
            FileManager.save(this.employees);

            console.log(`13th salary calculated: ${amount}`);
            this.show();
        });
    }

    removeEmployee() {
        this.rl.question("Employee ID: ", id => {
            this.employees = this.employees.filter(e => e.id !== id);
            FileManager.save(this.employees);
            console.log("Employee removed.");
            this.show();
        });
    }
}

// ==========================================
// MAIN
// ==========================================
new Menu().show();
