from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and sessions

# Database connection with hardcoded credentials
def get_db_connection():
    return mysql.connector.connect(
        host="moviebooking.c38664csc4vd.ap-south-1.rds.amazonaws.com",  # RDS endpoint
        user="root",  # Master username for RDS
        password="8111arnavavni",  # Master password for RDS
        database="moviebooking"  # Name of the database created in RDS
    )

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Verify the password
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect('/movies')  # Redirect to movies page after login
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('No account found with that email. Please sign up.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('Email already exists. Please login.', 'error')
            return redirect('/signup')

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Account created successfully! Please login.', 'success')
        return redirect('/login')

    return render_template('signup.html')

@app.route('/movies')
def movies():
    if 'user_id' not in session:
        flash('User login is required to browse movies.', 'error')
        return redirect('/login')

    return render_template('movies.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You need to log in to view your profile.', 'error')
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, email FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile.html', username=user['username'], email=user['email'])

@app.route('/booking/<int:movie_id>')
def booking(movie_id):
    if 'user_id' not in session:
        flash('You must be logged in to book tickets.', 'error')
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, genre, showtime FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    conn.close()

    if not movie:
        flash('Movie not found.', 'error')
        return redirect('/movies')

    return render_template('booking.html', movie_name=movie['name'], movie_description=movie['genre'], movie_id=movie['id'])

@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        flash('You must be logged in to book tickets.', 'error')
        return redirect('/login')

    movie_id = request.form['movie_id']
    booking_date = request.form['date']
    booking_time = request.form['time']
    tickets = request.form['tickets']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bookings (user_id, movie_id, booking_date, booking_time, tickets) VALUES (%s, %s, %s, %s, %s)",
        (session['user_id'], movie_id, booking_date, booking_time, tickets)
    )
    conn.commit()

    booking_id = cursor.lastrowid
    cursor.close()
    conn.close()

    flash('Your tickets have been booked successfully!', 'success')
    return redirect(url_for('confirmation', booking_id=booking_id))

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    if 'user_id' not in session:
        flash('You must be logged in to view the booking confirmation.', 'error')
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, m.name AS movie_name, b.booking_date, b.booking_time, b.tickets
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
        WHERE b.id = %s AND b.user_id = %s
    """, (booking_id, session['user_id']))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()

    if not booking:
        flash('Booking not found.', 'error')
        return redirect('/movies')

    return render_template('booking_confirmation.html', booking=booking)

@app.route('/view_bookings', methods=['GET'])
def view_bookings():
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to view your bookings.", "error")
        return redirect('/login')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT b.id, m.name AS movie_name, b.booking_date, b.booking_time, 
           b.tickets, b.status
    FROM bookings b
    JOIN movies m ON b.movie_id = m.id
    WHERE b.user_id = %s
    ORDER BY b.booking_date DESC, b.booking_time DESC
    """
    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
