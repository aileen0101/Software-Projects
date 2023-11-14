package cs2110;

import java.io.PrintWriter;
import java.util.*;

/**
 * Stores the academic genealogy of a "root" professor, defined as all professors who earned a PhD
 * while primarily advised by the root professor, as well as everyone those professors similarly
 * advised, and so on.  This genealogy forms a tree, where each node represents a person who earned
 * a PhD, and the edges represent advisor-advisee relationships.  All professor names must be
 * distinct.
 */
public class PhDTree {

    /**
     * The Professor at the root of this PhDTree. i.e. the Professor at this "node" in an academic
     * genealogy tree. All nodes of a PhDTree have a different Professor in them. The professors'
     * names are all distinct - there are no duplicates.
     */
    private Professor professor;

    /**
     * The direct advisees of the professor at the root of this PhDTree. Each element of this set is
     * an advisee of the professor at this node.  The PhDTree nodes reachable via `advisees` form a
     * tree.
     */
    private SortedSet<PhDTree> advisees;

    /**
     * Assert that the class invariant is satisfied.  Specifically, asserts that all professor names
     * in the tree are distinct and that no node is reachable from more than one parent.
     */
    private void assertInv() {
        Set<String> seenProfs = new HashSet<>();
        Set<PhDTree> seenNodes = new HashSet<>();
        assertInvTraverse(seenProfs, seenNodes);
    }

    /**
     * Recursive helper method for classInv. Traverses the tree from this node, adding all
     * Professors and nodes seen to the respective "seen" sets. Things added must not already be in
     * the set, as that would imply that either the values in the tree are not distinct or that the
     * data structure is not a tree.
     */
    private void assertInvTraverse(Set<String> seenProfs, Set<PhDTree> seenNodes) {
        assert !seenNodes.contains(this) : "node " + this + " is not unique";
        assert !seenProfs.contains(professor.name()) : "prof " + professor + " is not unique";
        seenProfs.add(professor.name());
        seenNodes.add(this);
        for (PhDTree advisee : advisees) {
            advisee.assertInvTraverse(seenProfs, seenNodes);
        }
    }

    /**
     * Create a new PhDTree with `prof` as the root professor and no advisees.
     */
    public PhDTree(Professor prof) throws IllegalArgumentException {
        assert prof != null;
        this.professor = prof;
        // The elements of this set will be iterated in order according to the ordering of the
        // nodes' professors.  Since `PhDTree` is not `Comparable` itself, an anonymous function is
        // used to tell the comparator to look at its professor instead.
        advisees = new TreeSet<>(Comparator.comparing(node -> node.professor));
        assertInv();
    }

    /**
     * Return the Professor at the root of this PhDTree.
     */
    public Professor prof() {
        return professor;
    }

    /**
     * Return the number of direct advisees of the professor at the root of this PhDTree.
     */
    public int numAdvisees() {
        // TODO 1: Implement this method according to its specification.
        // The implementation can be a one-liner.
       return advisees.size();
    }

    /**
     * Return the number of professors in this tree with no advisees of their own.
     */
    public int numLeaves() {
        // Base case: this node is a leaf
        if (numAdvisees() == 0) {
            return 1;
        }

        // This is a counting method
        int totalLeaves = 0;
        for (PhDTree advisee : advisees) {
            totalLeaves += advisee.numLeaves();
        }
        return totalLeaves;
    }

    /**
     * Return a professor in this PhDTree who has at least `minAdvisees` advisees, if one exists.
     * Otherwise, throws `NotFound`.
     */
    public Professor findProlificMentor(int minAdvisees) throws NotFound {
        // This is a searching method

        // Base case: this node's professor qualifies
        if (numAdvisees() >= minAdvisees) {
            return professor;
        }

        // Recursive case: search each child
        for (PhDTree advisee : advisees) {
            try {
                return advisee.findProlificMentor(minAdvisees);
            } catch (NotFound exc) {
                // Continue (search the next child)
            }
        }

        // Not found under any child; throw an exception ourselves.
        throw new NotFound();
    }

    /**
     * Return the number of professors in this PhDTree.
     */
    public int size() {
        // TODO 2: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        // Hint: the size of a tree is just the sum of the sizes of the subtrees rooted at its
        // children, plus 1.  So call `c.size()` on each immediate child node `c`, add the results,
        // and add 1 more!
        //throw new UnsupportedOperationException();

        //Base case:
        if (numAdvisees() == 0){
            return 1;
        }

        //finding size for each non-root node
        int size = 0;
        for (PhDTree advisee: advisees){
            size = size + advisee.size();
        }

        return size + 1;
    }

