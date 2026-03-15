# 15113-hw6-database-exploration

Video demo: https://drive.google.com/file/d/1hH7D-VRyFd-fLSzqF7pmODmDrpkcs3bY/view?usp=sharing

For my hw6 assignment, I decided to build a cruise tracker. My family loves to cruise, and it is one of our favorite vacations! I thought this could be a very practical tool for my family to use to organize our cruise vacations. I created a single table called cruises with 7 columns: cruise_id (integer, primary key), cruise_line (text, required), ship_name (text, required), departure_date (text, required), duration_nights (integer, required), loyalty_status (text, optional), total_fare (real, required). My app can be run with the command python app.py. Here is a brief description of how each CRUD operation is implemented and performed by a user:

Create (INSERT):

- Implemented in the add_new_cruise function with the SQL statement INSERT INTO cruises to add a new trip, safely passing the user's inputs (like cruise_line and total_fare) into the database using parameterized queries (?)
- User performs this CRUD operation by choosing to add a new cruise

Read (SELECT):

- Implemented in the show_all_cruises, search_by_line, and sort_cruises_by_date functions with the SQL statement SELECT \* FROM cruises, using WHERE or ORDER BY clauses to filter by a specific cruise line or sort by departure date
- User performs this CRUD operation by choosing to show all cruises, search by cruise line, or sort by departure date

Update (UPDATE):

- Implemented in the update_cruise function with the SQL statement UPDATE cruises SET... to modify existing details (like fixing a typo in ship_name), pinpointing the exact record by matching the user's chosen cruise_id in the WHERE clause
- User performs this CRUD operation by choosing to update a cruise

Delete (DELETE):

- Implemented in the delete_cruise function with the SQL statement DELETE FROM cruises, critically using a WHERE cruise_id = ? clause to ensure only that specific trip is removed from the database
- User performs this CRUD operation by choosing to delete a cruise
