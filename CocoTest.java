import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.*;
import java.net.URLDecoder;

/**
 * Created by Handong.
 */
public class CocoTest {

    public static void main(String[] args) throws IOException {
//        StringBuilder stringBuilder=new StringBuilder("");
//        File file=new File("C:/Users/Administrator/Desktop/test.html");
//        FileInputStream fis=null;
//        try {
//            fis=new FileInputStream(file);
//            byte[] buffer=new byte[1024];
//            int length=0;
//            while((length=fis.read(buffer,0,1024))!=-1){
//                stringBuilder.append(new String(buffer));
//            }
//            System.out.println(stringBuilder);
//        } catch (FileNotFoundException e) {
//            e.printStackTrace();
//        }
//
//        Document doc= Jsoup.parse(String.valueOf(stringBuilder));
//        Elements elements=doc.select(".g");
//        for(Element ele:elements){
//            System.out.println(ele.select(".r").select("a").first().attr("href").substring(7));
//        }
//        System.out.println(elements);
        System.out.println(URLDecoder.decode("%E6%8F%90%E4%BA%A4"));
    }
}
