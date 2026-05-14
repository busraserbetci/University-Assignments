import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;


public class MazeSolver {

    public static char[][] readMazeGrid(String input) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(input));
        String line;
        int rows = 0;

        while((line = reader.readLine()) != null) {
            rows++;
        }

        reader.close();
        reader = new BufferedReader(new FileReader(input));

        char [][] mazeGrid = new char[rows][];

        int row = 0;
        while((line = reader.readLine()) != null) {
            mazeGrid[row] = line.toCharArray();
            row++;
        }
        reader.close();

        return mazeGrid;
    }

    public static void printMaze(char [][] mazeGrid){
        for(int i = 0; i < mazeGrid.length; i++) {
            for(int j = 0; j < mazeGrid[i].length; j++) {
                System.out.print(mazeGrid[i][j] + " ");
            }
            System.out.println();
        }
    }

    //Direction vectors for right, down, left and up
    static int[] dx = {0 , 1, 0, -1};
    static int[] dy = {1, 0, -1, 0};

    //Check whether a move is valid or not. Return True if the move is valid, otherwise False
    public static boolean canMove(char[][] mazeGrid, boolean[][] visited, int x, int y) {

        //Return true if all conditions are met.
        //Meaning the position is within the maze boundaries, is not a wall ('#'), and has not been visited before
        //Thereby preventing illegal moves and infinite loops.
        return x >= 0 && x < mazeGrid.length && y >= 0 && y < mazeGrid[0].length && mazeGrid[x][y] != '#' && !visited[x][y];

    }

    public static boolean wallFollower(char[][] mazeGrid, boolean[][] visited, int x, int y) {

        visited[x][y] = true; //Mark the start position as visited

        if (mazeGrid[x][y] == 'X') {

            System.out.println("Exit fount at x:" + x + ", y:" + y); //Exit is found
            return true;

        }

        for (int dir = 0; dir < 4; dir++) {
            int newX = x + dx[dir];
            int newY = y + dy[dir];

            if (canMove(mazeGrid, visited, newX, newY)) {
                //Move to the new position and check for the exit
                if (wallFollower(mazeGrid, visited, newX, newY)) {
                    return true; //Exit found in recursion
                }
            }

        }

        //Backtrack if no solution
        visited[x][y] = false;
        return false;

    }

    public static void main(String[] args) throws IOException {

        int startX = Integer.parseInt(args[0]);
        int startY = Integer.parseInt(args[1]);
        String fileName = args[2];

        //Read the maze
        char[][] mazeGrid = readMazeGrid(fileName);
        boolean[][] visited = new boolean[mazeGrid.length][mazeGrid[0].length];

        // Print the maze
        //printMaze(mazeGrid);

        if (!wallFollower(mazeGrid, visited, startX, startY)) {

            System.out.println("There is no solution! ");

        }

    }
}