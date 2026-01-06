package ec.edu.espe.bill.controller;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import java.util.List;
import org.bson.Document;

public class BillDAO {

    private static final String COLLECTION_NAME = "bill"; // como pediste
    private final MongoCollection<Document> collection;

    public BillDAO() {
        MongoDatabase db = MongoDBManager.getDatabase();
        this.collection = db.getCollection(COLLECTION_NAME);
    }

    public void insertBill(Document clientData, List<Document> items, double subtotal, double iva, double totalNeto) {

        // ID de factura opcional (por si quieres identificarla fácilmente)
        String billId = java.time.LocalDateTime.now()
                .format(java.time.format.DateTimeFormatter.ofPattern("yyyyMMddHHmmss"));

        Document billDoc = new Document("billId", billId)
                .append("client", clientData)
                .append("items", items)
                .append("subtotal", subtotal)
                .append("iva", iva)
                .append("totalNeto", totalNeto)
                .append("createdAt", java.time.Instant.now().toString());

        collection.insertOne(billDoc);
    }
}
