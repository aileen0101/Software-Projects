package cs2110;

/*
 * Assignment metadata
 * Name and NetID: Aileen Huang (aeh245)
 * Hours spent on assignment: 12 hours
 */

/**
 * Collection of misc. static functions for showcasing the capabilities of Java in a procedural
 * context.
 */
public class A1 {

    /**
     * Return the area of a regular polygon with `nSides` sides of length `sideLength`. Units of
     * result are the square of the units of `sideLength`. Requires `nSides` is at least 3,
     * `sideLength` is non-negative.
     */
    public static double polygonArea(int nSides, double sideLength) {
        double s_squared = Math.pow(sideLength, 2.0);
        double tangent = Math.tan(Math.PI / nSides);
        double first_part = 0.25 * s_squared;
        double area = first_part * (nSides / tangent);
        return area;
    }

    /**
     * Return the next term in the Collatz sequence after the argument.  If the argument is even,
     * the next term is it divided by 2.  If the argument is odd, the next term is 3 times it plus
     * 1.  Requires magnitude of odd `x` is less than `Integer.MAX_VALUE/3` (otherwise overflow is
     * possible).
     */
    // TODO: Declare and implement a method named `nextCollatz()` that takes one int argument and
    // returns an int.

    /**
     * Return the sum of the Collatz sequence starting at `seed` and ending at 1 (inclusive).
     * Requires `seed` is positive, sum does not overflow.
     */
    public static int collatzSum(int seed) {
        // Implementation constraint: Use a while-loop.  Call `nextCollatz()` to
        // advance the sequence.

        int sum = seed;
        int curr = seed;
        while (curr > 1) {
            if (curr != 1) {
                int next = nextCollatz(curr);
                sum = sum + next;
                curr = next;
            }
        }
        return sum;
    }

    public static int nextCollatz(int curr) {
        int nxt = curr;
        if (nxt % 2 == 0) {
            nxt = nxt / 2;
        } else {
            nxt = nxt * 3 + 1;

        }
        return nxt;


    }


    /**
     * Return the median value among `{a, b, c}`.  The median has the property that at least half of
     * the elements are less than or equal to it and at least half of the elements are greater than
     * or equal to it.
     */
    public static int med3(int a, int b, int c) {
        // Implementation constraint: Do not call any other methods.

        if (a >= b && a <= c) {
            return a;
        }

        if (a <= b && a >= c) {
            return a;
        }

        if (b >= a && b <= c) {
            return b;
        }

        if (b >= c && b <= a) {
            return b;
        }

        if (c >= a && c <= b) {
            return c;
        } else {
            return c;
        }

    }

    /**
     * Return whether the closed intervals `[lo1, hi1]` and `[lo2, hi2]` overlap.  Two intervals
     * overlap if there exists a number contained in both of them.  Notation: the interval `[lo,
     * hi]` contains all numbers greater than or equal to `lo` and less than or equal to `hi`.
     * Requires `lo1` is less than or equal to `hi1` and `lo2` is less than or equal to `hi2`.
     */
    public static boolean intervalsOverlap(int lo1, int hi1, int lo2, int hi2) {
        // Implementation constraint: Use a single return statement to return
        // the value of a Boolean expression; do not use an if-statement.

        return (lo1 >= lo2 && hi1 <= hi2) || (lo1 >= lo2 && lo1 <= hi2) || (hi1 >= lo2 && hi1 <= hi2) ||
                (lo1 <= lo2 && hi1 >= hi2) || (lo2 >= lo1 && lo2 <= hi1) || (hi2 >= lo1 && hi2 <= hi1);

    }

    /**
     * Return the approximation of pi computed from the sum of the first `nTerms` terms of the
     * Madhava-Leibniz series.  This formula states that pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
     * Requires `nTerms` is non-negative.
     */
    public static double estimatePi(int nTerms) {
        // Implementation constraint: Use a for-loop.  Do not call any other
        // methods (including `Math.pow()`).

        double estPiOver4 = 0.0;

        if (nTerms == 0) {
            return 0.0;
        }
        int index;
        for (index = 0; index < nTerms; index++) {
            int denom = (2 * index) + 1;
            double fraction = 1.0 / (denom);

            if (index % 2 == 1) {
                fraction = -1 * fraction;
            }

            estPiOver4 = estPiOver4 + fraction;
        }

        return estPiOver4 * 4;
    }

    /**
     * Returns whether the sequence of characters in `s` is equal (case-sensitive) to that sequence
     * in reverse order.
     */
    public static boolean isPalindrome(String s) {
        // Implementation constraint: Use the `charAt()` and `length()` methods
        // of the `String` class.

        if (s.length() == 0) {
            return true;
        }
        if (s.length() == 1) {
            return true;
        }

        if (s.length() == 2) {
            if (s.charAt(0) != s.charAt(1)) {
                return false;
            } else {
                return true;
            }
        }

        if (s.length() >= 3) {
            for (int i = 0; i < s.length() - 2; i++) {
                if (s.charAt(i) != s.charAt(s.length() - 1 - i)) {
                    return false;
                }
            }
        }
        return true;

    }

    /**
     * Return an order confirmation message in English containing the order ID and the number of
     * items it contains.  Message shall handle item plurality properly (e.g. "1 item" vs. "3
     * items") and shall surround the order ID in single quotes. Examples:
     * <pre>
     * formatConfirmation("123ABC", 1) should return
     *   "Order '123ABC' contains 1 item."
     * formatConfirmation("XYZ-999", 3)" should return
     *   "Order 'XYZ-999' contains 3 items."
     * </pre>
     * Requires `orderId` only contains digits, hyphens, or letters 'A' - 'Z'; `itemCount` is
     * non-negative.
     */
    public static String formatConfirmation(String orderId, int itemCount) {
        // Implementation constraint: Use Java's ternary operator (`?:`) to give "item" the
        // appropriate plurality.
        String item = itemCount != 1 ? "items" : "item";
        String fullstring = "Order" + " " + "'" + orderId + "'" + " contains " + itemCount + " " + item + ".";
        return fullstring;

    }

    // TODO: Declare, document, and implement a `main()` method calling the above methods and
    // printing a result.

    public static void main(String[] args) {
        int median = med3(3, 5, 4);
        int collatzsum = collatzSum(median);
        double estPi = estimatePi(collatzsum);
        double polygonArea = polygonArea(collatzsum, estPi);
        System.out.println("The area of a polygon with " + collatzsum + " sides" + " and length " + estPi + " units is " + polygonArea + ".");


    }

}
