import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.jsoup.Jsoup;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SearchByUrl {

    private final static String SOURCE_FILE_PATH = "C:/Users/Administrator/Desktop/input-2-1.xlsx";
    private final static String SOURCE_SHEET_NAME = "Sheet2";
    private final static Integer BEGIN_ROW = 1;
    private final static Integer TITLE_COL = 1;
    private final static Integer URL_COL = 8;
    private final static String GENERATE_FILE_PATH = "C:/Users/Administrator/Desktop/resultSearchByUrl.xlsx";
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
        String regEx_html = "<[^>]+>";
        Pattern p_html = Pattern.compile(regEx_html, Pattern.CASE_INSENSITIVE);
        Matcher m_html = null;
        //read the search title
        List<String> urlList = readFromExcel(SOURCE_FILE_PATH, SOURCE_SHEET_NAME, URL_COL);
        List<String> titleList = readFromExcel(SOURCE_FILE_PATH, SOURCE_SHEET_NAME, TITLE_COL);
        Map<String, String> titleMap = new HashMap<>();
        for (String str : titleList) {
            titleMap.put(str.toUpperCase(), str);
        }
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        XSSFWorkbook wb = new XSSFWorkbook();
        Sheet sheet = wb.createSheet(GENERATE_SHEET_NAME);
        String title = null;
        String url = null;
        ResponseEntity<String> searchResult = null;
        Row row = null;
        row = sheet.createRow(0);
        Cell cell = null;
        cell = row.createCell(0);
        cell.setCellValue("url");
        cell = row.createCell(1);
        cell.setCellValue("title");
        String documentStr = null;
        Boolean flag = null;
//        for (int i = 0; i < urlList.size(); i++) {
        for(int i=0;i<100;i++){
            flag = false;
            RestTemplate restTemplate = new RestTemplate();
            int random = (int) (Math.random() * userAgents.length);
            System.out.println(i);
            headers.set("user-agent", userAgents[random]);
            HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
            Thread.sleep(random * 100);
            url = urlList.get(i);
            row = sheet.createRow(i + 1);
            cell = row.createCell(0);
            cell.setCellValue(url);
            try {
                searchResult = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);
                documentStr = Jsoup.parse(searchResult.getBody()).selectFirst("h1.heading-large.heading-spacing--small").toString();
                m_html = p_html.matcher(documentStr);
                System.out.println(m_html.replaceAll("").trim());
                title=m_html.replaceAll("").trim().toUpperCase();
                if (titleMap.containsKey(title)) {
                    cell = row.createCell(1);
                    cell.setCellValue(title);
                    flag = true;
                }
                if (flag) {
                    titleMap.remove(title);
                }
            } catch (Exception e) {
                System.out.println("404: url "+ url+" not found");
                continue;
            }
        }
        try {
            //save the answer
            File generateFile = new File(GENERATE_FILE_PATH);
            if (generateFile.exists()) {
                generateFile.delete();
            }
            wb.write(new FileOutputStream(GENERATE_FILE_PATH));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<String> readFromExcel(String filePath, String sheetName, int col) {
        List<String> result = new ArrayList<>();
        FileInputStream fis = null;
        try {
            fis = new FileInputStream(filePath);
            try {
                XSSFWorkbook wb = new XSSFWorkbook(fis);
                Sheet sheet = wb.getSheet(sheetName);
                Row row = null;
                Cell cell = null;
                for (int i = BEGIN_ROW; i < sheet.getLastRowNum(); i++) {
                    row = sheet.getRow(i);
                    cell = row.getCell(col - 1);
                    if (!(cell == null || cell.getCellType() == XSSFCell.CELL_TYPE_BLANK)) {
                        result.add(cell.getStringCellValue());
                    }
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
