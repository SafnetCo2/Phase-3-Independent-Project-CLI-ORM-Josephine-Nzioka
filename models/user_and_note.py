import click
from sqlalchemy import create_engine, DateTime, ForeignKey, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

#  Base class declarative used for ORM classes
Base = declarative_base()
#user file
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default="Regular")

    notes = relationship("Note", back_populates="user")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, email={self.email}, role={self.role})"

    @classmethod
    def create(cls, session, username, email, role="Regular"):
        user = cls(username=username, email=email, role=role)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, user_id):
        user = session.query(cls).filter_by(user_id=user_id).first()
        if user:
            session.delete(user)
            session.commit()

    @classmethod
    def update(cls, session, user_id, **kwargs):
        user = session.query(cls).filter_by(user_id=user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
            return user
        return None

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).first()
#note class file
class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000))
    created_at = Column(DateTime, default=func.now())
    last_modified_at = Column(DateTime, onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"Note(note_id={self.note_id}, title={self.title}, content={self.content}, created_at={self.created_at})"

    @classmethod
    def create(cls, session, title, content, user_id):
        note = cls(title=title, content=content, user_id=user_id)
        session.add(note)
        session.commit()
        return note

    @classmethod
    def delete(cls, session, note_id):
        note = session.query(cls).filter_by(note_id=note_id).first()
        if note:
            session.delete(note)
            session.commit()

    @classmethod
    def update(cls, session, note_id, **kwargs):
        note = session.query(cls).filter_by(note_id=note_id).first()
        if note:
            for key, value in kwargs.items():
                setattr(note, key, value)
            session.commit()
            return note
        return None

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, note_id):
        return session.query(cls).filter_by(note_id=note_id).first()

    @classmethod
    def search(cls, session, keyword):
        return session.query(cls).filter(cls.title.like(f'%{keyword}%') | cls.content.like(f'%{keyword}%')).all()

#command line interface applications CLI for user and note
@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Username', help='User username')
@click.option('--email', prompt='Email', help='User email')
@click.option('--role', default='Regular', help='User role')
def create_user(username, email, role):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    User.create(session, username, email, role)
    click.echo('The user has been created.')
    session.close()

@cli.command()
def list_users():
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    users = User.get_all(session)
    for user in users:
        click.echo(user)

@cli.command()
@click.option('--user_id', prompt='User ID', help='User ID to delete')
def delete_user(user_id):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    User.delete(session, int(user_id))
    click.echo(f'The user with ID {user_id} has been deleted.')

@cli.command()
@click.option('--title', prompt='Title', help='Note title')
@click.option('--content', prompt='Content', help='Note content')
@click.option('--user_id', prompt='User ID', help='User ID associated with the note')
def create_note(title, content, user_id):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Note.create(session, title, content, int(user_id))
    click.echo('The note has been created.')
#cli for note


@cli.command()
@click.option('--note_id', prompt='Note ID', help='Note ID to delete')
def delete_note(note_id):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Note.delete(session, int(note_id))
    click.echo(f'The note with ID {note_id} has been deleted.')


@cli.command()
@click.option('--user_id', prompt='User ID', help='User ID to update')
@click.option('--username', prompt='New Username', help='New username')
@click.option('--email', prompt='New Email', help='New email')
@click.option('--role', prompt='New Role', help='New role')
def update_user(user_id, username, email, role):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = User.update(session, int(user_id), username=username, email=email, role=role)
    if user:
        click.echo(f'The user with ID {user_id} has been updated.')
    else:
        click.echo(f'User with ID {user_id} not found.')
#note CLI commands
@cli.command()
@click.option('--note_id', prompt='Note ID', help='Note ID to update')
@click.option('--title', prompt='New Title', help='New title')
@click.option('--content', prompt='New Content', help='New content')
def update_note(note_id, title, content):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    note = Note.update(session, int(note_id), title=title, content=content)
    if note:
        click.echo(f'The note with ID {note_id} has been updated.')
    else:
        click.echo(f'Note with ID {note_id} not found.')

@cli.command()
@click.option('--keyword', prompt='Keyword', help='Search keyword')
def search_notes(keyword):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    notes = Note.search(session, keyword)
    if notes:
        for note in notes:
            click.echo(note)
    else:
        click.echo('No notes found matching the search criteria.')

@cli.command()
@click.option('--user_id', prompt='User ID', help='User ID to list notes')
def list_notes_by_user(user_id):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = User.find_by_id(session, int(user_id))
    if user:
        click.echo(f'Notes for user: {user.username}')
        for note in user.notes:
            click.echo(note)
    else:
        click.echo(f'User with ID {user_id} not found.')

@cli.command()
@click.option('--date', prompt='Date (YYYY-MM-DD)', help='Date to list notes')
def list_notes_by_date(date):
    engine = create_engine('sqlite:///mydb.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    notes = session.query(Note).filter(func.date(Note.created_at) == date).all()
    if notes:
        click.echo(f'Notes created on {date}:')
        for note in notes:
            click.echo(note)
    else:
        click.echo(f'No notes found created on {date}.')
# Define a main function to run the CLI in a loop until the user exits
def main():
    while True:
        cli()
        choice = click.prompt('Do you want to continue? (yes/no)', type=str)
        if choice.lower() != 'yes':
            click.echo('Exiting...')
            break

if __name__ == '__main__':
    
    cli()