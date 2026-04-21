package cs2110;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class CourseTest {

    @Test
    void testConstructor(){
        Course course = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 8, 30, 60);
        assertEquals("Biology 200", course.title());
        assertEquals(3,course.credits());
        assertEquals("Professor Parker", course.instructor());
        assertEquals("Physical Sciences Building", course.location());

    }
    @Test
    void testFormatStartTime(){
        Course course = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 0, 30, 60);
        assertEquals("0:30 AM", course.formatStartTime());
    }

    @Test
    void testOverlaps(){
        Course course = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 10, 30, 60);
        Course course2 = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 11, 29, 60);
        assertEquals(true, course.overlaps(course2));
    }
    @Test
    void testEnrollStudent(){
        Course course = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 10, 30, 60);
        Student student = new Student("student", "1");
        if (course.hasStudent(student)){
            assertEquals(false, course.enrollStudent(student));
        }
        else{
            assertEquals(true, course.enrollStudent(student));

        }
    }

    @Test
    void testDropStudent(){
        Course course = new Course("Biology 200",3,"Parker", "Physical Sciences Building", 10, 30, 60);
        Student student = new Student("student", "1");
        if (course.hasStudent(student)){
            assertEquals(true, course.dropStudent(student));
        }
        else {
            assertEquals(false, course.dropStudent(student));
        }
    }


}


