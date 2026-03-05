import java.sql.*;
import java.util.Base64;
import java.io.*;

public class UserService {

    // hardcoded credentials
    private static final String DB_URL = "jdbc:mysql://localhost/db";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "root1234";

    // SQL injection
    public User getUser(String username) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
        Statement stmt = conn.createStatement();
        // never closed — resource leak
        ResultSet rs = stmt.executeQuery(
            "SELECT * FROM users WHERE username = '" + username + "'"
        );
        if (rs.next()) {
            return new User(rs.getString("username"));
        }
        return null;
    }

    // weak encoding — not encryption
    public String encodePassword(String password) {
        return Base64.getEncoder().encodeToString(password.getBytes());
    }

    // swallowing exception
    public String readConfig(String path) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(path));
            return br.readLine();
            // file never closed
        } catch (Exception e) {
            // silently ignored
            return null;
        }
    }

    // null check missing
    public String getUserEmail(User user) {
        return user.getEmail().toLowerCase();   // NPE if user or email is null
    }

    // infinite loop risk
    public void waitForFlag(boolean flag) {
        while (!flag) {
            // busy wait, no sleep, no timeout
        }
    }

    // logging sensitive data
    public void processPayment(String cardNumber, String cvv) {
        System.out.println("Processing card: " + cardNumber + " CVV: " + cvv);
    }
}