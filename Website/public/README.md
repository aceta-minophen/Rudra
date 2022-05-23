<img src="Rudra.svg" align="right" width="200">

# Rudra Website
## Architecture

1. Index Page - `css, html`
    1. Sign-in/log-in
    2. Rudra Description
2. Sign-In page - `css, html, js`
    1. Sign in 
3. Users
    1. Admins
        1. Heads
            - Viewing all team heirarchy
            - Assigning tasks
            - Viewing tasks of individuals
            - Creating new users
            - Creating groups
            - Track Progress
        2. Group Leaders
            - See group agenda
            - Assign tasks to group members
            - View Group members
            - Track Progress
            - View other groups
        3. Members
            - View profiles
            - View assigned tasks and completion date
            - Update task Status
            - Create subtasks

## Database
1. Users
    1. UserName = collegeName+fullEnrollmentNo
        1. Password
        2. Name
        3. AccessLevel = Heads | Leaders | Members
        4. Assigned Tasks
            1. Task1
            2. Task2
            3. Task3, etc.
2. Rudra
    1. Heads
        1. Company Heirarchy
            1. Leaders:
                1. Name1:
                    1. Leader of?
                    2. Members in group:
                        1. Mem1
                            1. Task Assigned 1
                                1. Assignment date
                                2. Due date
                            2. Tasks Assigned 2
                        2. Mem2
                            1. Task Assigned 1
                                1. Assignment date
                                2. Due date
                            2. Tasks Assigned 2
                        3. Mem3, etc
                    3. Task assigned to group
                2. Name2, etc.
3. Tasks
    1. Task Title 1:
        1. Assigned to?
        2. Task Details
        3. Subtasks:
            1. Subtask1
            2. Subtask2, etc.
    2. Task Title 2, etc.