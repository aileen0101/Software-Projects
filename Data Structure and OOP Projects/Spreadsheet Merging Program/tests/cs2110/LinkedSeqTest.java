package cs2110;

import java.util.Iterator;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LinkedSeqTest {

    // Helper functions for creating lists used by multiple tests.  By constructing strings with
    // `new`, more likely to catch inadvertent use of `==` instead of `.equals()`.

    /**
     * Creates [].
     */
    static Seq<String> makeList0() {
        return new LinkedSeq<>();
    }

    /**
     * Creates ["A"].  Only uses prepend.
     */
    static Seq<String> makeList1() {
        Seq<String> ans = new LinkedSeq<>();
        ans.prepend(new String("A"));
        return ans;
    }

    /**
     * Creates ["A", "B"].  Only uses prepend.
     */
    static Seq<String> makeList2() {
        Seq<String> ans = new LinkedSeq<>();
        ans.prepend(new String("B"));
        ans.prepend(new String("A"));
        return ans;
    }

    /**
     * Creates ["A", "B", "C"].  Only uses prepend.
     */
    static Seq<String> makeList3() {
        Seq<String> ans = new LinkedSeq<>();
        ans.prepend(new String("C"));
        ans.prepend(new String("B"));
        ans.prepend(new String("A"));
        return ans;
    }

    /**
     * Creates a list containing the same elements (in the same order) as array `elements`.  Only
     * uses prepend.
     */
    static <T> Seq<T> makeList(T[] elements) {
        Seq<T> ans = new LinkedSeq<>();
        for (int i = elements.length; i > 0; i--) {
            ans.prepend(elements[i - 1]);
        }
        return ans;
    }

    @Test
    void testConstructorSize() {
        Seq<String> list = new LinkedSeq<>();
        assertEquals(0, list.size());
    }

    @Test
    void testPrependSize() {
        // List creation helper functions use prepend.
        Seq<String> list;

        list = makeList1();
        assertEquals(1, list.size());

        list = makeList2();
        assertEquals(2, list.size());

        list = makeList3();
        assertEquals(3, list.size());
    }

    @Test
    void testToString() {
        Seq<String> list;

        list = makeList0();
        assertEquals("[]", list.toString());

        list = makeList1();
        assertEquals("[A]", list.toString());

        list = makeList2();
        assertEquals("[A, B]", list.toString());

        list = makeList3();
        assertEquals("[A, B, C]", list.toString());
    }

    // TODO: Add new test cases here as you implement each method in `LinkedSeq`.  You may combine
    // multiple tests for the _same_ method in the same @Test procedure, but be sure that each test
    // case is visibly distinct (comments are good for this).  You are welcome to compare against an
    // expected `toString()` output in order to check multiple aspects of the state at once (in
    // general, later tests may make use of methods that have previously been tested).

    @Test
    void testContains(){
        Seq<String> list;

        list = makeList1();
        assertEquals(true, list.contains("A"));
        assertEquals(false, list.contains("B"));

        list = makeList2();
        assertEquals(true, list.contains("B"));
        assertEquals(false, list.contains("C"));

        list = makeList3();
        assertEquals(true, list.contains("C"));
        assertEquals(false, list.contains("D"));
    }

    @Test
    void testGet(){
        Seq<String> list;
        list = makeList1();
        assertEquals("A", list.get(0));
        list = makeList2();
        assertEquals("A", list.get(0));
        assertEquals("B", list.get(1));
        list = makeList3();
        assertEquals("A", list.get(0));
        assertEquals("B", list.get(1));
        assertEquals("C", list.get(2));

    }

    @Test
    void testAppend(){
        Seq<String> list;
        list = makeList0();
        list.append("S");
        assertEquals("[S]",list.toString());

        list = makeList1();
        list.append("D");
        assertEquals("[A, D]", list.toString());

        list = makeList2();
        list.append("J");
        assertEquals("[A, B, J]", list.toString());

        list = makeList3();
        list.append("P");
        assertEquals("[A, B, C, P]", list.toString());

    }

    @Test
    void testInsertBefore(){
        Seq<String> list;
        list = makeList3();
        list.insertBefore("A", "B");
        assertEquals("[A, A, B, C]", list.toString());

        list.insertBefore("C", "A");
        assertEquals("[C, A, A, B, C]", list.toString());

        list = makeList3();
        list.insertBefore("M", "C");
        assertEquals("[A, B, M, C]", list.toString());

        list = makeList2();
        list.insertBefore("A", "A");
        assertEquals("[A, A, B]", list.toString());
    }

    @Test
    void testRemove(){
        Seq<String> list;
        //empty list
        list=makeList0();
        assertEquals(false, list.remove("B"));
        assertEquals("[]", list.toString());

        list=makeList1();
        //Elem present in the list once
        assertEquals(true, list.remove("A"));
        assertEquals("[]", list.toString());

        //Elem not present in the list
        list=makeList1();
        assertEquals(false, list.remove("B"));
        assertEquals("[A]", list.toString());

        //Testing list of 2 elements
        list=makeList2();
        assertEquals(true, list.remove("A"));
        assertEquals("[B]", list.toString());

        list=makeList2();
        assertEquals(true, list.remove("B"));
        assertEquals("[A]", list.toString());

        //ELem in the list twice
        list=makeList2();
        list.prepend("B");
        assertEquals(true, list.remove("B"));
        assertEquals("[A, B]", list.toString());

        //Elem not in the list
        list=makeList3();
        assertEquals(false, list.remove("K"));
        assertEquals("[A, B, C]", list.toString());
        //Elem in the list
        list=makeList3();
        assertEquals(true, list.remove("C"));
        assertEquals("[A, B]", list.toString());
    }

    @Test
    void testEquals(){
        Seq<String> list;
        list=makeList0();
        Seq<String> list00;
        list00=makeList0();
        Seq<String> list2;
        list2=makeList1();
        Seq<String> list22;
        list22=makeList2();
        Seq<String> list23;
        list23=makeList2();
        Seq<String> list3;
        list3=makeList3();
        list3.prepend("C");
        Seq<String> list4;
        list4=makeList3();
        list4.prepend("H");
        Seq<String> list5;
        list5=makeList3();
        list5.append("H");

        //Same lists
        assertEquals(true, list22.equals(list23));
        //Comparing two empty lists
        assertEquals(true,list00.equals(list));
        //Different lists: empty list with non-empty list
        assertEquals(false, list.equals(list4));
        //Different lists: non empty lists of different sizes
        assertEquals(false,list2.equals(list4));
        //Different lists: same sized lists with different elements
        assertEquals(false, list3.equals(list4));
        //Different lists: same sized lists of same elements in different order
        assertEquals(false,list4.equals(list5));

    }
    /*
     * There is no need to read the remainder of this file for the purpose of completing the
     * assignment.  We have not yet covered `hashCode()` or `assertThrows()` in class.
     */

    @Test
    void testHashCode() {
        assertEquals(makeList0().hashCode(), makeList0().hashCode());

        assertEquals(makeList1().hashCode(), makeList1().hashCode());

        assertEquals(makeList2().hashCode(), makeList2().hashCode());

        assertEquals(makeList3().hashCode(), makeList3().hashCode());
    }

    @Test
    void testIterator() {
        Seq<String> list;
        Iterator<String> it;

        list = makeList0();
        it = list.iterator();
        assertFalse(it.hasNext());
        Iterator<String> itAlias = it;
        assertThrows(NoSuchElementException.class, () -> itAlias.next());

        list = makeList1();
        it = list.iterator();
        assertTrue(it.hasNext());
        assertEquals("A", it.next());
        assertFalse(it.hasNext());

        list = makeList2();
        it = list.iterator();
        assertTrue(it.hasNext());
        assertEquals("A", it.next());
        assertTrue(it.hasNext());
        assertEquals("B", it.next());
        assertFalse(it.hasNext());
    }
}
