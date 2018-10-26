import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine))
db = session()

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",
            {'isbn': isbn, 'title': title, 'author': author, 'year': year})
        print(f"{isbn} {title} {author} {year}")
    db.commit()
    
    print('Insertions into database completed')

if __name__ == "__main__":
    main()