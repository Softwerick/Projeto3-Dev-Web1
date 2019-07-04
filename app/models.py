from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Like(db.Model):
    __tablename__ = 'likes'
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                         primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('produtos.id'),
                           primary_key=True)


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    preco = db.Column(db.Integer)
    peso = db.Column(db.Integer)
    estoque = db.Column(db.Integer)
    liked = db.relationship(
        'Like', foreign_keys=[Like.product_id],
        backref=db.backref('liker', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=False, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    liker = db.relationship(
        'Like', foreign_keys=[Like.liker_id],
        backref=db.backref('liked', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_liking(self, produto):
        return self.liker.filter_by(
            product_id=produto.id
        ).first() is not None

    def fav(self, produto):
        if not self.is_liking(produto):
            lhi = Like(liker_id=self.id, product_id=produto.id)
            db.session.add(lhi)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
