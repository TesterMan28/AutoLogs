import com.sun.mail.smtp.SMTPTransport;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.Date;
import java.util.Properties;

public class SendEmailSMTP {

    // for example, smtp.mailgun.org
    /*
    private static final String SMTP_SERVER = "smtp.mailgun.org";
    private static final String USERNAME = "sandbox26af3b72848944f6b0df74e40a50dff1.mailgun.org";
    private static final String PASSWORD = "";

    private static final String EMAIL_FROM = "testwork323@gmail.com";
    private static final String EMAIL_TO = "testwork323@gmail.com";
    private static final String EMAIL_TO_CC = "";

    private static final String EMAIL_SUBJECT = "Test Send Email via SMTP";
    private static final String EMAIL_TEXT = "Hello Java Mail \n 123";
     */

    /*
    public static void main(String[] args) {
        SendEmailSMTP smtpInstance = new SendEmailSMTP();
    }

     */


    // public SendEmailSMTP() {
    public SendEmailSMTP(String recipient, String cc, String content) {
        final String username = "testwork323@gmail.com";
        final String password = "ntpdeyojsvdwczds";

        Properties prop = new Properties();
        prop.put("mail.smtp.host", "smtp.gmail.com");
        prop.put("mail.smtp.port", "587");
        prop.put("mail.smtp.auth", "true");
        prop.put("mail.smtp.starttls.enable", "true"); //TLS

        Session session = Session.getInstance(prop,
                new javax.mail.Authenticator() {
                    protected PasswordAuthentication getPasswordAuthentication() {
                        return new PasswordAuthentication(username, password);
                    }
                });

        try {

            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress("testwork323@gmail.com"));
            message.setRecipients(
                    Message.RecipientType.TO,
                    InternetAddress.parse(recipient)
            );
            message.setRecipients(Message.RecipientType.CC, InternetAddress.parse(cc));
            message.setSubject("Testing Gmail TLS");
            //message.setText("Dear Mail Crawler,"
            //        + "\n\n Please do not spam my email!");
            message.setText(content);

            Transport.send(message);

            System.out.println("Done");

        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
}
