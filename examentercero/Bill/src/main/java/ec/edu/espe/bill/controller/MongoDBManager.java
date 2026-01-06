package ec.edu.espe.bill.controller;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;

/**
 * Administrador de MongoDB (singleton).
 * Aquí pegas tu URI de MongoDB Atlas (la misma que usas en MongoDB Compass).
 */
public class MongoDBManager {

    // TODO: Pega aquí tu URI de MongoDB Atlas/Compass (ej: mongodb+srv://user:pass@cluster...)
    private static final String MONGO_URI = "mongodb+srv://Steven:Steven2001@cluster0.mp8muds.mongodb.net/?appName=Cluster0";

    // TODO: Cambia el nombre si tu base se llama diferente
    private static final String DB_NAME = "BillDB";

    private static MongoClient client;

    private MongoDBManager() {
    }

    public static MongoDatabase getDatabase() {
        if (client == null) {
            client = MongoClients.create(MONGO_URI);
        }
        return client.getDatabase(DB_NAME);
    }
}

