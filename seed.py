from sqlalchemy import func
from model import connect_to_db, db, PollingCenter, Comment, User, Parties, PollingHour
from server import app

def load_parties():
    """Load parties from v.parties into database"""

    print("Votings")

    for i, row in enumerate(open("seed_data/v.parties")):
        row = row.rstrip()
        party_id, political_party, political_party_abbr = row.split("|")

        parties = Parties(party_id=party_id, political_party=political_party, political_party_abbr=political_party_abbr)

        # We need to add to the session or it won't ever be stored
        db.session.add(parties)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)
    
    # Once seeding is done, should commit our work
    db.session.commit()

def load_polling_hours():
    """Load polling center hours into database"""

    for i, row in enumerate(open("seed_data/v.hours")):
        row = row.strip()
        state_id, state_name, state_abbrev, state_hours = row.split("|")

        hours = PollingHour(state_id=state_id, state_name=state_name, state_abbrev=state_abbrev, state_hours=state_hours)

        db.session.add(hours)

        if i % 100 == 0:
            print(i)

    db.session.commit()

def set_val_user_id():
    """Sets the value for next user in database"""

    # Get the value for the next user_id to be max_id +1
    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id +1
    query = "SELECT setval('users_user_id_seq', max(id) FROM users"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_polling_hours()
    load_parties()
    set_val_user_id()
