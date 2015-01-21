# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, default='', nullable=True)
    email = db.Column(db.String(80), unique=False, default='', nullable=True)
    role_id = db.Column(db.Integer)

    def __init__(self, username, email, role_id):
        self.username = username
        self.email = email
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, default='', nullable=True)
    desc = db.Column(db.String(80), unique=False, default='', nullable=True)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<Role %r>' % self.name


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('email', 'username')


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('name', 'desc')


@app.route("/")
def hello():
    # new_role = Role(name='administration', desc='It is administration.')
    # db.session.add(new_role)
    # db.session.commit()

    new_user = User(username='fuboqing', email='fuboqing@live.cn', role_id=1)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(result={})


@app.route('/api/users/')
def users():
    all_users = User.query.with_entities(User.email.label('id'), User.username).all()
    users_schema = UserSchema(many=True, only=('id',))
    result = users_schema.dump(all_users)
    return jsonify(result=result)


@app.route('/api/users/<id>')
def user_detail(id):
    user = User.query.filter_by(id=id).first()
    user_schema = UserSchema()
    result = user_schema.dump(user)
    return jsonify(result=result.data)


@app.route('/join')
def join():
    res = db.session.query(User.username.label('name'), User.email, Role.name.label('role'))\
        .outerjoin(Role, Role.id == User.role_id).all()
    res_schema = UserSchema(many=True, only=('name', 'email', 'role'))
    result = res_schema.dump(res)
    return jsonify(result=result.data)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)