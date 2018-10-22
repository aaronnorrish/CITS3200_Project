import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.io.*;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
//the file path setting things refer to GoogleSearchV1 in same style
public class BingSearch {

    private final static String SOURCE_FILE_PATH = "C:/Users/Administrator/Desktop/output (3).xlsx";
    private final static String SOURCE_SHEET_NAME = "journals";
    private final static String DEFAULT_PAGE_NUM = "1";
    private final static String DEFAULT_ROW_NUM = "2";
    private final static Integer BEGIN_ROW = 1;
    private final static String DEFAULT_TYPE = "json";
    private final static String GENERATE_FILE_PATH = "C:/Users/Administrator/Desktop/resultBing.xlsx";
    private final static String GENERATE_SHEET_NAME = "Sheet 1";
    private final static String[] userAgents=new String[]{"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"};

    public static void main(String[] args) throws Exception{
        List<String> searchTitle = readFromExcel(SOURCE_FILE_PATH, SOURCE_SHEET_NAME);
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.ALL));
        XSSFWorkbook wb = new XSSFWorkbook();
        Sheet sheet = wb.createSheet(GENERATE_SHEET_NAME);
        String title = null;
        ResponseEntity<String> searchResult = null;
        Row row = null;
        row=sheet.createRow(0);
        Cell cell = null;
        cell=row.createCell(0);
        cell.setCellValue("title");
        cell=row.createCell(1);
         cell.setCellValue("url");
        Document document = null;
        Elements elements = null;
        Element element = null;
//        for (int i = 0; i < searchTitle.size(); i++) {
        for (int i = 0; i < 100; i++) {
            RestTemplate restTemplate = new RestTemplate();
            int random=(int)(Math.random()*userAgents.length);
            System.out.println(i);
            headers.set("user-agent",userAgents[random]);
            HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
            Thread.sleep(random*100);
            title = URLEncoder.encode(searchTitle.get(i),"UTF8");
            String url="https://www.bing.com/search?q="+title+"&go=Search&form=QBLH&pq="+title+"&first=1";
            System.out.println(headers.get("user-agent"));
            System.out.println(url);
            searchResult = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);
            row = sheet.createRow(i+1);
            cell=row.createCell(0);
            cell.setCellValue(searchTitle.get(i));
            document = Jsoup.parse(searchResult.getBody());
            elements = document.selectFirst("#b_results").select(".b_algo");
//            for (int j = 0; j < elements.size(); j++) {
            for (int j = 0; j < elements.size(); j++) {
                element=elements.get(j);
                cell = row.createCell(1);
                String rawString=element.selectFirst("h2").select("a").attr("href");
                try{
                    cell.setCellValue(rawString);
                    System.out.println(cell.getStringCellValue());
                    break;
                }catch(Exception e){
                    continue;
                }
            }
        }
        try {
            File generateFile = new File(GENERATE_FILE_PATH);
            if (generateFile.exists()) {
                generateFile.delete();
            }
            wb.write(new FileOutputStream(GENERATE_FILE_PATH));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<String> readFromExcel(String filePath, String sheetName) {
        List<String> result = new ArrayList<>();
        FileInputStream fis = null;
        try {
            fis = new FileInputStream(filePath);
            try {
                XSSFWorkbook wb = new XSSFWorkbook(fis);
                Sheet sheet = wb.getSheet(sheetName);
                Row row = null;
                for (int i = BEGIN_ROW; i < sheet.getLastRowNum(); i++) {
                    row = sheet.getRow(i);
                    result.add(String.valueOf(row.getCell(0)));
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } finally {
            if (fis != null) {
                try {
                    fis.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return result;
    }
}