    /**
     * Return the number of professors along the longest path from the root of this PhDTree to a
     * professor with no advisees (a leaf).  If the professor at the root of this PhDTree has no
     * advisees, its depth is 1.
     */
    public int maxDepth() {
        // TODO 3: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        // Hint: how can you use the result of `c.maxDepth()`, for each child `c`, to obtain the
        // maximum depth from the current node?
        //throw new UnsupportedOperationException();

        //Base case:
        if (this.numAdvisees()==0){
            return 1;
        }
        int maxdepth = 0;
        for (PhDTree advisee: advisees){
            int ad_depth = advisee.maxDepth();
            if (ad_depth>maxdepth){
                maxdepth=ad_depth;
            }
        }

        return maxdepth + 1;
    }

    /**
     * Return the subtree with a professor named `targetName` at the root if such a professor is in
     * this PhDTree. Throws `NotFound` if `target` is not in this PhDTree.
     */
    public PhDTree findTree(String targetName) throws NotFound {
        // TODO 4: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        // Since the method can throw an exception, your recursive calls will need to happen inside
        // a try–catch block so that you can handle their exceptions and do the right thing.
        //throw new UnsupportedOperationException();

        //root professor has this name
        if (this.professor.name().equals(targetName)){
            return this;
        }

        //Look at each advisee node
        for (PhDTree advisee: advisees){
            try{
                return advisee.findTree(targetName);
            } catch (NotFound ex){

            }

        }
        throw new NotFound();
    }

    /**
     * Returns true if this PhDTree contains Professor `targetName` (either at the root or among the
     * root's advising descendants).
     */
    public boolean contains(String targetName) {
        try {
            findTree(targetName);
            return true;
        } catch (NotFound exc) {
            return false;
        }
    }

    /**
     * Extend the subtree rooted at the professor named `advisorName` with a new advisee,
     * `newAdvisee`. Requires `newAdvisee` is not already in this PhDTree. Throws `NotFound` if
     * `advisorName` is not the name of any professor in this PhDTree.
     */
    public void insert(String advisorName, Professor newAdvisee) throws NotFound {
        // TODO 5: Implement this method according to its specification.
        // Implementation constraint: This method should NOT be recursive.
        // Use findTree(), above.  Do not use any methods that are below.
        // DO NOT traverse the tree twice looking for the same professor--don't duplicate work.

        //throw new UnsupportedOperationException();

        assert !this.contains(newAdvisee.name());

        //find the node

            PhDTree advisor = findTree(advisorName);
            //Create new PhDTree with newAdvisee
            PhDTree newTree = new PhDTree(newAdvisee);
            //add the newAdvisee
            advisor.advisees.add(newTree);

    }


    /**
     * Return the immediate advisor of the professor named `targetAdviseeName`, or throw `NotFound`
     * if `targetAdviseeName` is not an advising descendant of the professor at the root of this
     * PhDTree.
     */
    public Professor findAdvisor(String targetAdviseeName) throws NotFound {
        // TODO 6: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        //throw new UnsupportedOperationException();

        //Base case: check immediate children of our root node
//        try {
            for (PhDTree advisee: advisees){
                if (advisee.prof().name().equals(targetAdviseeName)){
                    return professor;
                }
                else{
                    try {
                        return advisee.findAdvisor(targetAdviseeName);
                    }
                    catch ( NotFound ex){
                        //keep going to each advisee
                    }
                }
            }

//        catch ( NotFound ex){
//            //keep going to each advisee
//        }

        throw new NotFound();

    }

    /**
     * Return the professors on the path between the root of this PhDTree and the descendant
     * professor named `targetName`.  The path should start with the root advisor and end with
     * professor `targetName`, and each element (except the first) is preceded by their advisor.
     * Throws `NotFound` if there is no such path.
     */
    public List<Professor> findAcademicLineage(String targetName) throws NotFound {
        // TODO 7: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        // Do not use findAdvisor() in this method: it is too inefficient, leading to multiple
        // traversals of the tree. This method must return an object satisfying the interface
        // `List<Professor>`. Recall that `List<T>` is an interface, so use a class that implements
        // it, like `java.util.LinkedList<T>`.  Choose an implementation that provides your
        // most-used operations efficiently.
        // Hint: The base case is when the root of this PhDTree is `targetName`, in which case the
        // lineage is a list containing only `targetName`.
        //throw new UnsupportedOperationException();


        //base case: root name = targetName
        List<Professor> list = new LinkedList<>();

        if (this.professor.name().equals(targetName)) {
            list.add(this.professor);
            return list;
        }

        for (PhDTree advisee: advisees){
            try {
                List<Professor> list2 = advisee.findAcademicLineage(targetName);
                list2.add(0, professor);
                return list2;
            }
            catch (NotFound ex){
                //go to next child
            }
        }
        throw new NotFound();

    }


