import javax.swing.*;
import java.sql.*;

public class QueryDatabase {
    public static void main(String[] args) {

    }
    public QueryDatabase(String username, String password) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test?useSSL=false&serverTimezone=UTC", "root", "");
            Statement stmt = conn.createStatement();
            String hashedPassword = EncryptPass.hashPass(password);
            String sql = "Select * from users where username=" + username + " and password=" + hashedPassword;
            ResultSet rs;
            rs = stmt.executeQuery(sql);
            while (rs.next()) {
                JOptionPane.showMessageDialog(null, "Welcome " + username);
            }
            conn.close();
        }
        catch (Exception ex) {
            System.err.println("Got an exception!");
            System.err.println(ex.getMessage());
            JOptionPane.showMessageDialog(null, "Unable to connect to database");
        }
    }
}
