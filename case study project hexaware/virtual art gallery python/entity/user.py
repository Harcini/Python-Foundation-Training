class User:
    def __init__(self, user_id, username, password, email, first_name, last_name, dob, profile_pic):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.profile_pic = profile_pic

def insert_user(user):
    from db_connect import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO User (Username, Password, Email, FirstName, LastName, DateOfBirth, ProfilePicture)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        user.username, user.password, user.email, user.first_name,
        user.last_name, user.dob, user.profile_pic
    )
    cursor.execute(sql, values)
    conn.commit()
    print("User inserted successfully!")
    cursor.close()
    conn.close()

def view_all_users():
    from db_connect import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    rows = cursor.fetchall()
    print("\n--- All Users ---")
    if not rows:
        print("No users found.")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[3]}, Name: {row[4]} {row[5]}")
    cursor.close()
    conn.close()
