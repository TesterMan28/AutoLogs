import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class UserProfile {
    public UserProfile() {
        UserSession currentSession = UserSession.getInstance("");
        JFrame userFrame = new JFrame("User Profile");
        userFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        userFrame.setSize(500, 500);
        userFrame.setLocationRelativeTo(null);

        JPanel userDetails = new JPanel();
        userDetails.setLayout(new BoxLayout(userDetails, BoxLayout.Y_AXIS));

        JLabel mainLabel = new JLabel("User Profile");
        mainLabel.setFont(new Font("Courier New", Font.BOLD, 30));

        // Username panel
        JPanel usernamePanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 5, 5));
        JLabel usernameLabel = new JLabel("Username");
        JTextField usernameField = new JTextField(currentSession.getUsername(), 20);
        usernamePanel.add(usernameLabel);
        usernamePanel.add(usernameField);

        // Email panel
        JPanel emailPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 5, 5));
        JLabel emailLabel = new JLabel("Email");
        JTextField emailField = new JTextField(20);
        emailPanel.add(emailLabel);
        emailPanel.add(emailField);

        // Button to update profile
        JButton update = new JButton("Update");
        update.addActionListener(new EmailVerify(emailField));

        // Main panel add
        userDetails.add(usernamePanel);
        userDetails.add(emailPanel);
        userDetails.add(update);

        // Main frame add
        userFrame.add(userDetails);
        userFrame.setVisible(true);
    }

    class EmailVerify implements ActionListener {
        JTextField emailField;
        public EmailVerify(JTextField emailField) {
            this.emailField = emailField;
        }
        @Override
        public void actionPerformed(ActionEvent actionEvent) {
            if (emailField.getText() != null) {
                String regex = "^([_a-zA-Z0-9-]+(\\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*(\\.[a-zA-Z]{1,6}))?$";
                Pattern pattern = Pattern.compile(regex);
                Matcher matcher = pattern.matcher(emailField.getText());
                if (!matcher.matches()) {
                    System.out.println("\nNot a valid email\n");
                } else {
                    System.out.println("\nThat is a valid email\n");
                }
            }
        }
    }
    /*
    public HashMap<String, String> userInformation() {
        MysqlDataSource dataSource = new MysqlDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("");
        dataSource.setServerName("localhost");
        dataSource.setDatabaseName("fyp");


    }

     */
}
