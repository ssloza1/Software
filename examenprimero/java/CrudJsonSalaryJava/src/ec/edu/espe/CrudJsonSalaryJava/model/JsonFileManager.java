/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ec.edu.espe.CrudJsonSalaryJava.model;

/**
 *
 * @author Steven Loza @ESPE
 */
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.*;
import java.util.ArrayList;

class JsonFileManager {

    private static final String FILE_NAME = "employees.json";
    private static final Gson gson = new Gson();

    public static void saveList(ArrayList<Employee> list) {
        try (FileWriter writer = new FileWriter(FILE_NAME)) {
            gson.toJson(list, writer);
        } catch (IOException e) {
            System.out.println("Error saving JSON: " + e.getMessage());
        }
    }

    public static ArrayList<Employee> readList() {
        File file = new File(FILE_NAME);
        if (!file.exists()) {
            return new ArrayList<>();
        }

        try (FileReader reader = new FileReader(FILE_NAME)) {
            return gson.fromJson(reader, new TypeToken<ArrayList<Employee>>() {
            }.getType());
        } catch (IOException e) {
            System.out.println("Error reading JSON: " + e.getMessage());
            return new ArrayList<>();
        }
    }
}
