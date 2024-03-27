README

To run the project, follow these steps :
a. Run all the queries from queries.txt in your mysql local server.
b. Open the app.py file and enter your username and password according to your my sql local server in line no. 15 and 16 of the file.
c. Open windows terminal in the same folder, make sure you have everything installed like flask,mysql.connector and a minimum of python version 3.7.
d. Now, in the windows terminal, type python app.py.
e. Open the link you get on running the above command to access our project and explore the various features.

1. Index Page

Book List Display
Overview: The index page serves as a comprehensive showcase of available books within the system, allowing users to explore the wide array of titles and subjects available for borrowing or reference.

Multi-filtered Book Search
Filtering Criteria: Users can conduct nuanced searches by book name, author, genre, or other specific parameters, refining their search results for precise book discovery.

Enhanced User Experience: This search feature elevates the user experience by providing a more tailored and targeted book search, ensuring users find books that align closely with their preferences.

Book Issuance and Returns
Issuance Process: Users have the functionality to borrow books, facilitating their study or reading needs within the system.
Return Process: Upon completion, users can easily return books, updating the log table in real-time to maintain accurate records of book movements and availability.

College Search and Book Recommendations
College Search: A tool allowing users to search for colleges based on various parameters, aiding in academic planning and decision-making.
Book Recommendations: As users explore colleges, the system offers book suggestions relevant to the type of institution, assisting in finding resources tailored to academic pursuits.

CGPA Calculator
Purpose: A tool to calculate the Cumulative Grade Point Average (CGPA) based on user input, assisting in the identification of colleges that align with the desired CGPA range.
Decision-making Tool: Provides valuable information to users, empowering them to make informed decisions about suitable college options based on their academic performance.


2. Discussion Room Booking

Discussion Room Reservation
Availability Display: The system exhibits unissued slots for discussion rooms in the library, giving users an overview of available spaces.

Issue Functionality: Users can reserve a discussion room for a limited period (typically 2 hours) for academic discussions or collaborative work.

Automated Reset: To maintain fairness and availability, unattended slots automatically reset after the allocated time, ensuring efficient utilization.


3. Admin Panel

Book and Slot Log Details
Comprehensive Log: Provides administrators with a detailed log of all book issuances, returns, and discussion room slot statuses, enabling them to track user activities and system utilization effectively.

Administrative Oversight: Equips administrators with insights into user behaviors, book availability, and discussion room usage, facilitating informed decision-making and resource management.

Data Insertion
Database Management: Allows administrators to insert new details into relevant tables, ensuring the database remains up-to-date and reflective of current information.

Data Integrity: Maintains data accuracy and completeness within the system, crucial for providing users with the most accurate and relevant information.

Slot Management
Slot Status View: Offers administrators a comprehensive view of discussion room slot statuses, detailing which slots are issued and which are available.

Manual Unissue: Provides the ability to manually unissue slots if necessary, offering administrators control over the availability and allocation of discussion room spaces.

Each functionality caters to specific user needs while empowering administrators with tools for effective system management, data integrity, and informed decision-making. Together, these features contribute to an efficient, user-friendly, and well-managed system environment.