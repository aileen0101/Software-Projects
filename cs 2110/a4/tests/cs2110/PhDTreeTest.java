package cs2110;

import static org.junit.jupiter.api.Assertions.*;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.List;
import java.util.LinkedList;

import org.junit.jupiter.api.Test;

public class PhDTreeTest {

    // These pre-defined Professor and PhDTree objects may be used to simplify the setup for your
    // test cases.  You are encouraged to add your own helper methods (even `tree3()` would be
    // considered "trivial", since no node has more than 1 child).
    private static final Professor prof1 = new Professor("Amy Huang", 2023);
    private static final Professor prof2 = new Professor("Maya Leong", 2023);
    private static final Professor prof3 = new Professor("Matthew Hui", 2025);
    private static final Professor prof4 = new Professor("Arianna Curillo", 2022);
    private static final Professor prof5 = new Professor("Michelle Gao", 2022);
    private static final Professor prof6 = new Professor("Isa Siu", 2024);

    // These helper methods create a copy of each Professor object, which would normally be seen as
    // wasteful.  They do so to help expose bugs involving the use of `==` instead of `.equals()`.
    private static PhDTree tree1() {
        return new PhDTree(new Professor(prof1));
    }

    private static PhDTree tree2() {
        return new PhDTree(new Professor(prof4));
    }

    private static PhDTree tree3() throws NotFound {
        PhDTree t = new PhDTree(new Professor(prof1));
        t.insert(prof1.name(), new Professor(prof2));
        t.insert(prof2.name(), new Professor(prof3));
        return t;
    }

    private static PhDTree tree4() throws NotFound {
        PhDTree tree = new PhDTree(new Professor(prof2));
        tree.insert(prof2.name(), new Professor(prof1));
        tree.insert(prof2.name(), new Professor(prof3));
        tree.insert(prof3.name(), new Professor(prof4));
        tree.insert(prof3.name(), new Professor(prof5));
        tree.insert(prof5.name(), new Professor(prof6));
        return tree;
    }

    private static PhDTree tree5() throws NotFound {
        PhDTree tree = new PhDTree(new Professor(prof6));
        tree.insert(prof6.name(), new Professor(prof1));
        tree.insert(prof6.name(), new Professor(prof3));
        tree.insert(prof6.name(), new Professor(prof4));
        tree.insert(prof3.name(), new Professor(prof5));
        return tree;
    }

    private static PhDTree tree6() throws NotFound {
        PhDTree tree = new PhDTree(new Professor(prof4));
        tree.insert(prof4.name(), new Professor(prof1));
        tree.insert(prof1.name(), new Professor(prof2));
        tree.insert(prof1.name(), new Professor(prof6));
        tree.insert(prof1.name(), new Professor(prof5));
        tree.insert(prof5.name(), new Professor(prof3));
        return tree;
    }

    private static PhDTree oneAdvisee() throws NotFound {
        PhDTree tree = new PhDTree(new Professor(prof6));
        tree.insert(prof6.name(), new Professor(prof2));
        tree.insert(prof2.name(), new Professor(prof3));
        return tree;
    }

    private static PhDTree rootParent() throws NotFound {

        PhDTree tree = new PhDTree(new Professor(prof4));
        tree.insert(prof4.name(), new Professor(prof5));
        tree.insert(prof4.name(), new Professor(prof1));
        tree.insert(prof4.name(), new Professor(prof2));
        tree.insert(prof4.name(), new Professor(prof6));
        //tree.insert(prof4.name(), new Professor(prof5));
        return tree;
    }

    @Test
    public void testConstructorProfToString() {

        PhDTree t1 = tree1();
        assertEquals("Amy Huang", t1.toString());
        assertEquals(prof1, t1.prof());

        PhDTree t2 = tree2();
        assertEquals("Arianna Curillo", t2.toString());
        assertEquals(prof4, t2.prof());

    }

    @Test
    public void testNumAdvisees() throws NotFound {
        PhDTree t = tree1();
        assertEquals(0, t.numAdvisees());
        //one direct child
        PhDTree t2 = tree3();
        assertEquals(1, t2.numAdvisees());
        // TODO: Add three additional tests of `numAdvisees()` using your own tree(s)
        //one direct child
        PhDTree t3 = tree6();
        assertEquals(1, t3.numAdvisees());
        //two direct children
        PhDTree t4 = tree4();
        assertEquals(2, t4.numAdvisees());
        //three direct children
        PhDTree t5 = tree5();
        assertEquals(3, t5.numAdvisees());

    }

