package cs2110;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * The main program for the CMSμ course management system.
 */
public class Main {

    public static void main(String[] args) {
        Main app = new Main();
        if (args.length > 0) {
            File file = new File("tests", args[0]);
            try {
                app.processCommands(new Scanner(file), true);
            } catch (FileNotFoundException e) {
                System.out.println("File not found: " + file);
            }
        } else {
            app.processCommands(new Scanner(System.in), false);
        }
    }

    CMSu cms;

    public Main() {
        cms = new CMSu();
    }

    /**
     * Read commands from a Scanner and execute them. Return when the "exit" command is read.
     * If `echo` is true, print the read command after the prompt.
     *
     * @param sc The scanner
     */
    public void processCommands(Scanner sc, boolean echo) {
        while (true) {
            System.out.print("Please enter a command: ");
            String input = sc.nextLine().trim();
            if (echo) {
                System.out.println(input);
            }
            String[] words = input.split(" ");
            switch (words[0]) {
                case "help":
                    getCommandHelp();
                    break;
                case "addstudent":
                    runAddStudentCommand(words);
                    break;
                case "addcourse":
                    runAddCourseCommand(words);
                    break;
                case "enroll":
                    runEnrollCommand(words);
                    break;
                case "drop":
                    runDropCommand(words);
                    break;
                case "courses":
                    runListCoursesCommand();
                    break;
                case "students":
                    runListStudentsCommand();
                    break;
                case "enrollment":
                    runListEnrollmentCommand(words);
                    break;
                case "exit":
                    return;
                default:
                    System.out.println(
                            "This is not a valid command. For help, enter the command \"help\"");
            }
        }
    }

    public void getCommandHelp() {
        System.out.println("\nhelp\n" +
                "  Output a summary of all available commands\n" +
                "addstudent <firstName> <lastName>\n" +
                "  Create a new student with the specified name\n" +
                "addcourse <courseName> <profName> <location> <time (24-hour)> <duration (min)> <credits>\n"
                +
                "  Create a new course with the specified properties\n" +
                "enroll <student ID> <course ID>\n" +
                "  Enroll the specified student in the specified course\n" +
                "drop <student ID> course ID>\n" +
                "  Drop the specified student from the specified course\n" +
                "students\n" +
                "  List all students being tracked\n" +
                "courses\n" +
                "  List all courses being tracked\n" +
                "enrollment <course ID>\n" +
                "  List all students enrolled in the specified course\n" +
                "exit\n" +
                "  Exit the program\n");
    }

    private void invalidCommand(String cmd) {
        System.out.println("Invalid " + cmd + " command. " +
                "Enter the command \"help\" for information about that command.");
    }

    public void runAddStudentCommand(String[] command) {
        if (command.length != 3) {
            invalidCommand("addstudent");
            return;
        }
        if (cms.canAddStudent()) {
            String first = command[1];
            String last = command[2];
            Student newStudent = new Student(first, last);
            cms.addStudent(newStudent);
            System.out.println(
                    "Successfully created new student: " + newStudent);
        } else {
            System.out.println("ERROR: insufficient capacity to add a new student");
        }
    }

    public void runAddCourseCommand(String[] command) {
        if (command.length != 7) {
            invalidCommand("addcourse");
            return;
        }
        String name = command[1];
        String prof = command[2];
        String loc = command[3];
        int hr;
        int min;
        String time = command[4];
        String[] timeArr = time.split(":");
        if (timeArr.length < 2) {
            System.out.println("Invalid time input");
            return;
        } else {
            try {
                hr = Integer.parseInt(timeArr[0]);
                if (hr < 0 || hr > 23) {
                    System.out.println("Invalid time input");
                    return;
                } else {
                    min = Integer.parseInt(timeArr[1]);
                    if (min < 0 || min > 59) {
                        System.out.println("Invalid time input");
                        return;
                    }
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid time input");
                return;
            }
        }
        int dur;
        try {
            dur = Integer.parseInt(command[5]);
        } catch (NumberFormatException e) {
            System.out.println("Invalid duration input");
            return;
        }
        int cred;
        try {
            cred = Integer.parseInt(command[6]);
        } catch (NumberFormatException e) {
            System.out.println("Invalid credit input");
            return;
        }
        Course newCourse = new Course(name, cred, prof, loc, hr, min, dur);
        if (cms.canAddCourse()) {
            cms.addCourse(newCourse);
            System.out.println(
                    "Successfully created new course: " + newCourse.title() + " taught by "
                            + newCourse.instructor() + " at " + newCourse.formatStartTime()
                            + ", Location: "
                            + newCourse.location()
                            + ", Duration: " + dur + " min, Credits: " + newCourse.credits());
        } else {
            System.out.println("ERROR: insufficient capacity to add a new course");
        }
    }

    public void runEnrollCommand(String[] command) {
        if (command.length != 3) {
            invalidCommand("enroll");
            return;
        }

        int studentId = -1;
        int courseId = -1;
        try {
            studentId = Integer.parseInt(command[1]);
            courseId = Integer.parseInt(command[2]);
        } catch (NumberFormatException e) {
            invalidCommand("enroll");
            return;
        }

        if (!cms.isValidStudentId(studentId) || !cms.isValidCourseId(courseId)) {
            System.out.println("One of the IDs you provided is invalid");
            return;
        }

        Student student = cms.getStudent(studentId);
        Course course = cms.getCourse(courseId);

        if (course.enrollStudent(student)) {
            System.out.println(student +
                    " was successfully enrolled in " + course.title());
        } else {
            System.out.println(student +
                    " is already enrolled in " + course.title());
        }
    }

    public void runDropCommand(String[] command) {
        if (command.length != 3) {
            invalidCommand("drop");
            return;
        }

        int studentId = -1;
        int courseId = -1;
        try {
            studentId = Integer.parseInt(command[1]);
            courseId = Integer.parseInt(command[2]);
        } catch (NumberFormatException e) {
            invalidCommand("enroll");
            return;
        }

        if (!cms.isValidStudentId(studentId) || !cms.isValidCourseId(courseId)) {
            System.out.println("One of the IDs you provided is invalid");
            return;
        }

        Student student = cms.getStudent(studentId);
        Course course = cms.getCourse(courseId);

        boolean success = course.dropStudent(student);
        if (success) {
            System.out.println(student +
                    " was successfully dropped from " + course.title());
        } else {
            System.out.println(student +
                    " is not enrolled in " + course.title());
        }
    }

    public void runListStudentsCommand() {
        System.out.println();
        cms.printStudents(System.out);
    }

    public void runListCoursesCommand() {
        System.out.println();
        cms.printCourses(System.out);
    }

    public void runListEnrollmentCommand(String[] command) {
        if (command.length != 2) {
            invalidCommand("list enrollment");
            return;
        }
        try {
            int courseId = Integer.parseInt(command[1]);
            if (!cms.isValidCourseId(courseId)) {
                System.out.println("The ID you provided is invalid");
                return;
            }
            Course course = cms.getCourse(courseId);
            System.out.println(course.formatStudents());
        } catch (NumberFormatException e) {
            invalidCommand("list enrollment");
        }
    }
}
