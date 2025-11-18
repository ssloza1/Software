/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ec.edu.espe.CrudJsonSalaryJava.model;

/**
 *
 * @author Steven Loza @ESPE
 */
import java.util.ArrayList;
import java.util.Scanner;

public class Menu {

    private ArrayList<Employee> employees;
    private Scanner sc;

    public Menu() {
        employees = JsonFileManager.readList();
        sc = new Scanner(System.in);
    }

    public void show() {
        int option;
        do {
            System.out.println("===== CRUD MENU (GSON) =====");
            System.out.println("1. Create employee");
            System.out.println("2. Read employees");
            System.out.println("3. Update employee salary");
            System.out.println("4. Calculate 13th salary (and save)");
            System.out.println("5. Delete employee");
            System.out.println("6. Exit");
            System.out.print("Choose: ");
            option = sc.nextInt();
            sc.nextLine();

            switch (option) {
                case 1 ->
                    create();
                case 2 ->
                    read();
                case 3 ->
                    update();
                case 4 ->
                    calculate();
                case 5 ->
                    delete();
                case 6 ->
                    System.out.println("Exiting...");
                default ->
                    System.out.println("Invalid option.");
            }
        } while (option != 6);
    }

    private void create() {
        System.out.print("Name: ");
        String name = sc.nextLine();
        System.out.print("Age: ");
        int age = sc.nextInt();
        System.out.print("Salary: ");
        double salary = sc.nextDouble();
        sc.nextLine();

        employees.add(new Employee(name, age, salary));
        JsonFileManager.saveList(employees);

        System.out.println("Employee created and saved.\n");
    }

    private void read() {
        employees = JsonFileManager.readList();
        System.out.println("===== EMPLOYEE LIST =====");

        for (Employee e : employees) {
            System.out.println(
                    "Name: " + e.getName()
                    + ", Age: " + e.getAge()
                    + ", Salary: " + e.getSalary()
                    + ", 13th Salary: " + e.getBonus13()
            );
        }
        System.out.println();
    }

    private void update() {
        System.out.print("Enter employee name to update salary: ");
        String name = sc.nextLine();

        for (Employee e : employees) {
            if (e.getName().equalsIgnoreCase(name)) {

                System.out.print("New salary: ");
                double newSalary = sc.nextDouble();
                sc.nextLine();

                // Create updated employee
                Employee updated = new Employee(e.getName(), e.getAge(), newSalary);
                updated.setBonus13(e.getBonus13()); // preserve bonus if already calculated

                // Replace in list
                employees.set(employees.indexOf(e), updated);

                JsonFileManager.saveList(employees);
                System.out.println("Salary updated.\n");
                return;
            }
        }
        System.out.println("Employee not found.\n");
    }

    private void calculate() {
        System.out.print("Enter employee name: ");
        String name = sc.nextLine();

        for (Employee e : employees) {
            if (e.getName().equalsIgnoreCase(name)) {

                double value = BonusCalculator.calculateSalary13(e);

                // 🔥 Save new value inside the employee
                e.setBonus13(value);

                // 🔥 Save the whole list to JSON
                JsonFileManager.saveList(employees);

                System.out.println("13th salary: " + value);
                System.out.println("Saved to JSON.\n");
                return;
            }
        }

        System.out.println("Employee not found.\n");
    }

    private void delete() {
        System.out.print("Enter employee name to delete: ");
        String name = sc.nextLine();

        employees.removeIf(e -> e.getName().equalsIgnoreCase(name));
        JsonFileManager.saveList(employees);

        System.out.println("Employee deleted if existed.\n");
    }
}
