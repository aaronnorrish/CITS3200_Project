
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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by Handong.
 */
public class GoogleSearchV1 {

    //Path for the source file
    private final static String SOURCE_FILE_PATH = "C:/Users/Administrator/Desktop/output (3).xlsx";
    //the sheet name used
    private final static String SOURCE_SHEET_NAME = "journals";
    //Page number is google search
    private final static String DEFAULT_PAGE_NUM = "1";
    //google search result
    private final static String DEFAULT_ROW_NUM = "20";
    //the row number in excel form
    private final static Integer BEGIN_ROW = 4;
    //reuslt save path
    private final static String GENERATE_FILE_PATH = "C:/Users/Administrator/Desktop/resultGoogleV1.xlsx";
    //search result created sheet name
    private final static String GENERATE_SHEET_NAME = "Sheet 1";
    private final static String[] userAgents = new String[]{"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
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
// multi User Agent
    public static void main(String[] args) throws Exception {
        //Read the search title
        List<String> searchTitle = readFromExcel(SOURCE_FILE_PATH, SOURCE_SHEET_NAME);
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        XSSFWorkbook wb = new XSSFWorkbook();
        Sheet sheet = wb.createSheet(GENERATE_SHEET_NAME);
        String title = null;
        ResponseEntity<String> searchResult = null;
        Row row = null;
        Cell cell = null;
        Document document = null;
        Element searchDiv = null;
        Elements gDivs = null;
        Element h3 = null;
        Element a = null;
//        for (int i = 0; i < searchTitle.size(); i++) {
        for (int i = 0; i < 100; i++) {
            //restTemplate
            RestTemplate restTemplate = new RestTemplate();
            int random = (int) (Math.random() * userAgents.length);
            headers.set("user-agent", userAgents[random]);
            HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
            int j = 0;
            System.out.println(i);
            //reduce request speed by sleep Thread,otherwise may blocked with google with error code 503
            Thread.currentThread().sleep(1000);
            title = searchTitle.get(i);
            //start searching
            searchResult = restTemplate.exchange("https://www.google.com/search?q=" + title + "&start=" + DEFAULT_PAGE_NUM + "&num=" + DEFAULT_ROW_NUM, HttpMethod.GET, entity, String.class);
            row = sheet.createRow(i);
            //take result from google
            document = Jsoup.parse(searchResult.getBody());
            //div#search
            searchDiv = document.selectFirst("#search");
            if (searchDiv != null) {
                //seach if have div.g or not
                gDivs = searchDiv.select("div[class=g]");
                if (gDivs != null && gDivs.size() > 0) {
                    for (Element gDiv : gDivs) {
                        //cheack if have h3.r or not
                        h3 = gDiv.selectFirst("h3[class=r]");
                        if (h3 != null) {
                            //check does it have a
                            a = h3.selectFirst("a");
                            if (a != null) {
                                cell = row.createCell(j);
                                //get the link from href，save into cell
                                cell.setCellValue(a.attr("href"));
                                j++;
                                if (j == 2) {
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            //if the result was not link with Journals especially for the Journal's name have wilde means
            //add key words "Journal"
            if (j == 0) {
                title = searchTitle.get(i) + " Journal";
                searchResult = restTemplate.exchange("https://www.google.com/search?q=" + title + "&start=" + DEFAULT_PAGE_NUM + "&num=" + DEFAULT_ROW_NUM, HttpMethod.GET, entity, String.class);
                document = Jsoup.parse(searchResult.getBody());
                searchDiv = document.selectFirst("#search");
                if (searchDiv != null) {
                    gDivs = searchDiv.select("div[class=g]");
                    if (gDivs != null && gDivs.size() > 0) {
                        for (Element gDiv : gDivs) {
                            h3 = gDiv.selectFirst("h3[class=r]");
                            if (h3 != null) {
                                a = h3.selectFirst("a");
                                if (a != null) {
                                    cell = row.createCell(j);
                                    cell.setCellValue(a.attr("href"));
                                    j++;
                                    if (j == 2) {
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        try {
            //Save the file
            File generateFile = new File(GENERATE_FILE_PATH);
            if (generateFile.exists()) {
                generateFile.delete();
            }
            wb.write(new FileOutputStream(GENERATE_FILE_PATH));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //red excel and create a list
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
