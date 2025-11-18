/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ec.edu.espe.CrudJsonSalaryJava.model;

/**
 *
 * @author Steven Loza @ESPE
 */
class Employee {

    private String name;
    private int age;
    private double salary;
    private double bonus13; // NEW FIELD

    public Employee(String name, int age, double salary) {
        this.name = name;
        this.age = age;
        this.salary = salary;
        this.bonus13 = 0; // default
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public double getSalary() {
        return salary;
    }

    public double getBonus13() {
        return bonus13;
    }

    public void setBonus13(double bonus13) {
        this.bonus13 = bonus13;
    }
}
