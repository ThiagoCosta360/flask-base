from flask.cli import FlaskGroup
from src import app, db, User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("populate_db")
def populate_db():
    db.session.add(User(email="t.afonso@sidi.org.br"))
    db.session.commit()

if __name__ == "__main__":
    cli()
    
    # run_server.py 