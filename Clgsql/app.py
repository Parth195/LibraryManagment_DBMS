# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
#from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from datetime import datetime
import bcrypt


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

salt = bcrypt.gensalt(rounds=15)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Parth@27',
    'database': 'knowledge_hub',
}

def execute_query(query, params=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        result = None  # Check if this part is being executed and why

    finally:
        cursor.close()
        connection.close()

    return result

def execute_procedure(proc_name, args):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.callproc(proc_name, args)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']  # 'admin' or 'regular'
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        print("Hashed Password:", hashed_password)  # Debug: Print the hashed password
        
        query = "INSERT INTO users (name, email, password, account_type) VALUES (%s, %s, %s, %s)"
        result = execute_query(query, (name, email, hashed_password, account_type))
        print("Query Result:", result)  # Debug: Print the result of the query
        
        return redirect(url_for('login'))
    return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT * FROM users WHERE email = %s"
        user = execute_query(query, (email,))
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')):
            session['logged_in'] = True
            session['user_id'] = user[0]['id']
            session['account_type'] = user[0]['account_type']
            session['user_name'] = user[0]['name']
            
            if session['account_type'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Account not found or invalid credentials")
            
    return render_template('login.html')





@app.route('/logout', methods=['GET', 'POST'])  # Allow both GET and POST requests
def logout():
    if request.method == 'POST':
        # Clear the session data
        session.clear()
        return redirect(url_for('index'))
    else:
        # Handle cases where method is not POST (optional)
        session.clear()
	
        return redirect(url_for('index'))


@app.route('/admin')
def admin():
    query1 = """
        SELECT books.*, GROUP_CONCAT(genre.genre SEPARATOR ', ') AS genres
        FROM books
        LEFT JOIN genre ON books.BOOK_ID = genre.BOOK_ID
        GROUP BY books.BOOK_ID LIMIT 5
    """
    books = execute_query(query1)
    return render_template('admin.html',books=books)


@app.route('/insert_details', methods=['GET', 'POST'])
def insert_details():
    if request.method == 'POST':
        # Retrieve form data for each table
        book_id = request.form['book_id']
        book_name = request.form['book_name']
        author = request.form['author']
        subject = request.form['subject']
        e_book = request.form['e_book']
        location = request.form['location']
        total_books = request.form['total_books']
        books_available = request.form['books_available']
        genre = request.form['genre']
        college_id = request.form['college_id']
        college_name = request.form['college_name']
        country = request.form['country']
        min_cgpa = request.form['min_cgpa']
        degree = request.form['degree']
        stream = request.form['stream']
        exam_type = request.form['exam_type']

        # Insert data into respective tables using procedures
        execute_procedure('insert_into_books', (book_id, book_name, author, subject, e_book, location, total_books, books_available))
        execute_procedure('insert_into_genre', (book_id, genre))
        execute_procedure('insert_into_colleges', (college_id, college_name, country, min_cgpa))
        execute_procedure('insert_into_exam', (college_id, degree, stream, exam_type))

        flash('Data inserted successfully!')
        return redirect(url_for('insert_details'))

    return render_template('insert_details.html')


@app.route('/')
def index():
    query = """
        SELECT books.*, GROUP_CONCAT(genre.genre SEPARATOR ', ') AS genres
        FROM books
        LEFT JOIN genre ON books.BOOK_ID = genre.BOOK_ID
        GROUP BY books.BOOK_ID LIMIT 5
    """
    books = execute_query(query)
    return render_template('index.html', books=books)

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')



@app.route('/search-results', methods=['POST'])
def search_results():
    criteria = []
    conditions = []
    values = []

    # Fetching data from form fields
    book_id = request.form.get('book_id')
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    subject = request.form.get('subject')
    e_book = request.form.get('e_book')
    location = request.form.get('location')
    genre = request.form.get('genre')

    # Checking each criterion and building the SQL query dynamically
    if book_id:
        criteria.append('BOOK_ID = %s')
        values.append(book_id)
    
    if book_name:
        criteria.append('BOOK_NAME LIKE %s')
        values.append('%' + book_name + '%')

    if author:
        criteria.append('AUTHOR LIKE %s')
        values.append('%' + author + '%')
   
    if subject:
        criteria.append('SUBJECT LIKE %s')
        values.append('%' + subject + '%')	

    if e_book:
        criteria.append('E_BOOK LIKE %s')
        values.append('%' + e_book + '%')	
    
    if location:
        criteria.append('LOCATION LIKE %s')
        values.append('%' + location + '%')

    # Constructing the SQL query
    if criteria:
        conditions.append(' AND '.join(criteria))

    if genre:
        if 'GENRE' in criteria:
            criteria.remove('GENRE')  # Remove 'GENRE' if already present
        query = """
            SELECT b.BOOK_ID, b.BOOK_NAME, b.AUTHOR, b.SUBJECT, b.e_book, b.LOCATION, b.TOTAL_NO_OF_BOOKS, b.BOOKS_AVAILABLE_TO_ISSUE, GROUP_CONCAT(g.genre SEPARATOR ', ') AS genre
            FROM books b
            LEFT JOIN genre g ON b.BOOK_ID = g.BOOK_ID
            WHERE g.genre LIKE %s
            GROUP BY b.BOOK_ID
        """
        result = execute_query(query, ('%' + genre + '%',))
        return render_template('search_results.html', result=result)

    # If 'genre' not specified, continue with the regular query
    query = "SELECT * FROM books"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    result = execute_query(query, tuple(values))

    return render_template('search_results.html', result=result)




@app.route('/issue-book', methods=['POST'])
def issue_book():
    book_id = request.form['book_id']
    roll_number = request.form['roll_number']

    # Check if the book exists
    check_book_query = "SELECT * FROM books WHERE BOOK_ID = %s"
    book = execute_query(check_book_query, (book_id,))

    if not book:
        return "Book not found. Please enter a valid Book ID."

    # Issue the book
    update_issue_query = """
        UPDATE books
        SET BOOKS_AVAILABLE_TO_ISSUE = BOOKS_AVAILABLE_TO_ISSUE - 1
        WHERE BOOK_ID = %s
    """
    execute_query(update_issue_query, (book_id,))

    # Add the issuance record
    add_issue_record_query = """
        INSERT INTO issue (BOOK_ID2, ISSUED_BY)
        VALUES (%s, %s)
    """
    execute_query(add_issue_record_query, (book_id, roll_number))

    return f"Issued Book {book_id} to {roll_number} successfully."


@app.route('/return-book', methods=['POST'])
def return_book():
    book_id = request.form['book_id']
    roll_number = request.form['roll_number']

    # Check if the book is issued
    check_issue_query = "SELECT * FROM issue WHERE BOOK_ID2 = %s AND ISSUED_BY = %s"
    issued_books = execute_query(check_issue_query, (book_id, roll_number))

    if not issued_books:
        return "No books to return or invalid return details."

    # Return the book
    update_return_query = """
        UPDATE books
        SET BOOKS_AVAILABLE_TO_ISSUE = BOOKS_AVAILABLE_TO_ISSUE + 1
        WHERE BOOK_ID = %s
    """
    execute_query(update_return_query, (book_id,))

    # Remove the issuance record
    remove_issue_record_query = "DELETE FROM issue WHERE BOOK_ID2 = %s AND ISSUED_BY = %s"
    execute_query(remove_issue_record_query, (book_id, roll_number))

    return f"Returned Book {book_id} from {roll_number} successfully."



@app.route('/college-search', methods=['GET'])
def college_search():
    criteria = request.args.get('criteria')  # Fetch the criteria from URL args
    desired_cgpa = request.args.get('desired_cgpa')  # Fetch the desired CGPA from URL args

    # Other logic to handle the page

    return render_template('college_search.html', criteria=criteria, desired_cgpa=desired_cgpa)


@app.route('/college-search-results', methods=['POST'])
def college_search_results():
    criteria = request.form['criteria']
    keyword = request.form['keyword']

    if criteria in ['STREAM', 'DEGREE', 'EXAMS']:
        query = """
            SELECT DISTINCT c.COLLEGE_ID, c.COLLEGE_NAME, c.COUNTRY, c.MIN_CGPA_REQUIRED
            FROM colleges c
            JOIN exam e ON c.COLLEGE_ID = e.COLLEGE_ID
            WHERE e.EXAMS = %s
        """
        result = execute_query(query, (keyword,))
    elif criteria == 'MIN_CGPA_REQUIRED':
        # Treat keyword as a float for CGPA comparison
        keyword = float(keyword)
        query = "SELECT * FROM colleges WHERE MIN_CGPA_REQUIRED <= %s"
        result = execute_query(query, (keyword,))
    else:
        query = f"SELECT * FROM colleges WHERE {criteria} LIKE %s"
        result = execute_query(query, ('%' + keyword + '%',))

    if result is None:
        result = []

    return render_template('college_search_results.html', result=result, criteria=criteria, keyword=keyword)



@app.route('/college-details/<int:college_id>', methods=['GET'])
def college_details(college_id):
    college_query = "SELECT * FROM colleges WHERE COLLEGE_ID = %s"
    college = execute_query(college_query, (college_id,))

    if not college:
        return "College not found."

    exam_query = "SELECT * FROM EXAM WHERE COLLEGE_ID = %s"
    exams = execute_query(exam_query, (college_id,))

    return render_template('college_details.html', college=college[0], exams=exams)


@app.route('/display-log-details')
def display_log_details():
    query = "SELECT * FROM log_details"
    log_data = execute_query(query)  # Assuming execute_query method exists to execute SQL queries
    return render_template('log_details.html', log_data=log_data)


@app.route('/log-details', methods=['GET', 'POST'])
def log_details():
    search_issued_by = None
    if request.method == 'POST':
        search_issued_by = request.form['search_issued_by']

    if search_issued_by:
        query = "SELECT * FROM log_details WHERE issued_by LIKE %s"
        log_data = execute_query(query, ('%' + search_issued_by + '%',))
    else:
        query = "SELECT * FROM log_details"
        log_data = execute_query(query)

    return render_template('log_details.html', log_data=log_data)



@app.route('/display-slots-details')
def display_slot_details():
    query = "SELECT * FROM slot"
    log_data = execute_query(query)
    return render_template('slots.html', log_data=log_data)

@app.route('/slot-details', methods=['GET', 'POST'])
def slot_details():
    search_slot_id = None
    if request.method == 'POST':
        search_slot_id = request.form['search_slot_id']

    if search_slot_id:
        query = "SELECT * FROM slot WHERE SLOT_ID = %s"
        log_data = execute_query(query, (search_slot_id,))
    else:
        query = "SELECT * FROM slot"
        log_data = execute_query(query)

    return render_template('slots.html', log_data=log_data)

@app.route('/unissued-slots')
def unissued_slots():
    query = "SELECT * FROM slot WHERE ISSUED_BY IS NULL"
    unissued_slots_data = execute_query(query)  # Fetch unissued slots data
    
    # Pass fetched data to the 'unissued_slots.html' template using the correct variable name
    return render_template('unissued_slots.html', unissued_slots_data=unissued_slots_data)

@app.route('/issue-slot/<slot_id>', methods=['GET', 'POST'])
def issue_slot(slot_id):
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        query = "UPDATE slot SET ISSUED_BY = %s, log_time = NOW() WHERE SLOT_ID = %s"
        execute_query(query, (roll_number, slot_id))
        return "Slot issued successfully!"  # You can redirect or display a success message

    return render_template('issue_slot.html', slot_id=slot_id)



@app.route('/get-books-by-stream', methods=['POST'])
def get_books_by_stream():
    stream = request.form.get('stream')  # Check the selected value from the form

    if stream:
        # Fetch books based on the selected stream
        query = "SELECT * FROM books WHERE Subject LIKE %s;"
        books = execute_query(query, (f'%{stream}%',))

        # Pass the books data to a new HTML page for display
        return render_template('get_books_by_stream.html', books=books, stream=stream)
    else:
        # Handle the case when no stream is selected
        return "No stream selected"

@app.route('/unissue-slot/<string:slot_id>', methods=['POST'])
def unissue_slot(slot_id):
    # Perform an update query to set ISSUED_BY and LOG_TIME to NULL for the specified slot_id
    update_query = "UPDATE slot SET ISSUED_BY = NULL, LOG_TIME = NULL WHERE SLOT_ID = %s"
    # Pass the slot_id as a parameter to prevent SQL injection
    execute_query(update_query, (slot_id,))  # Execute the update query
    
    # Redirect back to the slot_details page after unissuing the room
    return redirect(url_for('slot_details'))


@app.route('/calculate-required-cgpa', methods=['GET', 'POST'])
def calculate_required_cgpa():
    if request.method == 'POST':
        rollno = request.form['rollno']
        current_cgpa = float(request.form['current_cgpa'])
        completed_semesters = int(request.form['completed_semesters'])
        desired_cgpa = float(request.form['desired_cgpa'])
        completed_credits = int(request.form['completed_credits'])
        credits_left = int(request.form['credits_left'])

        # Execute the query with the stored function
        query = "SELECT CalculateRequiredCGPA(%s, %s, %s, %s, %s) AS required_cgpa"
        result = execute_query(query, (current_cgpa, completed_semesters, desired_cgpa, completed_credits, credits_left))

        # Fetch the result of the stored function
        required_cgpa = result[0]['required_cgpa']

        # Render the template with input values and calculated output
        return render_template('required_cgpa_result.html',
                               rollno=rollno,
                               current_cgpa=current_cgpa,
                               completed_semesters=completed_semesters,
                               desired_cgpa=desired_cgpa,
                               completed_credits=completed_credits,
                               credits_left=credits_left,
                               required_cgpa=required_cgpa)

    # Return the form template for the initial load
    return render_template('required_cgpa_result.html')




if __name__ == '__main__':
    app.run(debug=True)
