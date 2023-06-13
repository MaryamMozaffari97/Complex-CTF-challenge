from flask.cli import FlaskGroup

from core import User, app, db

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    user1 = User(username='john_doe', password='password1')
    user2 = User(username='jane_smith', password='password2')
    user3 = User(username='bob_johnson', password='password3')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

if __name__ == "__main__":
    cli()