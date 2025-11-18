/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ec.edu.espe.CrudJsonSalaryJava.model;

/**
 *
 * @author Steven Loza @ESPE
 */
public class BonusCalculator {

    public static double calculateSalary13(Employee employee) {
        return employee.getSalary() / 12;
    }
}

