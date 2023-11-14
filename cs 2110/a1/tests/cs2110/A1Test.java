package cs2110;

import static cs2110.A1.nextCollatz;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class A1Test {

    @Test
    void testPolygonArea() {
        /* Note: Comparing doubles in tests can be tricky; see comment below if you'd like to
         * understand the third argument in the tests' assertions. */

        // Triangle
        assertEquals(Math.sqrt(3) / 4, A1.polygonArea(3, 1.0),
                3 * Math.ulp(Math.sqrt(3) / 4));
        assertEquals(Math.sqrt(3), A1.polygonArea(3, 2.0),
                3 * Math.ulp(Math.sqrt(3)));

        // Square
        assertEquals(1, A1.polygonArea(4, 1.0),
                3 * Math.ulp(1));
        assertEquals(1.0 / 9.0, A1.polygonArea(4, 1.0 / 3.0),
                3 * Math.ulp(1.0 / 9.0));

        // Hexagon
        assertEquals(3 * Math.sqrt(3) / 2, A1.polygonArea(6, 1.0),
                3 * Math.ulp(3 * Math.sqrt(3) / 2));
    }

    /*
     * Regarding comparisons of floating-point numbers:
     * Floating-point arithmetic is subtle - two expressions that look algebraically equivalent may
     * actually produce different values on a computer because intermediate results get rounded.
     * For this reason, it is usually not appropriate to use `==` to ask whether the results of two
     * floating-point calculations are the same (there are exceptions, such as when computing with
     * integers or comparing to zero).  Instead, we ask whether the result is sufficiently close to
     * the expected value, and the third argument of `assertEquals()` is how we indicate the maximum
     * amount they are allowed to differ.  Choosing this tolerance is a deeper question than it may
     * seem, but for relatively simple equations, we don't expect more than the last few bits to be
     * different.  Since floating-point precision is _relative_, we use `Math.ulp()` to get a
     * corresponding absolute tolerance.
     * Students are **not** expected to come up with this logic on their own right now.
     */

    // TODO: Uncomment this test case after declaring `testNextCollatz()`.
    @Test
    void testNextCollatz() {
        // 4-2-1 cycle
        assertEquals(2, nextCollatz(4));
        assertEquals(1, nextCollatz(2));
        assertEquals(4, nextCollatz(1));

        // Negative numbers are allowed
        assertEquals(-1, nextCollatz(-2));
        assertEquals(-2, nextCollatz(-1));

        // Zero is allowed
        assertEquals(0, nextCollatz(0));
    }

    @Test
    void testMed3() {
        // Elements are distinct and sorted
        assertEquals(2, A1.med3(1, 2, 3));

        // Elements are distinct and not sorted
        assertEquals(2, A1.med3(2, 1, 3));
        assertEquals(2, A1.med3(1, 3, 2));
        assertEquals(2, A1.med3(3, 2, 1));

        // Elements may be negative
        assertEquals(0, A1.med3(-3, 0, 4));

        // Two duplicate elements
        assertEquals(1, A1.med3(1, 2, 1));
        assertEquals(2, A1.med3(2, 2, 1));

        // Three duplicate elements
        assertEquals(1, A1.med3(1, 1, 1));

        // Extreme values
        assertEquals(2, A1.med3(Integer.MIN_VALUE, 2, Integer.MAX_VALUE));
        assertEquals(Integer.MAX_VALUE,
                A1.med3(Integer.MIN_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE));
    }

    @Test
    void testIntervalsOverlap() {
        // Partial overlap
        assertTrue(A1.intervalsOverlap(1, 3, 2, 4));

        // One-point overlap
        assertTrue(A1.intervalsOverlap(1, 2, 2, 3));

        // One interval contained in the other
        assertTrue(A1.intervalsOverlap(0, 3, 1, 2));
        assertTrue(A1.intervalsOverlap(2, 3, 1, 3));

        // First is left of second
        assertFalse(A1.intervalsOverlap(-4, -2, 2, 4));

        // First is right of second
        assertFalse(A1.intervalsOverlap(-4, -2, -10, -5));

        // Single-point intervals
        assertTrue(A1.intervalsOverlap(1, 1, 1, 1));
        assertTrue(A1.intervalsOverlap(1, 1, 0, 2));
        assertFalse(A1.intervalsOverlap(1, 1, 2, 2));
    }

    @Test
    void testEstimatePi() {
        // Single term
        assertEquals(4, A1.estimatePi(1));

        // No terms
        assertEquals(0, A1.estimatePi(0));

        // Two terms
        assertEquals(8.0 / 3.0, A1.estimatePi(2),
                3 * Math.ulp(8.0 / 3.0));

        // All terms in API example
        assertEquals(1052.0 / 315.0, A1.estimatePi(5),
                3 * Math.ulp(1052.0 / 315.0));

        // 100 terms (matches many digits with isolated errors)
        assertEquals(3.1315929035585528, A1.estimatePi(100),
                3 * Math.ulp(3.1315929035585528));
    }

    @Test
    void testCollatzSum() {
        // 4-2-1 cycle
        assertEquals(7, A1.collatzSum(4));

        // Powers of 2
        assertEquals(63, A1.collatzSum(32));

        // A seed with more than twice as many steps as its value
        assertEquals(339, A1.collatzSum(9));
    }

    @Test
    void testIsPalindrome() {
        // Lower-case letters
        assertTrue(A1.isPalindrome("aba"));
        assertTrue(A1.isPalindrome("abba"));
        assertFalse(A1.isPalindrome("ab"));
        assertFalse(A1.isPalindrome("abcda"));

        // Empty string
        assertTrue(A1.isPalindrome(""));

        // One letter
        assertTrue(A1.isPalindrome("a"));

        // Palindrome except for first or last character (to catch 1-based indexing)
        assertFalse(A1.isPalindrome("cabba"));
        assertFalse(A1.isPalindrome("abbac"));

        // Digits
        assertTrue(A1.isPalindrome("121"));
        assertTrue(A1.isPalindrome("11"));
        assertFalse(A1.isPalindrome("1337"));

        // Non-ASCII characters (no supplemental)
        assertTrue(A1.isPalindrome("二零零二"));
        assertFalse(A1.isPalindrome("年月日"));

        // Longer input
        assertTrue(A1.isPalindrome("GohangasalamIImalasagnahoG"));

        // Case sensitive
        assertFalse(A1.isPalindrome("GoHangASalamiImALasagnaHog"));
    }

    @Test
    void testFormatConfirmation() {
        // Examples from spec
        assertEquals("Order '123ABC' contains 1 item.", A1.formatConfirmation("123ABC", 1));
        assertEquals("Order 'XYZ-999' contains 3 items.", A1.formatConfirmation("XYZ-999", 3));

        // Zero should be treated as plural
        assertEquals("Order 'AMZN1' contains 0 items.", A1.formatConfirmation("AMZN1", 0));
    }
}
