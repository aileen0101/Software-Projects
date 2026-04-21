package cs2110;

/**
 * A course managed by the CMSμ course management system.  Courses are assumed to meet every day of
 * the week.
 */
public class Course {

    /**
     * Set of all students enrolled in this Course.
     */
    private StudentSet students;

    /**
     * The title of this course (e.g. Object-Oriented Programming and Data Structures).  Must be
     * non-empty.
     */

    private String title;

    /**
     * Number of credit hours students will receive upon completing this course.  Must be
     * non-negative.
     */
    private int credits;

    /**
     * The last name of the professor of this course (e.g. Myers).  Must be non-empty.
     */
    private String prof;

    /**
     * The location of lectures at this course (e.g. Statler Hall room 185).  Must be non-empty.
     */
    private String location;

    /**
     * The start time of this course's daily meetings, expressed as the number of minutes after
     * midnight.  Must be between 0 and 1439, inclusive.
     */
    private int startTimeMin;

    /**
     * The duration of this course's daily meetings, in minutes.  Must be positive, and
     * `startTimeMin + durationMin` must be no greater than 1440.
     */
    private int durationMin;

    /**
     * Assert that this object satisfies its class invariants.
     */
    private void assertInv() {
        assert this.students != null;
        assert this.title.length() != 0;
        assert this.credits >=0;
        assert this.prof.length() !=0;
        assert this.location.length() !=0;
        assert this.startTimeMin <= 1439;
        assert this.startTimeMin >=0;
        assert this.durationMin >=0;
        assert this.startTimeMin + this.durationMin < 1440;
    }

    /**
     * Create a course with title `title`, taught by a professor with last name `profName`, where
     * lectures of duration `duration` minutes start at local time `startHr`:`startMin` and take
     * place in a location described by `location`.  The course counts for `credits` credit hours
     * and initially has no students. Requires `title`, `profName`, and `location` are non-empty,
     * `startHr` is between 0 and 23 (inclusive), `startMin` is between 0 and 59 (inclusive), and
     * `credits` is non-negative. `duration` must be positive and must imply an end time no later
     * than midnight.
     */
    public Course(String title, int credits, String profName, String location,
            int startHr, int startMin, int duration) {

        assert startHr >=0;
        assert startHr<=23;
        assert startMin >=0;
        assert startMin <=59;
        assert credits >=0;
        assert duration >=0;
        Integer startTime = 60*startHr + startMin;
        this.startTimeMin = startTime;
        assert duration + startTime < 1440;

        this.durationMin = duration;
        this.title = title;
        this.prof = profName;
        this.location = location;
        this.credits=credits;
        Integer startTimee = 60*startHr + startMin;
        this.startTimeMin = startTimee;
        this.students = new StudentSet();

        assertInv();

    }

    /**
     * Return the title of this course.
     */
    public String title() {
        return title;
    }

    /**
     * Return the number of credit hours awarded for completing this course.  Will not be negative.
     */
    public int credits() {
        return credits;
    }

    /**
     * Return the location of lectures in this course.
     */
    public String location() {
        return location;
    }

    /**
     * Return the last name of the instructor teaching the course, prefixed by the title "Professor"
     * (separated by a space).
     */
    public String instructor() {
        return "Professor" + " " + this.prof;
    }

    /**
     * Return the time at which lectures are held for this course in the format hour:min AM/PM using
     * 12-hour time. For example, "11:15 AM", "1:35 PM". Add leading zeros to the minutes if
     * necessary.
     */
    public String formatStartTime() {

        Integer hour = (Integer)this.startTimeMin/60;
        Integer min = startTimeMin - hour*60;
        if (( hour > 12 ) && (hour < 24)) {
            hour = hour -12;
            return Integer.toString(hour) + ":" + Integer.toString(min) + " PM";
        }
        if (hour == 24){
            return "0" + ":" + Integer.toString(min) + " AM";
        }

        if (hour ==12){
            return "12" + ":" + Integer.toString(min) + " PM";
        }

        return Integer.toString(hour) + ":" + Integer.toString(min) + " AM";

    }

    /**
     * Return whether this course's daily meetings overlap with those of `course` by at least 1
     * minute.  For example:
     * <ul>
     *   <li>A course that starts at 10:00 AM and has a duration of 60 minutes does **not** overlap
     *       with a course that starts at 11:00 AM and has a duration of 60 minutes.
     *   <li>A course that starts at 10:00 AM and has a duration of 61 minutes **does** overlap with
     *       a course that starts at 11:00 AM and has a duration of 60 minutes.
     * </ul>
     */
    public boolean overlaps(Course course) {
        Integer course_startMin = course.startTimeMin;
        Integer course_endMin = course.startTimeMin + course.durationMin;
        Integer endMin = this.startTimeMin + this.durationMin;
        Integer startMin = this.startTimeMin;

        return (startMin >= course_startMin && endMin <= course_endMin) || (startMin>= course_startMin && startMin <= course_endMin) ||
                (endMin>=course_startMin && endMin <=course_endMin)|| (startMin <= course_startMin && endMin >= course_endMin) || (course_startMin >= startMin && course_startMin <= endMin) ||
                (course_endMin >= startMin && course_endMin <= endMin);

    }

    /**
     * Return whether `student` is enrolled in this course.
     */
    public boolean hasStudent(Student student) {
        return this.students.contains(student);
    }

    /**
     * Enroll `student` in this course if they were not enrolled already, adjusting their credit
     * count accordingly.  Return whether this causes a change in the enrollment of the course.
     */
    public boolean enrollStudent(Student student) {
        if (this.hasStudent(student) != true){
            this.students.add(student);
            student.adjustCredits(this.credits);
            return true;
        }

        return false;
    }

    /**
     * Drop Student `student` from this course if they are currently enrolled, adjusting their
     * credit count accordingly.  Return whether this causes a change in the enrollment of the
     * course.
     */
    public boolean dropStudent(Student s) {
        if (this.hasStudent(s)) {
            this.students.remove(s);
            s.adjustCredits(-1*this.credits);
            return true;
        }

        return false;
    }

    /**
     * Return the String representation of the list of students enrolled in this course
     */
    public String formatStudents() {
        return students.toString();
    }
}
