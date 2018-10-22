
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
public class GoogleSearchV2 {

    //path settings refer to GoogleSearch or Users guid
    private final static String SOURCE_FILE_PATH = "C:/Users/Administrator/Desktop/output (3).xlsx";

    private final static String SOURCE_SHEET_NAME = "journals";

    private final static String DEFAULT_PAGE_NUM = "1";

    private final static String DEFAULT_ROW_NUM = "20";

    private final static Integer BEGIN_ROW = 4;

    private final static String GENERATE_FILE_PATH = "C:/Users/Administrator/Desktop/resultGoogleV2.xlsx";

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

    public static void main(String[] args) throws Exception {
        //read title
        List<SearchObj> searchObjList = readFromExcel(SOURCE_FILE_PATH, SOURCE_SHEET_NAME);
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
            //Thread Sleep
            Thread.currentThread().sleep(1000);
            title = searchObjList.get(i).getTitle()+" "+searchObjList.get(i).getPublisher();
            //start searching
            searchResult = restTemplate.exchange("https://www.google.com/search?q=" + title + "&start=" + DEFAULT_PAGE_NUM + "&num=" + DEFAULT_ROW_NUM, HttpMethod.GET, entity, String.class);
            row = sheet.createRow(i);
            //return google result
            document = Jsoup.parse(searchResult.getBody());
            //seach div#search
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
            //replace the ELE key words into any other column
            //it can be changed with journal title + publishers or journal tile with ISSN
            if (j == 0) {
                title = searchObjList.get(i).getTitle() + " ELE"+searchObjList.get(i).getPublisher();
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
            //save result
            File generateFile = new File(GENERATE_FILE_PATH);
            if (generateFile.exists()) {
                generateFile.delete();
            }
            wb.write(new FileOutputStream(GENERATE_FILE_PATH));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //read tile
    private static List<SearchObj> readFromExcel(String filePath, String sheetName) {
        List<SearchObj> result = new ArrayList<>();
        FileInputStream fis = null;
        try {
            fis = new FileInputStream(filePath);
            try {
                XSSFWorkbook wb = new XSSFWorkbook(fis);
                Sheet sheet = wb.getSheet(sheetName);
                Row row = null;
                for (int i = BEGIN_ROW; i < 104; i++) {
                    row = sheet.getRow(i);
                    SearchObj searchObj=new SearchObj();
                    searchObj.setTitle(String.valueOf(row.getCell(0)));
                    searchObj.setPublisher(String.valueOf(row.getCell(1)));
                    searchObj.setIssn(String.valueOf(row.getCell(2)));
                    searchObj.seteIssn(String.valueOf(row.getCell(3)));
                    searchObj.setCountry(String.valueOf(row.getCell(4)));
                    searchObj.setLanguage(String.valueOf(row.getCell(5)));
                    searchObj.setCategory(String.valueOf(row.getCell(6)));
                    result.add(searchObj);
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
