package cs2110;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class CMSuTest {


    @Test
    void testHasConflict() {
        Student student = new Student("first", "last");
        CMSu cms = new CMSu();
        //add two courses that have conflict and enroll student in both
        Course course = new Course("Physics 200", 3, "Parker", "Physical Sciences Building", 8, 30, 60);
        Course course2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 8, 45, 60);
        cms.addCourse(course);
        cms.addCourse(course2);
        course.enrollStudent(student);
        course2.enrollStudent(student);
        assertEquals(true, cms.hasConflict(student));

        //add two courses with no conflict and enroll student2 in both


        student = new Student("first", "last");
        cms = new CMSu();
        course = new Course("Physics 200", 3, "Parker", "Physical Sciences Building", 8, 30, 60);
        course2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 10, 45, 60);
        course.enrollStudent(student);
        course2.enrollStudent(student);
        assertEquals(false, cms.hasConflict(student));

    }

    @Test
    void testAuditCredits() {
        //exceeds credit limit
        Student student = new Student("first", "last");
        Student student2 = new Student("first2", "last2");
        CMSu cms = new CMSu();
        //add two courses that have conflict and enroll student in both
        Course course = new Course("Physics 200", 7, "Parker", "Physical Sciences Building", 8, 30, 60);
        Course course2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 8, 45, 60);
        cms.addCourse(course);
        cms.addCourse(course2);
        student.adjustCredits(11);
        student2.adjustCredits(11);
        course.enrollStudent(student);
        course2.enrollStudent(student);
        course.enrollStudent(student2);
        course2.enrollStudent(student2);
        StudentSet students = new StudentSet();
        students.add(student);
        students.add(student2);
        //assertEquals(students, cms.auditCredits(2));


        Student studentt = new Student("first", "last");
        Student studentt2 = new Student("first2", "last2");
        CMSu cmss = new CMSu();
        //add two courses that have conflict and enroll student in both
        Course coursee = new Course("Physics 200", 7, "Parker", "Physical Sciences Building", 8, 30, 60);
        Course coursee2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 8, 45, 60);
        cmss.addCourse(course);
        cms.addCourse(course2);
        student.adjustCredits(11);
        student2.adjustCredits(11);
        course.enrollStudent(student);
        course2.enrollStudent(student);
        course.enrollStudent(student2);
        course2.enrollStudent(student2);
        StudentSet studentss = new StudentSet();
        //assertEquals(studentss, cms.auditCredits(15));


    }

    @Test
    void testCheckCreditConsistency() {
        Student student = new Student("first", "last");
        Student student2 = new Student("first2", "last2");
        CMSu cms = new CMSu();
        Course course = new Course("Physics 200", 7, "Parker", "Physical Sciences Building", 8, 30, 60);
        Course course2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 8, 45, 60);
        cms.addCourse(course);
        cms.addCourse(course2);
        student.adjustCredits(11);
        student2.adjustCredits(11);
        course.enrollStudent(student);
        course2.enrollStudent(student);
        course.enrollStudent(student2);
        course2.enrollStudent(student2);
        assertEquals(false, cms.checkCreditConsistency());

        Student studentt = new Student("first", "last");
        Student studentt2 = new Student("first2", "last2");
        CMSu cmss = new CMSu();
        Course coursee = new Course("Physics 200", 3, "Parker", "Physical Sciences Building", 8, 30, 60);
        Course coursee2 = new Course("Biology 100", 4, "Jack", "Physical Sciences Building", 8, 45, 60);
        cmss.addCourse(coursee);
        cmss.addCourse(coursee2);
        studentt.adjustCredits(10);
        studentt2.adjustCredits(5);
        coursee.enrollStudent(studentt);
        coursee2.enrollStudent(studentt);
        coursee.enrollStudent(studentt2);
        coursee2.enrollStudent(studentt2);
        assertEquals(false, cms.checkCreditConsistency());

    }


}