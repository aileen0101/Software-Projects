package cs2110;

/**
 * A student tracked by the CMSμ course management system.
 */
public class Student {

    private String firstname_student;
    //Invariant: private field representing first name of this Student (may not be empty or null).
    private String lastname_student;
    //Invariant: private field representing last name of this Student (may not be empty or null).
    private Integer num_credits;
    //Invariant: private field representing number of credits student is currently enrolled in (integer; may not be negative)



    /**
     * Assert that this object satisfies its class invariants.
     */
    private void assertInv() {

        assert (firstname_student != null) && (firstname_student.length() != 0);
        assert (lastname_student != null) && (lastname_student.length() != 0);
        assert (num_credits >=0);

    }

    /**
     * Create a new Student with first name `firstName` and last name `lastName` who is not enrolled
     * for any credits.  Requires firstName and lastName are not empty.
     */
    public Student(String firstName, String lastName) {

        assert (firstName.length() !=0);
        assert (lastName.length() !=0);
        this.firstname_student = firstName;
        this.lastname_student = lastName;
        this.num_credits = 0;
        assertInv();
    }

    /**
     * Return the first name of this Student.  Will not be empty.
     */
    public String firstName() {
        return this.firstname_student;
    }

    /**
     * Return the last name of this Student.  Will not be empty.
     */
    public String lastName() {
        return this.lastname_student;
    }

    /**
     * Return the full name of this student, formed by joining their first and last names separated
     * by a space.
     */
    public String fullName() {
        // Observe that, by invoking methods instead of referencing this fields, this method was
        // implemented without knowing how you will name your fields.
        return firstName() + " " + lastName();
    }

    /**
     * Return the number of credits this student is currently enrolled in.  Will not be negative.
     */
    public int credits() {
        return this.num_credits;
    }

    /**
     * Change the number of credits this student is enrolled in by `deltaCredits`. For example, if
     * this student were enrolled in 12 credits, then `this.adjustCredits(3)` would result in their
     * credits changing to 15, whereas `this.adjustCredits(-4)` would result in their credits
     * changing to 8.  Requires that the change would not cause the student's credits to become
     * negative.
     */
    void adjustCredits(int deltaCredits) {

        assert deltaCredits + credits() >=0;
        this.num_credits = credits()+deltaCredits;
        assertInv();

    }

    /**
     * Return the full name of this student as its string representation.
     */
    @Override
    public String toString() {
        return fullName();
    }
}
