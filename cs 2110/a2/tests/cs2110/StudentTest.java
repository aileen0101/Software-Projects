package cs2110;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class StudentTest {
    @Test
    void testConstructorAndObservers() {
        // Typical case
        {
            Student s = new Student("first", "last");
            assertEquals("first", s.firstName());
            assertEquals("last", s.lastName());
            assertEquals(0, s.credits());
        }

        // Short names
        {
            Student s = new Student("f", "l");
            assertEquals("f", s.firstName());
            assertEquals("l", s.lastName());
        }
    }

    @Test
    void testFullName() {
        Student s = new Student("Aileen", "Huang");
        assertEquals("Aileen Huang", s.fullName());
    }

    @Test
    void testAdjustCredits() {
        Student s = new Student("first", "last");
        s.adjustCredits(3);
        assertEquals(3, s.credits());

        // A second adjustment should be cumulative
        s.adjustCredits(4);
        assertEquals(7, s.credits());

        // Negative adjustments
        s.adjustCredits(-3);
        assertEquals(4, s.credits());

        // Back to zero
        s.adjustCredits(-4);
        assertEquals(0, s.credits());
    }
}
