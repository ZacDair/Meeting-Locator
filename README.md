# Mr McK Nav - Web application for location pathing

# Project Description
Mr McK Nav is a web application built using Python, Flask and web development technologies such as (HTML, CSS, JS).

This application is to solve the issue of a user being lost in an unfamiliar environment,
by generating a path from their starting location to their destination.

The initial premise behind this project was to provide a path finding to meeting rooms, in an unfamiliar office.
However the base functionality could be extended to support pathing solutions in distribution centres taking into account chemical spillages, outbreaks, congestion.
And also to support custom obstacles in officies, such as important meetings, areas under construction or even dynamic obstacles such as fires.


# High Level Explanation

  - An admin uploads a floor plan image of an office, using the image mapping methods converts the image to a usable grid.
  - Once happy that the grid accuratley represents the office floor plan and that path testing works, it can be stored in a database.
  - Admin's may also be required to set the meeting room locations, and stair/elevator locations and to which floor they go to as part of the setup.
  - General users can access floor plans on the web application via a query to the database.
  - Once the floor plan is loaded they can add custom starting locations and destinations and run the pathing algorithm.
  - Or using integration with Outlook, and meeting room location's being previously defined in the grid creation, the user can have their next meeting path displayed automatically.


You can also:
  - Request guest passes for a location that you may be visiting, these timed passes must be approved by an admin
  - Guest passes are timed access to a floor plan

### Setup and Running the Project

Mr McK Nav uses these technologies:

* Python - Version 3.8.2
* Flask - a micro web framework, Python Library
* HTML, CSS, Javascript - Core web technologies for the web application

### Installation

Mr Mck Nav requires [Python](https://www.python.org/) to run.

Install the source code from the repository and Flask in order to run the application.
Any Flask installtion issues see the [Installation guide](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask)
For a basic Flask project see this link [Minimal Flask Project](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application)

Flask setup for Windows:
```cmd
C:\path\to\app>set FLASK_APP= MrMckNav-Main.py
```

Flask setup for Linux:
```sh
$ export FLASK_APP= MrMckNav-Main.py
$ flask run
```

Pycharm also supports a preset Flask project structure, this structure allows the project to be ran in pycharm with minimal prior setup
### Project Structure

Mr McK Nav Currently consists of:

| File Name | Description |
| ------ | ------ |
| .git | Git Repository Files |
| .idea | Pycharm IDE Files |
| Static | Javascript Pathing File |
| templates | Core Website Code |
| MrMckNav-Main | Main Backend Logic|

Templates Folder contains: 
- admin.html - Core admin functions, loads the grid, allows editing and testing of the pathing.
- index.html - Acts as a landing page for the admin to upload an image, the form submit leads to the admin.html with the grid data.
- temp-client.html - Temporary dev file, that was used but is now deprecated.
