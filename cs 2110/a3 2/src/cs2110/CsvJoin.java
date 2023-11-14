package cs2110;

/*
 *
 * Name(s) and NetID(s): Aileen Huang (aeh245)
 * Hours spent on assignment: 20
 */


import javax.swing.tree.ExpandVetoException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class CsvJoin {


    /**
     * Load a table from a Simplified CSV file and return a row-major list-of-lists representation.
     * The CSV file is assumed to be in the platform's default encoding. Throws an IOException if
     * there is a problem reading the file.
     */
    public static Seq<Seq<String>> csvToList(String file) throws IOException {
        try (FileReader file_read = new FileReader(file)) {
            Scanner content = new Scanner(file_read); //scans the whole file
            Seq<Seq<String>> list_listOfStr = new LinkedSeq<>();
            //want to access each line:
            while (content.hasNextLine()) {
                //want to access each word of each line
                String line = content.nextLine();
                String[] tokens = line.split(",", -1);

                Seq<String> listOfStr = new LinkedSeq<>();
                //Need to append each token as a node to listOfStr
                for (String token : tokens) {
                    listOfStr.append(token);
                }

                //System.out.println(listOfStr.toString());
                list_listOfStr.append(listOfStr);
                //System.out.println(list_listOfStr.toString());
            }
            file_read.close();
            return list_listOfStr;
        }

    }

    /**
     * Return the left outer join of tables `left` and `right`, joined on their first column. Result
     * will represent a rectangular table, with empty strings filling in any columns from `right`
     * when there is no match. Requires that `left` and `right` represent rectangular tables with at
     * least 1 column.
     */
    public static Seq<Seq<String>> join(Seq<Seq<String>> left, Seq<Seq<String>> right) {
        //rectangular tables: each row has same number of columns
        assert rectangularTable(left);
        assert rectangularTable(right);

        //Create a list for rows
        Seq<Seq<String>> listOfcombinedList = new LinkedSeq<>();

        //For each row on left table, search through all rows on right table
        int leftSize = left.size();
        for (int i = 0; i < leftSize; i++) {
            int rightSize = right.size();
            //Create a brand new list for each row
            int num_matches = 0;
            for (int j = 0; j < rightSize; j++) {
                if (left.get(i).get(0).equals(right.get(j).get(0))) {
                    Seq<String> combinedListofStr = new LinkedSeq<>();

                    //Append each element from left and right table
                    int leftRowSize = left.get(i).size();
                    int rightRowSize = right.get(j).size();
                    //combinedListofStr.append(left.get(i).get(0));
                    //System.out.println(right.get(j).get(0) + left.get(i).get(0));

                    for (int k = 0; k < leftRowSize; k++) {
                        combinedListofStr.append(left.get(i).get(k));
                        // System.out.println("leftrowappend" + combinedListofStr);
                    }
                    //System.out.println(rightRowSize);
                    for (int m = 1; m < rightRowSize; m++) {
                        combinedListofStr.append(right.get(j).get(m));
                        // System.out.println("right rowappend" + combinedListofStr);
                        //  System.out.println("right row value" + right.get(j).get(m));
                    }
                    //  System.out.println(" combined list" + combinedListofStr);
                    //System.out.println(combinedListofStr + "added row");
                    listOfcombinedList.append(combinedListofStr);
                    num_matches += 1;
                }
            }
            if (num_matches == 0) {
                Seq<String> combinedListofStr = new LinkedSeq<>();
                for (int k = 0; k < left.get(i).size(); k++) {
                    combinedListofStr.append(left.get(i).get(k));
                }
                for (int m = 1; m < right.get(m).size(); m++) {
                    combinedListofStr.append("");
                }
                //System.out.println(combinedListofStr + "added row");
                listOfcombinedList.append(combinedListofStr);
            }


            //Append these row lists

            //System.out.println(listOfcombinedList+"final");

        }
        return listOfcombinedList;


    }

    /**
     *
     * Returns whether table (represented as a nested linked sequence) is a rectangular table.
     * A rectangular table has the same number of columns for each row.
     */
    private static boolean rectangularTable(Seq<Seq<String>> table) {
        //need at least one node in each row
        if (table.size() == 0) {
            return false;
        }
        if (table.size() == 1) {
            if (table.get(0).size() >= 1) {
                return true;
            }
            if (table.get(0).size() == 0) {
                return false;
            }
        }

        if (table.size() >= 2) {
            //get the size of each row and check
            int rowSize = table.get(0).size();

            //for each row
            for (int i = 0; i < table.size(); i++) {
                //check if rowSize == size of row
                if (rowSize != table.get(i).size()) {
                    return false;
                }
            }

        }
        return true;

    }

    public static void main(String[] args) throws IOException {
        //pass two arguments, print error msg if there are file-reading issues
        //do not output a string
       //test: System.out.println("a" + "\r\n" + "h");
        try {
            Seq<Seq<String>> leftTableList = CsvJoin.csvToList(args[0]);
            System.err.println("Issue with reading left table: input1.csv");
            Seq<Seq<String>> rightTableList = CsvJoin.csvToList(args[1]);
            System.err.println("Trouble with reading right table: input2.csv");
            Seq<Seq<String>> combinedList = CsvJoin.join(leftTableList, rightTableList);
            System.err.println("Assertion Error: One of the tables may not be rectangular");
            String combinedList_str = CsvJoin.formatCSV(combinedList);
            System.out.println(combinedList_str);
        }
        catch (Exception e){
            //table DNE
            System.out.println("Issue with reading table");
        }
    }

    /**
     * Convert a nested sequence representing a table to CSV format.
     */
    private static String formatCSV(Seq<Seq<String>> list){
        //Given a nested sequence
        //Take the toString of each row
        int numRows = list.size();
        String formatCSV = "";
        for (int i = 0; i < numRows; i ++){
            String row = list.get(i).toString();
            //Remove “[“ and “]”
            //Add new line
            int start= row.indexOf("[");
            int end = row.indexOf("]");
            row.substring(start+1, end);
            formatCSV += row + "\n";
        }

        return formatCSV;

    }
}