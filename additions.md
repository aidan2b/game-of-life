Potential improvements and features you could add to your Conway\'s Game
of Life implementation:

# Optimization \[2/2\]

-   [x] Sparse Representation: Storing only the live cells in a set.
-   [x] Avoid Redundant Drawing: Only redraw the changed cells instead
    of the entire grid.

# User Interface Enhancements \[1/4\]:

-   [ ] Zoom In/Out: Allow the user to zoom in or out, especially if the
    grid size is large.
-   [ ] Drag and Move: Implement a feature to move around the grid.
-   [ ] Predefined Patterns: Allow the user to select and place
    predefined patterns (like gliders or spaceships).
-   [x] Adjust Simulation Speed: Add a slider or buttons to speed up,
    slow down, or step through the simulation one frame at a time.

# Advanced Features \[2/5\]

-   [x] Save and Load: Allow users to save their current pattern and
    load it later.
-   [x] Boundary Conditions: Add options for different boundary
    conditions, like wrapping around the edges (toroidal array) to
    create a continuous world.
-   [x] Color: Introduce more colors. Could color recently born cells
    with a different shade, giving a visual indication of changes.
-   [x] Statistics: Display the number of living cells, the generation
    number, etc.
-   [ ] Rule Variations: The classic Game of Life is just one rule-set
    of cellular automata. Allow users to define their own rules.

# Code Refinement \[/\]

-   [-] Modularization: UI operations, grid handling, and simulation
    logic into separate classes or modules.
-   [ ] Documentation: Add inline comments and perhaps a user guide.
-   [ ] Error Handling: Add more comprehensive error handling for user
    inputs or file operations.

# Expand Beyond 2D \[/\]

-   [ ] 3D version of Conway\'s Game of Life.

# Testing \[/\]

-   [ ] Adding unit tests for core functionalities.
