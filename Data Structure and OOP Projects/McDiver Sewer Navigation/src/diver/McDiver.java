package diver;

import game.*;

import java.util.*;

import graph.*;


/** This is the place for your implementation of the {@code SewerDiver}.
 */
public class McDiver implements SewerDiver {

    /** See {@code SewerDriver} for specification. */
    @Override
    public void seek(SeekState state) {
        // TODO : Look for the ring and return.
        // DO NOT WRITE ALL THE CODE HERE. DO NOT MAKE THIS METHOD RECURSIVE.
        // Instead, write your method (it may be recursive) elsewhere, with a
        // good specification, and call it from this one.
        //
        // Working this way provides you with flexibility. For example, write
        // one basic method, which always works. Then, make a method that is a
        // copy of the first one and try to optimize in that second one.
        // If you don't succeed, you can always use the first one.
        //
        // Use this same process on the second method, scram.
        HashSet<Long> visited = new HashSet<>();
        seekDfs(state, visited);


    }
    /**
    Implements the depth first search algorithm recursively for McDiver to find the ring. Once we reach the ring, we return the function.
     **/
    private static void seekDfs(SeekState state, HashSet<Long> visited){
        //ArrayList<Long> visited = new ArrayList<>();
        Long currLoc = state.currentLocation();
        visited.add(state.currentLocation());
        if (state.distanceToRing()==0){
            return;
        }
        for (NodeStatus e: state.neighbors()){
            if (!visited.contains(e.getId())){
                state.moveTo(e.getId());
                seekDfs(state, visited);
                if (state.distanceToRing()==0){
                    return;
                }
                state.moveTo(currLoc);
            }
        }
    }

    /** See {@code SewerDriver} for specification. */
    @Override
    public void scram(ScramState state) {
        // TODO: Get out of the sewer system before the steps are used up.
        // DO NOT WRITE ALL THE CODE HERE. Instead, write your method elsewhere,
        // with a good specification, and call it from this one.

        List<Edge> bestEdges = pathOut(state);
        //moving the diver
        for (Edge ed: bestEdges){
            state.moveTo(ed.destination());
        }
    }

    private static List<Edge> pathOut(ScramState state) {
        Maze maze = new Maze((Set<Node>) state.allNodes());
        ShortestPaths<Node,Edge> pathOut = new ShortestPaths(maze);
        pathOut.singleSourceDistances(state.currentNode());
        List<Edge> bestEdges = pathOut.bestPath(state.exit());
        return bestEdges;
    }

}