    @Test
    public void testSize() throws NotFound {
        PhDTree t = tree3();
        assertEquals(3, t.size());

        // TODO: Add three additional tests of `size()` using your own tree(s)
        //tree with only root node
        PhDTree t2 = new PhDTree(prof2);
        assertEquals(1, t2.size());

        PhDTree t3 = tree4();
        assertEquals(6, t3.size());

        PhDTree t4 = tree5();
        assertEquals(5, t4.size());

        //Each node has only one child
        PhDTree t5 = oneAdvisee();
        assertEquals(3, t5.size());

        //Children all have root node as direct parent
        PhDTree t6 = rootParent();
        assertEquals(5, t6.size());
    }

    @Test
    public void testMaxDepth() throws NotFound {
        PhDTree t = tree3();
        assertEquals(3, t.maxDepth());

        // TODO: Add three additional tests of `maxDepth()` using your own tree(s)
        //depth of one
        PhDTree t1 = new PhDTree(prof4);
        assertEquals(1, t1.maxDepth());

        //Advisees have subtrees of different depths
        PhDTree t2 = tree4();
        assertEquals(4, t2.maxDepth());

        //advisees are all direct children of root professor
        PhDTree t3 = rootParent();
        assertEquals(2, t3.maxDepth());

        //Each parent has one child only
        PhDTree t4 = oneAdvisee();
        assertEquals(3, t4.maxDepth());
    }

    @Test
    public void testFindTree() throws NotFound {
        PhDTree tree1 = tree1();
        tree1.insert(prof1.name(), prof2);
        tree1.insert(prof2.name(), prof3);
        PhDTree tree4 = new PhDTree(prof2);
        tree4.insert(prof2.name(), prof3);
        assertEquals(tree4.prof(), tree1.findTree(prof2.name()).prof());
        assertEquals("Maya Leong[Matthew Hui]", tree1.findTree(prof2.name()).toString());

        assertThrows(NotFound.class, () -> tree2().findTree(prof5.name()));
        assertThrows(NotFound.class, () -> tree1.findTree(prof4.name()));
        assertEquals(1, tree1.findTree(prof3.name()).size());

        // TODO: Add three additional tests of `findTree()` using your own tree(s)

        //tree with only root professor
        PhDTree t1 = new PhDTree(prof5);
        assertEquals("Michelle Gao", t1.findTree(prof5.name()).toString());
        assertThrows(NotFound.class, () -> t1.findTree(prof2.name()));

        //subtrees with different depths
        PhDTree t2 = tree4();
        PhDTree t2subTree = new PhDTree(prof3);
        t2subTree.insert(prof3.name(), new Professor(prof4));
        t2subTree.insert(prof3.name(), new Professor(prof5));
        t2subTree.insert(prof5.name(), new Professor(prof6));
        assertEquals(t2subTree.prof(), t2.findTree(prof3.name()).prof());
        assertEquals("Matthew Hui[Arianna Curillo, Michelle Gao[Isa Siu]]", t2.findTree(prof3.name()).toString());
        assertEquals(4, t2.findTree(prof3.name()).size());

        assertThrows(NotFound.class, () -> t2.findTree("Aileen Huang"));

        //Root professor = direct professor of all children
        PhDTree t3 = rootParent();
        assertEquals(prof5, t3.findTree(prof5.name()).prof());
        assertEquals(prof1.name(), t3.findTree(prof1.name()).toString());
        assertEquals("Arianna Curillo[Michelle Gao, Amy Huang, Maya Leong, Isa Siu]", t3.findTree(prof4.name()).toString());
        assertEquals(5, t3.findTree(prof4.name()).size());
        assertThrows(NotFound.class, () -> t3.findTree(prof3.name()));

    }

    @Test
    public void containsTest() throws NotFound {
        PhDTree t = tree3();
        assertTrue(t.contains("Amy Huang"));
        assertFalse(t.contains(prof6.name()));
    }

