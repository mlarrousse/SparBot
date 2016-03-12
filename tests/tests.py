from lib import db
def test_registration():
    username = 'mary'
    registered = db.user_is_registered(username)
    if not registered:
        db.register_user(username)
    print(db.user_is_registered(username))
    conn.commit()
    conn.close()