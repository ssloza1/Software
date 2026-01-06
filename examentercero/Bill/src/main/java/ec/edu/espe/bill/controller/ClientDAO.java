package ec.edu.espe.bill.controller;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

public class ClientDAO {

    private static final String COLLECTION_NAME = "cliente"; // como pediste
    private final MongoCollection<Document> collection;

    public ClientDAO() {
        MongoDatabase db = MongoDBManager.getDatabase();
        this.collection = db.getCollection(COLLECTION_NAME);
    }

    public void insertClient(String name, String phone, String address, String email) {
        Document doc = new Document("name", name)
                .append("phone", phone)
                .append("address", address)
                .append("email", email)
                .append("createdAt", java.time.Instant.now().toString());
        collection.insertOne(doc);
    }
}

