package cs2110;

/**
 * A mutable set of students.
 */
public class StudentSet {
    // Implementation: the StudentSet is implemented as a resizable array data structure.
    // Implementation constraint: do not use any classes from java.util.
    // Implementation constraint: assert preconditions for all method parameters and assert that the
    //     invariant is satisfied at least at the end of every method that mutates any fields.

    /**
     * Array containing the students in the set.  Elements `store[0..size-1]` contain the distinct
     * students in this set, none of which are null.  All elements in `store[size..]` are null.  The
     * length of `store` is the current capacity of the data structure and is at least 1.  Two
     * students `s1` and `s2` are distinct if `s1.equals(s2)` is false.
     */
    private Student[] store;

    /**
     * The number of distinct students in this set.  Non-negative and no greater than
     * `store.length`.
     */
    private int size;

    /**
     * Assert that this object satisfies its class invariants.
     */
    private void assertInv() {
        assert store != null && store.length > 0;
        assert size >= 0 && size <= store.length;

        for (int i = 0; i < size; ++i) {
            // Check that elements in use are non-null
            assert store[i] != null;

            // Check that students are all distinct
            for (int j = i + 1; j < size; ++j) {
                assert !store[i].equals(store[j]);
            }
        }

        // Check that unused capacity is all null
        for (int i = size; i < store.length; ++i) {
            assert store[i] == null;
        }
    }

    /**
     * Create an empty set of students.
     */
    public StudentSet() {

        this.store = new Student [10];
        this.size=0;
        assertInv();


    }

    /**
     * Return the number of students in this set.
     */
    public int size() {
        return this.size;
    }

    /**
     * Effect: Add student `s` to the set.  Requires `s` is not already in the set.
     */

    /**
     * Helper method for test cases:
     * Return the capacity of the student set
     *
     */
    public int length() {return this.store.length;}
    public void add(Student s) {

        assert !this.contains(s);

        if (this.size() < this.store.length) {
            this.store[this.size] = s;
            this.size++;

        } else {
            this.add_exceed(s);
        }

        assertInv();
    }
    public void add_exceed(Student s){
        // Have a temp array that has double the length
        Student[] store_exceed = new Student[this.store.length * 2];

        // copy all values from this.store to temp array
        for (int i = 0; i < this.store.length; i++) {
            store_exceed[i] = this.store[i];
        }

        // set temp array to the this.store
        this.store = store_exceed;
    }

    /**
     * Return whether this set contains student `s`.
     */
    public boolean contains(Student s) {
        //i f it contains student s, return true, otherwise return false! check through each element
        for (int i=0; i < this.size; i++){
            if (this.store[i].equals(s)){
                return true;
            }
        }
        return false;
    }

    /**
     * Effect: If student `s` is in this set, remove `s` from the set and return true. Otherwise
     * return false.
     */
    public boolean remove(Student s) {

        int i;
        for (i=0; i<this.store.length;i++){
            if (this.store[i].equals(s)){
                this.store[i] = null;
                return true;
            }
        }
        return false;
    }

    /**
     * Return the String representation of this StudentSet.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("{");
        for (int i = 0; i < size; ++i) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(store[i]);
        }
        sb.append("}");
        return sb.toString();
    }
}
