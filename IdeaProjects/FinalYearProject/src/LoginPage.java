import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.beans.ExceptionListener;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class LoginPage implements MouseListener {
    public void LoginFrame() {
        JFrame loginFrame = new JFrame("Log In");
        loginFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        loginFrame.setSize(900, 900);
        loginFrame.setLocationRelativeTo(null);

        JPanel loginPanel = new JPanel();
        loginPanel.setLayout(new BoxLayout(loginPanel, BoxLayout.PAGE_AXIS));

        JLabel loginLabel = new JLabel("Login Page");
        loginLabel.setFont(new Font("Courier New", Font.BOLD, 30));

        JPanel usernamePanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 3, 3));
        JLabel usernameLabel = new JLabel("Username:");
        JTextField usernameEntry = new JTextField(20);

        usernamePanel.add(usernameLabel);
        usernamePanel.add(usernameEntry);

        JPanel passwordPanel = new JPanel(new FlowLayout());
        JLabel passwordLabel = new JLabel("Password");
        JTextField passwordEntry = new JTextField(20);

        passwordPanel.add(passwordLabel);
        passwordPanel.add(passwordEntry);

        JButton loginButton = new JButton("Login");
        loginButton.addActionListener(new VerifyUser(usernameEntry, passwordEntry));
        JLabel registerLabel = new JLabel("Don't have an account? Register here");

        loginFrame.add(loginPanel);

        addComponent(loginLabel, loginPanel);
        //addComponent(usernameLabel, loginPanel);
        //addComponent(usernameEntry, loginPanel);
        addComponent(usernamePanel, loginPanel);
        loginPanel.add(Box.createVerticalGlue());
        //addComponent(passwordLabel, loginPanel);
        //addComponent(passwordEntry, loginPanel);
        addComponent(passwordPanel, loginPanel);
        addComponent(loginButton, loginPanel);

        loginFrame.setVisible(true);
    }

    /*
    private String userContent() {
        // return
    }
     */


    private static void addComponent(JComponent component, Container container) {
        component.setAlignmentX(Component.CENTER_ALIGNMENT);
        container.add(component);
    }


    @Override
    public void mouseClicked(MouseEvent e) {
        LoginFrame();
    }

    @Override
    public void mousePressed(MouseEvent e) {

    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }
}

class VerifyUser implements ActionListener {
    JTextField userField;
    JTextField passField;
    public VerifyUser(JTextField userField, JTextField passField) {
        this.userField = userField;
        this.passField = passField;
    }
    @Override
    public void actionPerformed(ActionEvent actionEvent) {
        if (correctCred(userField.getText(), passField.getText())) {
            //UserProfile profileTab = new UserProfile();
            CompileEmail emailTab = new CompileEmail();
        }
    }
    public boolean correctCred(String username, String password) {
        try {
            MysqlDataSource dataSource = new MysqlDataSource();
            dataSource.setUser("root");
            dataSource.setPassword("");
            dataSource.setServerName("localhost");
            dataSource.setDatabaseName("fyp");

            Connection conn = dataSource.getConnection();

            // Check if username and password are the same as in the database
            String usernameCounter;
            PreparedStatement preparedStmt = conn.prepareStatement("SELECT * FROM user order by username desc");
            ResultSet rs = preparedStmt.executeQuery();
            if (rs.next()) {
                usernameCounter = rs.getString("username");
                if (username.equals(username)) {
                    EncryptPass decrypter = new EncryptPass();
                    boolean passMatch = decrypter.checkPass(password, rs.getString("password"));
                    if (passMatch) {
                        JOptionPane.showMessageDialog(null,
                                "Welcome " + username + "! You are being logged in" );
                        UserSession.getInstance(username);
                        return true;
                    } else {
                        throw new InvalidCredException("Invalid password");
                    }
                } else {

                    throw new InvalidCredException("Invalid username");
                }
            }
            rs.close();
            preparedStmt.close();
            conn.close();
            return false;

            //EncryptPass decrypter = new EncryptPass();
            //boolean hashedPassword = decrypter.checkPass();
        } catch (Exception ex) {
            System.err.println("Got an error in login page");
            System.err.println(ex.getMessage());
            return false;
        }
    }
}

class InvalidCredException extends Exception {
    public InvalidCredException(String errorMessage) {
        super(errorMessage);
    }
}