    /**
     * Return the professor at the root of the smallest subtree of this PhDTree that contains
     * professors named `prof1Name` and `prof2Name`, if such a subtree exists. Otherwise, throw
     * `NotFound`.
     */
    public Professor commonAncestor(String prof1Name, String prof2Name) throws NotFound {
        // TODO 8: Implement this method according to its specification.
        // Implementation constraint: Do not use `findAdvisor()` for this: it is too inefficient.
        // Instead, use `findAcademicLineage()` to find the routes to the two advisees, then iterate
        // over the common prefix of the routes.  If iterating using indices, ensure that the data
        // structure can be iterated over efficiently.
        //throw new UnsupportedOperationException();

        //find two separate lineages of prof1 and prof2:
        //if (numAdvisees()!=0) {
            List<Professor> lineage1 = findAcademicLineage(prof1Name);
            List<Professor> lineage2 = findAcademicLineage(prof2Name);
            //start from lineage1: go through each prof of lineage2 for each prof of lineage1
            Professor commonAdvisor = new Professor(lineage1.get(0));
            for (Professor p1 : lineage1) {
                for (Professor p2 : lineage2) {
                    if (p1.equals(p2)) {
                        commonAdvisor = p1;
                    } else {
                        commonAdvisor = commonAdvisor;
                    }
                }
            }
            return commonAdvisor;
        //}
        //throw new NotFound();
    }

    /**
     * Return a (single line) String representation of this PhDTree. If this PhDTree has no advisees
     * (it is a leaf), return the root professor's name. Otherwise, return the root professor's name
     * + "[" + each advisee node's toString(), separated by ", ", followed by "]".
     * <p>
     * Thus, for the following tree:
     *
     * <pre>
     * Depth:
     *   1      Maya_Leong
     *            /     \
     *   2 Matthew_Hui  Curran_Muhlberger
     *           /          /         \
     *   3 Amy_Huang    Andrew_Myers   Tomer_Shamir
     *           \
     *   4    David_Gries
     *
     * Maya_Leong.toString() should print:
     * Maya Leong[Matthew Hui[Amy Huang[David Gries]]], Curran Muhlberger[Andrew Myers, Tomer Shamir]]
     *
     * Matthew_Hui.toString() should print:
     * Matthew Hui[Amy Huang[David Gries]]
     *
     * Andrew_Myers.toString() should print:
     * Andrew Myers
     * </pre>
     */
    @Override
    public String toString() {
        if (advisees.isEmpty()) {
            return professor.name();
        }
        StringBuilder s = new StringBuilder();
        s.append(professor.name())
                .append("[");
        boolean first = true;
        for (PhDTree advisee : advisees) {
            if (!first) {
                s.append(", ");
            }
            first = false;
            s.append(advisee);
        }
        s.append("]");
        return s.toString();
    }

    /**
     * Print each professor in this tree to `out`.  Each professor is printed on their own line in
     * the format NAME - YEAR.
     * <p>
     * For the tree in the specification for `toString()`, its output might be:
     * <pre>
     * Maya Leong - 2005
     * Matthew Hui - 2023
     * David Gries - 1966
     * Curran Muhlberger - 2014
     * Andrew Myers - 1999
     * Tomer Shamir - 2023
     * </pre>
     */
    public void printProfessors(PrintWriter out) {
        // TODO 9: Implement this method according to its specification.
        // Implementation constraint: This method must be recursive.
        // Traverse the tree in PREORDER, respecting the ordering of advisees.

        //How to do preorder traversal
        //Maya Leong[Matthew Hui[Amy Huang[David Gries]]], Curran Muhlberger[Andrew Myers, Tomer Shamir]]

        //Base case: tree with no leaves

        String profString = "";
        if (numAdvisees()==0){
            //profString += professor.name() + " - " + professor.phdYear();
            out.println(this.professor.name() + " - " + this.professor.phdYear());
        }
        else{
            out.println(professor.name()+ " - " + professor.phdYear());
            for (PhDTree advisee: advisees){
                advisee.printProfessors(out);
            }
        }

    }
}
