// Inspiration code: https://stackoverflow.com/questions/24427092/how-to-make-a-java-gridbaglayout-with-six-rows-and-2-columns
import javax.swing.*;
import javax.swing.plaf.InsetsUIResource;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CompileEmail {
    JTextField recipientsField;
    JTextField ccField;
    JTextArea contentField;
    public CompileEmail() {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (ClassNotFoundException | InstantiationException |
                        IllegalAccessException | UnsupportedLookAndFeelException ex) {
                    ex.printStackTrace();
                }
                JFrame frame = new JFrame("Compile Email");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setSize(600, 600);
                // frame.setLayout(new GridBagLayout());

                JPanel mainPanel = new JPanel();
                mainPanel.setLayout(new BoxLayout(mainPanel, BoxLayout.Y_AXIS));
                frame.add(mainPanel);

                JPanel recipientsPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 3, 3));
                JLabel recipientsLabel = new JLabel("Recipients:");
                recipientsField = new JTextField(20);
                recipientsPanel.add(recipientsLabel);
                recipientsPanel.add(recipientsField);


                JPanel ccPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 3, 3));
                JLabel ccLabel = new JLabel("Cc:");
                ccField = new JTextField(20);
                ccPanel.add(ccLabel);
                ccPanel.add(ccField);

                JPanel contentPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 3, 3));
                JLabel contentLabel = new JLabel("Content:");
                contentField = new JTextArea(40, 50);
                contentPanel.add(contentLabel);
                contentPanel.add(contentField);

                JButton send = new JButton("Send");


                mainPanel.add(recipientsPanel);
                mainPanel.add(ccPanel);
                mainPanel.add(contentPanel);
                mainPanel.add(send);

                send.addActionListener(new SendEmail(recipientsField, ccField, contentField));

                frame.setVisible(true);
            }
        });

    }
    public JPanel createPane(Color color) {
        JPanel pane = new JPanel() {
            @Override
            public Dimension getPreferredSize() {
                return new Dimension(50, 50);
            }
        };
        pane.setBackground(color);
        return pane;
    }

    /*
    public void sendEmail() implements ActionListener

    {
        String recipient = recipientsField.getText();
        String cc = ccField.getText();
        String content = contentField.getText();
    }
     */
}


class SendEmail implements ActionListener{
    String recipients;
    String cc;
    String content;
    public SendEmail(JTextField recipients, JTextField cc, JTextArea content) {
        this.recipients = recipients.getText();
        this.cc = cc.getText();
        this.content = content.getText();
    }

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
        SendEmailSMTP sender = new SendEmailSMTP(recipients, cc, content);
    }
}


