## Preview

https://github.com/aidan2b/game-of-life/assets/80802578/bce898ec-b0db-44a4-b20a-1efe19899926

## Potential improvements

### Optimization \[2/2\]

-   [x] Sparse Representation: Storing only the live cells in a set.
-   [x] Avoid Redundant Drawing: Only redraw the changed cells instead
    of the entire grid.

### User Interface Enhancements \[1/4\]:

-   [ ] Zoom In/Out: Allow the user to zoom in or out, especially if the
    grid size is large.
-   [ ] Drag and Move: Implement a feature to move around the grid.
-   [ ] Predefined Patterns: Allow the user to select and place
    predefined patterns (like gliders or spaceships).
-   [x] Adjust Simulation Speed: Add a slider or buttons to speed up,
    slow down, or step through the simulation one frame at a time.

### Advanced Features \[5/5\]

-   [x] Save and Load: Allow users to save their current pattern and
    load it later.
-   [x] Boundary Conditions: Add options for different boundary
    conditions, like wrapping around the edges (toroidal array) to
    create a continuous world.
-   [x] Color: Introduce more colors. Could color recently born cells
    with a different shade, giving a visual indication of changes.
-   [x] Statistics: Display the number of living cells, the generation
    number, etc.
-   [X] Rule Variations: The classic Game of Life is just one rule-set
    of cellular automata. Allow users to define their own rules.

### Code Refinement \[2/3\]

-   [X] Modularization: UI operations, grid handling, and simulation
    logic into separate classes or modules.
-   [X] Documentation: Add inline comments and perhaps a user guide.
-   [ ] Error Handling: Add more comprehensive error handling for user
    inputs or file operations.

### Expand Beyond 2D \[0/1\]

-   [ ] 3D version of Conway\'s Game of Life.

### Testing \[0/1\]

-   [ ] Adding unit tests for core functionalities.
