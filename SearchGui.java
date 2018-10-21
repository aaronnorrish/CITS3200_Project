import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
// this SearchGUI not finished due time limit
public class SearchGui extends JFrame {

    private JLabel filePathLabel=null;
    private JTextField filePathText=null;
    private JLabel titleLabel=null;
    private JTextField titleText=null;
    private JButton goBtn=null;

    private void init(){
        this.setVisible(true);
        this.setSize(500,300);
//        this.setLayout(new GridLayout(3,4,10,5));
        this.setLayout(new FlowLayout());
        this.setTitle("search gui");
        this.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        filePathLabel=new JLabel();
        filePathLabel.setText("file path");
        filePathText=new JTextField(20);
        titleLabel=new JLabel();
        titleLabel.setText("search title");
        titleText=new JTextField(20);
        goBtn=new JButton();
        goBtn.setText("go");
        JPanel jPanel=new JPanel();
        jPanel.add(filePathLabel);
        jPanel.add(filePathText);
        jPanel.add(titleLabel);
        jPanel.add(titleText);
        jPanel.add(goBtn);
        this.add(jPanel);
//        container.add(jTextField1);
        initListener();
    }

    public void initListener(){
        goBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println(titleText.getText());
            }
        });
    }

    public static void main(String[] args){
        SearchGui searchGui=new SearchGui();
        searchGui.init();
    }
}
