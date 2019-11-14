import java.util.logging.Logger;

public class EncryptPass {
    // private static final Logger logg = LoggerFactory.get
    // String hashed = BCrypt.hashpw();
    /*
    String plainTextPassword;
    public EncryptPass(String plainTextPassword) {
        this.plainTextPassword = plainTextPassword;
    }
     */

    public static String hashPass(String plainTextPassword) {
        System.out.println(BCrypt.hashpw(plainTextPassword, BCrypt.gensalt()));
        return BCrypt.hashpw(plainTextPassword, BCrypt.gensalt());
    }

    public boolean checkPass(String plainPassword, String hashedPassword) {
        if (BCrypt.checkpw(plainPassword, hashedPassword)) {
            // System.out.println("The password matches");
            return true;
        } else {
            // System.out.println("The password does not match.");
            return false;
        }
    }
}