    @Test
    public void testInsert() throws NotFound {
        PhDTree t = tree1();
        t.insert(prof1.name(), prof2);
        t.insert(prof2.name(), prof3);
        assertEquals("Amy Huang[Maya Leong[Matthew Hui]]", t.toString());

        // TODO: Add three additional tests of `insert()` using your own tree(s)

        //each professor has one advisee only: add advisees
        PhDTree t1 = oneAdvisee();
        //add one to the end
        t1.insert(prof3.name(), prof4);
        //add one between root and end
        t1.insert(prof2.name(), prof5);
        assertEquals("Isa Siu[Maya Leong[Michelle Gao, Matthew Hui[Arianna Curillo]]]", t1.toString());

        //root is direct professor of all advisees: add advisees
        PhDTree t2 = rootParent();
        t2.insert(prof4.name(), prof3);
        assertEquals("Arianna Curillo[Michelle Gao, Amy Huang, Maya Leong, Isa Siu, Matthew Hui]", t2.toString());
        //subtree of different depths: add advisees
        PhDTree t4 = tree5();
        t4.insert(prof4.name(), prof2);
        assertEquals("Isa Siu[Arianna Curillo[Maya Leong], Amy Huang, Matthew Hui[Michelle Gao]]", t4.toString());
    }

    @Test
    public void testFindAdvisor() throws NotFound {
        PhDTree t = tree3();
        assertEquals(prof2, t.findAdvisor(prof3.name()));
        assertThrows(NotFound.class, () -> t.findAdvisor(prof1.name()));

        // TODO: Add three additional tests of `findAdvisor()` using your own tree(s)
        //  tree with only root node
        PhDTree tree1 = new PhDTree(prof3);
        //assertEquals(prof3, tree1.findAdvisor(prof3.name()));
        assertThrows(NotFound.class, () -> tree1.findAdvisor(prof3.name()));
        //this professor isn't contained in the tree
        assertThrows(NotFound.class, () -> tree1.findAdvisor(prof2.name()));

        // general tree
        PhDTree tree2 = tree4();
        assertEquals(prof3, tree2.findAdvisor(prof4.name()));
        //root professor is immediate advisor
        assertEquals(prof2, tree2.findAdvisor(prof3.name()));

        assertThrows(NotFound.class, () -> tree2.findAdvisor(prof2.name()));
        assertThrows(NotFound.class, () -> tree2.findAdvisor("Aileen Huang"));

        //each advisee is a direct child node of root professor
        PhDTree tree3 = rootParent();
        assertEquals(prof4, tree3.findAdvisor(prof5.name()));
        assertThrows(NotFound.class, () -> tree3.findAdvisor(prof4.name()));
        assertThrows(NotFound.class, () -> tree3.findAdvisor("Doctor Huang"));

        //each professor has one advisee only
        PhDTree tree4 = oneAdvisee();
        assertEquals(prof2, tree4.findAdvisor(prof3.name()));
        assertThrows(NotFound.class, () -> tree4.findAdvisor(prof6.name()));
        assertThrows(NotFound.class, () -> tree4.findAdvisor("Nate Jones"));
    }

    @Test
    public void testFindAcademicLineage() throws NotFound {
        PhDTree t = tree3();
        List<Professor> lineage1 = new LinkedList<>();
        lineage1.add(prof1);
        lineage1.add(prof2);
        lineage1.add(prof3);
        assertEquals(lineage1, t.findAcademicLineage(prof3.name()));

        // TODO: Add three additional tests of `findAcademicLineage()` using your own tree(s)

        //lineage to root professor
        PhDTree t1 = tree4();
        List<Professor> lineage2 = new LinkedList<>();
        lineage2.add(prof2);
        assertEquals(lineage2, t1.findAcademicLineage(prof2.name()));
        lineage2.add(prof3);
        assertEquals(lineage2, t1.findAcademicLineage(prof3.name()));
        //lineage to one of the descendants between root and one of the last descendants
        lineage2.add(prof5);
        lineage2.add(prof6);
        //lineage to one of the last descendants
        assertEquals(lineage2, t1.findAcademicLineage(prof6.name()));

        //repeat above for the following two trees

        PhDTree t2 = rootParent();
        List<Professor> lineage3 = new LinkedList<>();
        lineage3.add(prof4);
        assertEquals(lineage3, t2.findAcademicLineage(prof4.name()));
        lineage3.add(prof1);
        assertEquals(lineage3, t2.findAcademicLineage(prof1.name()));

        PhDTree t3 = oneAdvisee();
        List<Professor> lineage4 = new LinkedList<>();
        lineage4.add(prof6);
        assertEquals(lineage4, t3.findAcademicLineage(prof6.name()));
        lineage4.add(prof2);
        assertEquals(lineage4, t3.findAcademicLineage(prof2.name()));
        lineage4.add(prof3);
        assertEquals(lineage4, t3.findAcademicLineage(prof3.name()));
    }

