# Part I
* Overview of databases and SQL
* List of references
  * W3schools Tutorial
  * Official SQLite documentation
  * Python sqlite3 documentation
* Google Colab instructions
  * Colab database wget cell
## I. Getting a Database Connection
* Cell: imports
* Cell: connection
## II. Getting Started
### A. Our First Query
* cell: SELECT * FROM teams;
* description of first query
### B. Choosing Columns
* SELECT team_name, team_number FROM teams;
### C. Displaying different Column Names
* Aliases
* cell: SELECT team_name AS Team, ...
### D. Filtering with WHERE clause
* cell: SELECT * FROM teams WHERE year_founded = 2013;
* cell: WHERE clause with AND
### E. SQL Syntax and Style
## III. Exploring Tables and Schemas
### A. Table of Tables
* cell: ...FROM sqlite_schema...
### B. Database schemas
* cell: SELECT sql FROM sqlite_schema ...
#### Pragma Queries
* cell: SELECT * FROM schedule ...
* cell: schedule LEFT JOIN teams ...
## VI. Running Queries
### A. read_sql_query()
### C. Closing Connections
### E. SQLite on Command Line
### Mathematical Calculations in SQL
### Exercises



# Part II
* Intro
## More Ways to Execute Queries
### connection.execute
### Using cursor objects
## Creating Tables
* Awards Table?
## Updating Records
## Inserting Records
## Parameterizing Queries
## Joining Tables
## Aggregate Queries
## Nested Queries
## Views
## Window Queries