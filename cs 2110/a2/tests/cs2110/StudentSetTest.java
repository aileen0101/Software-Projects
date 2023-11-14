package cs2110;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class StudentSetTest {
    @Test
    void testConstructorAndSize() {
        // Constructor should yield an empty set
        StudentSet students = new StudentSet();
        assertEquals(0, students.size());
    }


    @Test
    void testAddStudent(){
        //Adding one student, not exceeding capacity
        StudentSet student_array = new StudentSet();
        Student s = new Student("firstname", "lastname");
        student_array.add(s);
        System.out.println("here");
        assertEquals(1, student_array.size());

        //Adding one student, exceeding capacity
        //add one each time, do assertion for each
        StudentSet s_array = new StudentSet();
        int set_size = s_array.length();
        for (int i = 0; i < set_size; i++){
                Student student = new Student("firstname" + Integer.toString(i), "lastname" +Integer.toString(i));
                s_array.add(student);
                System.out.println(s_array.length());
        }

        assertEquals(set_size, s_array.size());

        // exceeding capacity
        Student s_exceed = new Student("firstname", "lastname");
        int og_length = s_array.length();
        s_array.add(s_exceed);
        System.out.println("here3");
        assertEquals(og_length*2, s_array.length());
    }

    @Test
    void testAddExceed(){
        StudentSet student_array = new StudentSet();
        Student student =new Student("firstname", "lastname");
        int org_length = student_array.length();
        student_array.add_exceed(student);
        assertEquals(org_length*2, student_array.length());

    }

    @Test
    void testContains(){
        StudentSet student_array = new StudentSet();
        Student s =new Student("firstname", "lastname");
        student_array.add(s);
        assertEquals(true, student_array.contains(s));
    }
    @Test
    void testRemove(){
        StudentSet s_array = new StudentSet();
        Student s =new Student("firstname", "lastname");
        s_array.add(s);
        assertEquals(true, s_array.remove(s));
    }
}
