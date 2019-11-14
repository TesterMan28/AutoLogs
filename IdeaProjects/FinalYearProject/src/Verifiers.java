import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// InputVerifier 2 for username
class Verifiers implements ActionListener {
    JTextField userField;
    JTextField passField;
    JTextField confirmField;
    UserInterface interfaceInstance;
    //UserInterface interfaceInstance = new UserInterface();
    //JLabel userHint;
    //JLabel passHint;
    public Verifiers(UserInterface interfaceInstance) {
        this.interfaceInstance = interfaceInstance;
        //this.userField = userField;
        //this.passField = passField;
        //this.confirmField = confirmField;
        //this.userHint = userHint;
        //this.passHint = passHint;
    }

    public boolean verifyUsername() {

        userField = (JTextField) interfaceInstance.getComponentByName("userField");
        String input_text = userField.getText();
        // Checking for valid length
        if (input_text.length() < 8 ) {
            System.out.println("The length is: " + input_text.length());
            JOptionPane.showMessageDialog(null, "Username must be greater than 8 characters");
            return false;
        } else {
            return true;
        }

    }
    public boolean verifyPassword() {
        passField = (JTextField) interfaceInstance.getComponentByName("passField");
        String errorMessage = "";
        String input_text = passField.getText();
        // Checking for valid length
        if (input_text.length() < 8 || input_text.length() > 16) {
            errorMessage += "Password must be between 8 and 16 characters\n";

        }
        // Must have at least one uppercase character
        boolean hasUppercase = !input_text.equals(input_text.toLowerCase());
        if (!hasUppercase) {
            errorMessage += "Password must contain at least 1 uppercase character\n";
        }
        // Must have at least one lowercase character
        boolean hasLowercase = !input_text.equals(input_text.toUpperCase());
        if (!hasLowercase) {
            errorMessage += "Password must contain at least 1 lowercase character\n";
        }
        // Must have at least one digit
        Pattern p1 = Pattern.compile(".*\\d.*");
        Matcher m1 = p1.matcher(input_text);
        boolean b1 = m1.matches();
        if (!b1) {
            errorMessage += "Password must contain at least one digit\n";
        }
        // Must have at least one symbol
        Pattern p2 = Pattern.compile(".*[@#$%].*");
        Matcher m2 = p2.matcher(input_text);
        boolean b2 = m2.matches();
        if (!b2) {
            errorMessage += "Password must contain at least one symbol. eg (@#$%)\n";
        }
        if (errorMessage.length() > 0) {
            JOptionPane.showMessageDialog(null, errorMessage);
            return false;
        }
        System.out.println("Password accepted");
        return true;
    }
    public boolean confirmPassword() {
        confirmField = (JTextField) interfaceInstance.getComponentByName("confirmField");
        if (Objects.equals(passField.getText(), confirmField.getText())) {
            System.out.println("Password confirmed");
            return true;
        } else {
            return false;
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // If all return successful then insert field into database
        if (verifyUsername() && verifyPassword() && confirmPassword()) {
            // Encrypt password before sending it to the database
            EncryptPass encrypter = new EncryptPass();
            String encryptedPass = encrypter.hashPass(passField.getText());
            // Establish database connection and insert into
            System.out.println("Username passed: " + userField.getText());
            System.out.print("Password passed: " + encryptedPass);
            RegisterUser register = new RegisterUser();
            register.register(userField.getText(), encryptedPass);
        } else {
            System.err.println("Confirm password field not here");
            //JLabel userHint = Component.getName();
        }
    }
}