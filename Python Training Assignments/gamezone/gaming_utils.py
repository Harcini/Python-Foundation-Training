import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Harcini@1810",
            database="gamingzone"
        )
    except mysql.connector.Error as err:
        print("❌ Error connecting to database:", err)
        return None

# ✅ Game Operations
def add_game():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    name = input("Enter game name: ")
    gtype = input("Enter game type: ")
    charge = float(input("Enter charge per hour: "))
    cursor.execute("INSERT INTO games (GameName, GameType, ChargePerHour) VALUES (%s, %s, %s)", (name, gtype, charge))
    db.commit()
    print("✅ Game added successfully.")
    db.close()

def view_games():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("SELECT * FROM games")
    for row in cursor.fetchall():
        print(row)
    db.close()

def games_above_100():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("SELECT GameName, ChargePerHour FROM games WHERE ChargePerHour > 100")
    for row in cursor.fetchall():
        print(row)
    db.close()

def count_games_by_type():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("SELECT GameType, COUNT(*) FROM games GROUP BY GameType")
    for row in cursor.fetchall():
        print(row)
    db.close()

# ✅ Member Operations
def register_member():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    name = input("Enter member name: ")
    mtype = input("Enter membership type (yearly/monthly/daily): ").lower()
    cursor.execute("SELECT MembershipID FROM memberships WHERE MembershipType = %s", (mtype,))
    result = cursor.fetchone()
    if result:
        cursor.execute("INSERT INTO members (MemberName, MembershipID, HoursSpent) VALUES (%s, %s, %s)", (name, result[0], 0))
        db.commit()
        print("✅ Member registered successfully.")
    else:
        print("❌ Membership type not found.")
    db.close()

def view_members():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members")
    for row in cursor.fetchall():
        print(row)
    db.close()

def delete_member_if_not_played():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    name = input("Enter member name to delete: ")
    cursor.execute("SELECT MemberID FROM members WHERE MemberName = %s", (name,))
    member = cursor.fetchone()
    if not member:
        print("❌ Member not found.")
        return
    member_id = member[0]
    cursor.execute("SELECT * FROM play_logs WHERE member_id = %s", (member_id,))
    if cursor.fetchone() is None:
        cursor.execute("DELETE FROM members WHERE MemberID = %s", (member_id,))
        db.commit()
        print("✅ Member deleted (no gameplay recorded).")
    else:
        print("❌ Cannot delete. Member has gameplay records.")
    db.close()

# ✅ Gameplay Operations
def log_gameplay():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    mname = input("Enter member name: ")
    gname = input("Enter game name: ")
    hours = int(input("Enter hours to log: "))

    cursor.execute("SELECT MemberID, MembershipID, HoursSpent FROM members WHERE MemberName = %s", (mname,))
    member = cursor.fetchone()
    if not member:
        print("❌ Member not found.")
        return
    member_id, membership_id, spent = member

    cursor.execute("SELECT TotalHours FROM memberships WHERE MembershipID = %s", (membership_id,))
    allowed = cursor.fetchone()[0]

    if spent + hours > allowed:
        print("❌ Not enough hours left.")
        return

    cursor.execute("SELECT GameID FROM games WHERE GameName = %s", (gname,))
    game = cursor.fetchone()
    if not game:
        print("❌ Game not found.")
        return
    game_id = game[0]

    cursor.execute("INSERT INTO play_logs (member_id, game_id, hours_played) VALUES (%s, %s, %s)", (member_id, game_id, hours))
    cursor.execute("UPDATE members SET HoursSpent = HoursSpent + %s WHERE MemberID = %s", (hours, member_id))
    db.commit()
    print("✅ Gameplay logged successfully.")
    db.close()
def most_active_member():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT MemberName, HoursSpent
        FROM members
        ORDER BY HoursSpent DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    if result:
        print(f"Most active member: {result[0]} with {result[1]} hours")
    else:
        print("No members found.")
    db.close()
def members_never_played():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.MemberName
        FROM members m
        LEFT JOIN play_logs p ON m.MemberID = p.member_id
        WHERE p.id IS NULL
    """)
    results = cursor.fetchall()
    if results:
        print("Members who never played any game:")
        for row in results:
            print(row[0])
    else:
        print("✅ All members have gameplay records.")
    db.close()
def full_member_report():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            m.MemberName,
            ms.MembershipType,
            COUNT(DISTINCT p.game_id) AS GamesPlayed,
            IFNULL(SUM(p.hours_played), 0) AS TotalHoursPlayed,
            (ms.TotalHours - m.HoursSpent) AS HoursLeft
        FROM members m
        JOIN memberships ms ON m.MembershipID = ms.MembershipID
        LEFT JOIN play_logs p ON m.MemberID = p.member_id
        GROUP BY m.MemberID, m.MemberName, ms.MembershipType, ms.TotalHours, m.HoursSpent
    """)
    results = cursor.fetchall()
    if results:
        print("\nFull Member Report:")
        print("Name | Type | Games Played | Total Hours | Hours Left")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    else:
        print("No member data found.")
    db.close()
