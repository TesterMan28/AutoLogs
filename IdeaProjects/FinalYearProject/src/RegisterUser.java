import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

import javax.swing.*;
import java.sql.*;

// Reference code: https://alvinalexander.com/java/java-mysql-insert-example-preparedstatement
public class RegisterUser {

    public void register(String username, String password) {
        try {
            MysqlDataSource dataSource = new MysqlDataSource();
            dataSource.setUser("root");
            dataSource.setPassword("");
            dataSource.setServerName("localhost");
            dataSource.setDatabaseName("fyp");

            Connection conn = dataSource.getConnection();

            // Check if username exists in database. If it does inform use that username cannot be used
            String usernameCounter;
            PreparedStatement preparedStmt = conn.prepareStatement("SELECT * FROM user order by username desc");
            ResultSet rs = preparedStmt.executeQuery();
            if (rs.next()) {
                usernameCounter = rs.getString("username");
                if (usernameCounter.equals(username)) {
                    throw new UserExistsException("Username " + usernameCounter + " already exists");
                }
            }
            rs.close();


            String query = "insert into user (username, password)" + " values (?, ?)";

            // PreparedStatement preparedStmt = conn.prepareStatement(query);
            preparedStmt = conn.prepareStatement(query);
            preparedStmt.setString(1, username);
            preparedStmt.setString(2, password);

            // Execute the prepared statement
            preparedStmt.execute();

            // If no error, print success message
            System.out.println("Successfully registered to the database");

            preparedStmt.close();
            conn.close();

        } catch (Exception e) {
            System.err.println("Got an error!");
            System.err.println(e.getMessage());
        }
    }
}

class UserExistsException extends Exception {
    public UserExistsException(String errorMesssage) {
        super(errorMesssage);
    }
}