    @Test
    public void testCommonAncestor() throws NotFound {
        PhDTree t = tree3();
        assertEquals(prof2, t.commonAncestor(prof2.name(), prof3.name()));
        assertEquals(prof1, t.commonAncestor(prof1.name(), prof3.name()));
        assertThrows(NotFound.class, () -> t.commonAncestor(prof5.name(), prof3.name()));

        // TODO: Add three additional tests of `commonAncestor()` using your own tree(s)
        //general tree
        PhDTree t2 = tree4();
        assertEquals(prof2, t2.commonAncestor(prof2.name(), prof1.name()));
        assertEquals(prof2, t2.commonAncestor(prof1.name(), prof5.name()));
        assertEquals(prof3, t2.commonAncestor(prof4.name(), prof5.name()));
        assertEquals(prof3, t2.commonAncestor(prof4.name(), prof6.name()));
        assertEquals(prof3, t2.commonAncestor(prof3.name(), prof6.name()));

        assertThrows(NotFound.class, () -> t2.commonAncestor("Aileen Huang", prof3.name()));

        //root professor = parent of all advisees
        PhDTree t3 = rootParent();
        assertEquals(prof4, t3.commonAncestor(prof1.name(), prof4.name()));
        assertEquals(prof4, t3.commonAncestor(prof1.name(), prof6.name()));

        assertThrows(NotFound.class, () -> t3.commonAncestor(prof3.name(), prof4.name()));

        // professor has one advisee each
        PhDTree t4 = oneAdvisee();
        assertEquals(prof2, t4.commonAncestor(prof2.name(), prof3.name()));
        assertEquals(prof6, t4.commonAncestor(prof6.name(), prof2.name()));

        assertThrows(NotFound.class, () -> t4.commonAncestor(prof3.name(), prof4.name()));
        assertThrows(NotFound.class, () -> t4.commonAncestor(prof6.name(), prof5.name()));

    }

    @Test
    public void testPrintProfessors() throws NotFound {
        {  // Restrict scope to one test case
            PhDTree t = tree3();

            // A StringWriter lets us capture output that might normally be written to a file, or
            // printed on the console, in a String instead.
            StringWriter out = new StringWriter();

            // Need to wrap our Writer in a PrintWriter to satisfy `printProfessors()` (but we save
            // the original StringWriter so we can access its string later).  Flush the PrintWriter
            // when we are done with it.
            PrintWriter pw = new PrintWriter(out);
            t.printProfessors(pw);
            pw.flush();

            // Split string into lines for easy comparison ("\\R" is a "regular expression" that
            // matches both Windows and Unix line separators; it only works in methods like
            // `split()`).
            String[] lines = out.toString().split("\\R");
            String[] expected = {
                    "Amy Huang - 2023",
                    //"",
                    "Maya Leong - 2023",
                    //"",
                    "Matthew Hui - 2025"
            };
//            for (int i = 0; i < lines.length; i++) {
//                // ",\n"
//                System.out.println(lines[i]);
//            }
//            System.out.println(lines.length);
//            System.out.println("=======================");
//            for (int i = 0; i < expected.length; i++) {
//                System.out.println(expected[i]);
//            }
//            System.out.println(expected.length);
            assertArrayEquals(expected, lines);


            //testing general tree

        }

        // TODO: Add three additional tests of `commonAncestor()` using your own tree(s)
        // Feel free to define a helper method to avoid duplicated testing code.


    }

