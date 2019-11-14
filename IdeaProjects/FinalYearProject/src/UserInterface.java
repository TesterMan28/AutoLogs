// 10:09, 10/11: Implement CheckPasswordStrength. Look at CardLayout for top menu
// 23:44, 7/11: TODO: Check why cant pass JTextField values
// 16:51, 19/10: TODO: Add ActionListener/ActionHandler for imageMenu item
// 16:51, 19/10: TODO: May not need to use Action as it is recommended to use IF 2 or more components have the same function
// https://docs.oracle.com/javase/tutorial/uiswing/components/icon.html#getresource

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class UserInterface implements ActionListener, MouseListener {
    HashMap componentMap;
    JFrame frame;
    JPanel userPanel;
    JPanel passPanel;
    JPanel confirmPanel;
    public static void main(String[] args) {
        UserInterface instance = new UserInterface();


        /*

        frame.getContentPane().add(button1); // Adds Button to content pane of frame
        frame.getContentPane().add(button2); // Adds Button to content pane of frame
        frame.setVisible(true);
        */

    }
    public UserInterface() {


        frame = new JFrame("My first gui");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(900,900);
        frame.setLayout(new BorderLayout());

        // Content for top section
        JMenuBar topMenuBar = new JMenuBar();
        topMenuBar.setLayout(new FlowLayout(FlowLayout.LEFT));
        JMenu fileMenu = new JMenu("File");
        JMenu helpMenu = new JMenu("Help");
        JMenuItem open, save, profile, settings, log;
        open = fileMenu.add("Open");
        save = fileMenu.add("Save as");
        // Display an icon

        ImageIcon icon = createImageIcon("rui tachibana.jpg", "Cool pic");
        // Resize the ImageIcon above. Added 19/10/2019, 16:21. https://stackoverflow.com/questions/2856480/resizing-a-imageicon-in-a-jbutton?newreg=5486e301ce5940f68a8b3eb372eaf02d
        Image img = icon.getImage();
        Image newImg = img.getScaledInstance(20, 20, Image.SCALE_SMOOTH);
        icon = new ImageIcon(newImg);

        // Trying to add a custom image JMenu
        JMenu imageMenu = new JMenu();
        imageMenu.setIcon(icon);
        profile = imageMenu.add("Profile");
        settings = imageMenu.add("Settings");


        /*
        JLabel imageLabel = new JLabel(icon) {
            @Override
            public void paintComponent(Graphics g) {
                super.paintComponent(g);
                if (icon != null) {
                    // Interest point
                    g.drawImage(icon.getImage(), 0, 0, getWidth(), getHeight(), null);
                }
            }
        };
         */



        // Create a sample action for learning. https://docs.oracle.com/javase/tutorial/uiswing/misc/action.html
        Action leftAction = new LeftAction("Go left", icon, "This is the left button.", new Integer(KeyEvent.VK_L));
        JButton testButton = new JButton(leftAction);
        JButton anotherButton = new JButton(leftAction);

        // Different style for creating profile image. https://stackoverflow.com/questions/24397792/how-to-fill-the-surface-of-the-jbutton-completely-with-an-imageicon
        JButton anotherButton2 = new JButton();
        anotherButton2.setForeground(Color.RED);
        anotherButton2.setFocusPainted(true);
        anotherButton2.setContentAreaFilled(false);
        anotherButton2.setMargin(new Insets(0,0,0,0));
        anotherButton2.setIcon(icon);


        // Add components to top menu bar
        topMenuBar.add(fileMenu);
        topMenuBar.add(helpMenu);
        topMenuBar.add(testButton);
        topMenuBar.add(anotherButton);
        topMenuBar.add(anotherButton2);
        topMenuBar.add(imageMenu);

        // Add components to middle panel
        JPanel midPanel = new JPanel();
        midPanel.setLayout(new BoxLayout(midPanel, BoxLayout.Y_AXIS));
        /*
        JPanel midPanel = new JPanel(new GridBagLayout());
        boolean shouldFill = true;
        boolean shouldWeightX = true;

        GridBagConstraints mc = new GridBagConstraints();
        if (shouldFill) {
            // natural height, maximum width
            mc.fill = GridBagConstraints.HORIZONTAL;
        }

        if (shouldWeightX) {
            mc.weightx = 0.5;
        }

         */






        // Custom class to add user entry fields
        CreateEntry createFields = new CreateEntry();

        // User panel
        /*
        boolean shouldFill = true;
        JPanel userPanel = new JPanel(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        if (shouldFill) {
            c.fill = GridBagConstraints.HORIZONTAL;
        }

         */

        JLabel userLabel = new JLabel("Username:");
        JTextField user = new JTextField(20);
        JLabel userHint = new JLabel("Test hint label");


        JTextField pass = new JTextField(20);
        JTextField confirm_pass = new JTextField(20);
        JButton register = new JButton("Register");
        //register.addActionListener(new Verifiers(user, pass, confirm_pass));


        JPanel usernamePanel = createFields.addEntry("Username", "Username", "userField", 20,"userHint", "userHint");
        userPanel = usernamePanel;
        usernamePanel.setAlignmentX(Component.CENTER_ALIGNMENT);
        midPanel.add(usernamePanel);
        //midPanel.add(createFields.addEntry("Trump", "Trump", "TrumpField", 20,"TrumpHint", "TrumpHint"));

        //mc.gridx = 1;
        //mc.gridy = 1;
        JPanel passwordPanel = createFields.addEntry("Password", "Password", "passField", 20, "passHint", "passHint");
        passPanel = passwordPanel;
        passwordPanel.setAlignmentX(Component.CENTER_ALIGNMENT);
        midPanel.add(passwordPanel);
        //midPanel.add(createFields.addEntry("Obama", "Obama", "ObamaField", 20, "ObamaHint", "ObamaHint"));

        JPanel confirmpassPanel = createFields.addEntry("Confirm", "Confirm Password", "confirmField", 20, "confirmHint", "confirmpassHint");
        confirmPanel = confirmpassPanel;
        passwordPanel.setAlignmentX(Component.CENTER_ALIGNMENT);
        midPanel.add(confirmpassPanel);

        // this.createComponentMap();

        // register.addActionListener(new Verifiers(this));


        JLabel login = new JLabel("Log In");
        login.addMouseListener(new LoginPage());

        register.setAlignmentX(Component.CENTER_ALIGNMENT);
        midPanel.add(register);

        midPanel.add(login);


        // Content for bottom section
        JMenuBar botMenuBar = new JMenuBar();
        botMenuBar.setLayout(new FlowLayout());
        JLabel enterLabel = new JLabel("Enter Text");
        JTextField enterText = new JTextField(20);
        JButton send = new JButton("Send");
        send.addActionListener(this);
        JButton reset = new JButton("Reset");

        botMenuBar.add(enterLabel);
        botMenuBar.add(enterText);
        botMenuBar.add(send);
        botMenuBar.add(reset);



        // Adding sections to main frame
        frame.add(topMenuBar, BorderLayout.NORTH);
        frame.add(midPanel, BorderLayout.CENTER);
        frame.add(botMenuBar, BorderLayout.SOUTH);
        frame.setVisible(true);

        // Adding action listeners to components
        this.createComponentMap();
        register.addActionListener(new Verifiers(this));


        //this.createComponentMap();
    }

    /*
    private void createComponentMap() {
        componentMap = new HashMap<String, Component>();
        componentMap.put()
    }
     */


    private void createComponentMap() {
        componentMap = new HashMap<String, Component>();
        Component[] userComponents = userPanel.getComponents();
        Component[] passComponents = passPanel.getComponents();
        Component[] confirmComponents = confirmPanel.getComponents();
        Component[] both = Stream.concat(Arrays.stream(userComponents), Arrays.stream(passComponents))
                .toArray(Component[]::new);
        Component[] components = Stream.concat(Arrays.stream(both), Arrays.stream(confirmComponents))
                .toArray(Component[]::new);
        // Print contents in components
        for (int x = 0; x < components.length; x++) {
            System.out.println(components[x].getName());
        }
        for (int i=0; i < components.length; i++) {
            componentMap.put(components[i].getName(), components[i]);
        }
    }


    public JComponent getComponentByName(String name) {
        if (componentMap.containsKey(name)) {
            return (JComponent) componentMap.get(name);
        } else {
            return null;
        }
    }




    class CreateEntry {
        final static boolean shouldFill = true;
        final static boolean shouldWeightX = true;
        public JPanel addEntry(String labelName, String labelText, String textName, int textSize, String hintName, String hint) {
            JPanel fieldPanel = new JPanel();
            fieldPanel.setLayout(new GridBagLayout());
            GridBagConstraints c = new GridBagConstraints();
            JLabel label = new JLabel(labelText);
            label.setName(labelName);

            if (shouldFill) {
                // natural height, maximum width
                //c.fill = GridBagConstraints.HORIZONTAL;
            }

            if (shouldWeightX) {
                //c.weightx = 0.5;
            }
            //c.fill = GridBagConstraints.HORIZONTAL;
            c.gridx = 0;
            c.gridy = 0;
            c.insets = new Insets(0, 3, 3, 0);
            fieldPanel.add(label, c);

            JTextField entry = new JTextField(textSize);
            entry.setName(textName);
            //c.fill = GridBagConstraints.HORIZONTAL;
            c.gridx = 1;
            c.gridy = 0;
            fieldPanel.add(entry, c);

            JLabel hintLabel = new JLabel(hint);
            hintLabel.setName(hintName);
            hintLabel.setVisible(false);
            // hintLabel.setVisible(false);
            //c.fill = GridBagConstraints.HORIZONTAL;
            c.gridx = 1;
            c.gridy = 1;
            fieldPanel.add(hintLabel, c);

            return fieldPanel;
        }
    }



    public void displayResult(String actionDescription, ActionEvent e) {
        String s = ("Action event detected: " + actionDescription + "." + " Event source: " + e.getSource());
        System.out.println(s);
    }

    class LeftAction extends AbstractAction {
        public LeftAction(String text, ImageIcon icon, String desc, Integer mnemonic) {
            super(text, icon);
            putValue(SHORT_DESCRIPTION, desc);
            putValue(MNEMONIC_KEY, mnemonic);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            displayResult("Action for some button", e);
        }
    }

    /* Method for loading image. Returns an ImageIcon, or null if the path is invalid */
    protected ImageIcon createImageIcon(String path, String description) {
        java.net.URL imgURL = getClass().getResource(path);
        if (imgURL != null) {
            return new ImageIcon(imgURL, description);
        } else {
            System.err.println("Couldn't find file: " + path);
            return null;
        }
    }
    public void actionPerformed(ActionEvent e) {
        System.out.println("Action listener works");
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

    public void mouseClicked(MouseEvent e) { System.out.println("Mouse click!");}
}


