from random import randint

from faker import Faker
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Post


def users(count=100):
    faker = Faker()

    while count > 0:
        user = User(
            name = faker.user_name(),
            email = faker.email(),
            password='10000',
            confirmed= True,
            location= faker.city(),
            about_me= faker.text(),
            member_since= faker.past_date(),
        )
        db.session.add(user)
        try:
            db.session.commit()
            count-=1
        except IntegrityError:
            db.session.rollback()

def posts(count=100):
    faker = Faker()
    user_count = User.query.count()
    
    while count > 0:
        user = User.query.offset(randint(0,user_count-1)).first()
        post = Post(
            body = faker.text(),
            timestamp = faker.past_date(),
            author = user
        )
        db.session.add(post)
        try:
            db.session.commit()
            count-=1
        except IntegrityError:
            db.session.rollback()