    //General tree
    @Test
    public void testPrintProfessors1() throws NotFound {
        {  // Restrict scope to one test case
            PhDTree t = tree4();

            // A StringWriter lets us capture output that might normally be written to a file, or
            // printed on the console, in a String instead.
            StringWriter out = new StringWriter();

            // Need to wrap our Writer in a PrintWriter to satisfy `printProfessors()` (but we save
            // the original StringWriter so we can access its string later).  Flush the PrintWriter
            // when we are done with it.
            PrintWriter pw = new PrintWriter(out);
            t.printProfessors(pw);
            pw.flush();

            // Split string into lines for easy comparison ("\\R" is a "regular expression" that
            // matches both Windows and Unix line separators; it only works in methods like
            // `split()`).
            String[] lines = out.toString().split("\\R");
            String[] expected = {
                    "Maya Leong - 2023",
                    //"",
                    "Amy Huang - 2023",
                    //"",
                    "Matthew Hui - 2025",
                    "Arianna Curillo - 2022",
                    "Michelle Gao - 2022",
                    "Isa Siu - 2024"
            };
//            for (int i = 0; i < lines.length; i++) {
//                // ",\n"
//                System.out.println(lines[i]);
//            }
//            System.out.println(lines.length);
//            System.out.println("=======================");
//            for (int i = 0; i < expected.length; i++) {
//                System.out.println(expected[i]);
//            }
            //System.out.println(expected.length);
            assertArrayEquals(expected, lines);

        }

    }

    //Each advisee's direct professor is root professor
    @Test
    public void testPrintProfessors2() throws NotFound {
        {  // Restrict scope to one test case
            PhDTree t = rootParent();

            // A StringWriter lets us capture output that might normally be written to a file, or
            // printed on the console, in a String instead.
            StringWriter out = new StringWriter();

            // Need to wrap our Writer in a PrintWriter to satisfy `printProfessors()` (but we save
            // the original StringWriter so we can access its string later).  Flush the PrintWriter
            // when we are done with it.
            PrintWriter pw = new PrintWriter(out);
            t.printProfessors(pw);
            pw.flush();

            // Split string into lines for easy comparison ("\\R" is a "regular expression" that
            // matches both Windows and Unix line separators; it only works in methods like
            // `split()`).
            String[] lines = out.toString().split("\\R");
            String[] expected = {
                    "Arianna Curillo - 2022",
                    //"",
                    "Michelle Gao - 2022",
                    "Amy Huang - 2023",
                    //"",
                    "Maya Leong - 2023",
                    "Isa Siu - 2024"

            };
//            for (int i = 0; i < lines.length; i++) {
//                // ",\n"
//                System.out.println(lines[i]);
//            }
//            System.out.println(lines.length);
//            System.out.println("=======================");
//            for (int i = 0; i < expected.length; i++) {
//                System.out.println(expected[i]);
//            }
           // System.out.println(expected.length);
            assertArrayEquals(expected, lines);

        }

    }

    //Each professor has one advisee only
    @Test
    public void testPrintProfessors3() throws NotFound {
        {  // Restrict scope to one test case
            PhDTree t = oneAdvisee();

            // A StringWriter lets us capture output that might normally be written to a file, or
            // printed on the console, in a String instead.
            StringWriter out = new StringWriter();

            // Need to wrap our Writer in a PrintWriter to satisfy `printProfessors()` (but we save
            // the original StringWriter so we can access its string later).  Flush the PrintWriter
            // when we are done with it.
            PrintWriter pw = new PrintWriter(out);
            t.printProfessors(pw);
            pw.flush();

            // Split string into lines for easy comparison ("\\R" is a "regular expression" that
            // matches both Windows and Unix line separators; it only works in methods like
            // `split()`).
            String[] lines = out.toString().split("\\R");
            String[] expected = {
                    "Isa Siu - 2024",
                    //"",
                    "Maya Leong - 2023",
                    "Matthew Hui - 2025"

            };
//            for (int i = 0; i < lines.length; i++) {
//                // ",\n"
//                System.out.println(lines[i]);
//            }
//            System.out.println(lines.length);
//            System.out.println("=======================");
//            for (int i = 0; i < expected.length; i++) {
//                System.out.println(expected[i]);
//            }
            //System.out.println(expected.length);
            assertArrayEquals(expected, lines);

        }

    }
}