def members_over_75_percent():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            m.MemberName,
            ROUND((m.HoursSpent / ms.TotalHours) * 100, 2) AS UsagePercentage
        FROM members m
        JOIN memberships ms ON m.MembershipID = ms.MembershipID
        WHERE (m.HoursSpent / ms.TotalHours) >= 0.75
    """)
    results = cursor.fetchall()
    if results:
        print("\nMembers who used more than 75% of allowed hours:")
        for row in results:
            print(f"{row[0]} - {row[1]}% used")
    else:
        print("✅ No members have used more than 75% of their hours.")
    db.close()
def report_member_gameplay():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            m.MemberName,
            g.GameName,
            SUM(p.hours_played) AS TotalHours
        FROM play_logs p
        JOIN members m ON p.member_id = m.MemberID
        JOIN games g ON p.game_id = g.GameID
        GROUP BY m.MemberID, g.GameID
        ORDER BY m.MemberName, g.GameName
    """)
    results = cursor.fetchall()
    if results:
        print("\nTotal Hours Played Per Member Per Game:")
        print("Member | Game | Hours")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    else:
        print("No gameplay records found.")
    db.close()
def top_3_games():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.GameName, SUM(p.hours_played) AS TotalHours
        FROM play_logs p
        JOIN games g ON p.game_id = g.GameID
        GROUP BY g.GameID
        ORDER BY TotalHours DESC
        LIMIT 3
    """)
    results = cursor.fetchall()
    if results:
        print("\nTop 3 Most Played Games (by hours):")
        for row in results:
            print(f"{row[0]} - {row[1]} hours")
    else:
        print("No gameplay data found.")
    db.close()
def total_income():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(p.hours_played * g.ChargePerHour)
        FROM play_logs p
        JOIN games g ON p.game_id = g.GameID
    """)
    result = cursor.fetchone()
    total = result[0] if result and result[0] else 0
    print(f"\n💰 Total Income from Gameplay: ₹{total:.2f}")
    db.close()
def total_hours_remaining_by_type():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            ms.MembershipType,
            SUM(ms.TotalHours - m.HoursSpent) AS HoursLeft
        FROM members m
        JOIN memberships ms ON m.MembershipID = ms.MembershipID
        GROUP BY ms.MembershipType
    """)
    results = cursor.fetchall()
    if results:
        print("\nTotal Hours Remaining by Membership Type:")
        for row in results:
            print(f"{row[0]}: {row[1]} hours left")
    else:
        print("No members found.")
    db.close()
def members_played_more_than_two_games():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.MemberName, COUNT(DISTINCT p.game_id) AS games_played
        FROM play_logs p
        JOIN members m ON p.member_id = m.MemberID
        GROUP BY m.MemberID
        HAVING games_played > 2
    """)
    results = cursor.fetchall()
    if results:
        print("\nMembers who played more than 2 different games:")
        for row in results:
            print(f"{row[0]} - {row[1]} games")
    else:
        print("✅ No member has played more than 2 different games.")
    db.close()
def members_below_10_hours():
    db = connect_db()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.MemberName, (ms.TotalHours - m.HoursSpent) AS HoursLeft
        FROM members m
        JOIN memberships ms ON m.MembershipID = ms.MembershipID
        WHERE (ms.TotalHours - m.HoursSpent) < 10
    """)
    results = cursor.fetchall()
    if results:
        print("\nMembers with less than 10 hours remaining:")
        for row in results:
            print(f"{row[0]} - {row[1]} hours left")
    else:
        print("✅ All members have at least 10 hours left.")
    db.close()
def delete_member_if_not_played():
    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    name = input("Enter member name to delete: ")

    # Step 1: Read all members with that name
    cursor.execute("SELECT MemberID, MemberName FROM members WHERE MemberName = %s", (name,))
    all_matches = cursor.fetchall()

    if not all_matches:
        print("❌ Member not found.")
        db.close()
        return

    # Step 2: If multiple members with same name, show them
    if len(all_matches) > 1:
        print(f"⚠ Multiple members named '{name}' found:")
        for row in all_matches:
            print(f"- MemberID: {row[0]} | Name: {row[1]}")
        selected_id = input("Enter the MemberID you want to delete: ")
        member_id = int(selected_id)
    else:
        member_id = all_matches[0][0]

    # ✅ Step 3: Check for gameplay
    cursor.execute("SELECT * FROM gameplay WHERE MemberID = %s", (member_id,))
    _ = cursor.fetchall()  # ✅ this clears unread result
    if not _:
        cursor.execute("DELETE FROM members WHERE MemberID = %s", (member_id,))
        db.commit()
        print("✅ Member deleted (no gameplay recorded).")
    else:
        print("❌ Cannot delete. Member has gameplay records.")

    db.close()


    

  



