package ec.edu.espe.bill.controller;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Sorts;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import org.bson.Document;
import com.mongodb.client.model.Projections;

public class ProductDAO {

    private static final String COLLECTION_NAME = "PRODUCT"; // Colección requerida

    private final MongoCollection<Document> collection;

    public ProductDAO() {
        MongoDatabase db = MongoDBManager.getDatabase();
        this.collection = db.getCollection(COLLECTION_NAME);
    }

    /**
     * Genera ID en formato yyyyMMdd-001, yyyyMMdd-002...
     * Reinicia correlativo cada día.
     */
    public String generateNextProductId() {
        String today = LocalDate.now().format(DateTimeFormatter.BASIC_ISO_DATE); // yyyyMMdd

        // Busca el último ID del día (prefijo yyyyMMdd-)
        Document last = collection.find(Filters.regex("productId", "^" + today + "-"))
                .sort(Sorts.descending("productId"))
                .limit(1)
                .first();

        int nextSeq = 1;

        if (last != null) {
            String lastId = last.getString("productId"); // ejemplo: 20260105-003
            if (lastId != null && lastId.contains("-")) {
                String[] parts = lastId.split("-");
                if (parts.length == 2) {
                    try {
                        int lastSeq = Integer.parseInt(parts[1]);
                        nextSeq = lastSeq + 1;
                    } catch (NumberFormatException ignored) {
                        nextSeq = 1;
                    }
                }
            }
        }

        return today + "-" + String.format("%03d", nextSeq);
    }

    public void insertProduct(String productId, String name, String detail, int stock, double price) {
        Document doc = new Document("productId", productId)
                .append("name", name)
                .append("detail", detail)
                .append("stock", stock)
                .append("price", price)
                .append("createdAt", java.time.Instant.now().toString());

        collection.insertOne(doc);
    }
    
    public Document findByProductId(String productId) {
    return collection.find(Filters.eq("productId", productId))
            .projection(Projections.excludeId())
            .first();
}

public Document findByName(String name) {
    // Búsqueda exacta por nombre. Si quieres parcial (contains), me dices y lo cambio.
    return collection.find(Filters.eq("name", name))
            .projection(Projections.excludeId())
            .first();
}

}

