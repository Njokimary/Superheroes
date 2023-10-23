#!/usr/bin/env python3

from flask import Flask, make_response,request,jsonify
from flask_migrate import Migrate
from flask_restful import Api,Resource

from models import db, Hero,HeroPower,Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


api = Api(app)


@app.route('/')
def home():
    return ''

class Heroes(Resource):
    def get(self):
        heroes =Hero.query.all()
        heroes_list = []
        for hero in heroes:
            hero_dict ={
                "id": hero.id,
                "name": hero.name,
                "super_name":hero.super_name
            }
            heroes_list.append(hero_dict)
        return make_response(jsonify(heroes_list),200)
    
api.add_resource(Heroes,"/heroes")

class HeroById(Resource):
    def get(self,id):
        hero=Hero.query.get(id)
        if hero is not None:
            return make_response({
                "error": "Hero not found"
            },404)
        
api.add_resource(HeroById, "/heroes/<int:id>")

class Powers(Resource):
    def get(self):
        powers=Power.query.all()
        powers_list=[]
        for power in powers:
            power_dict={
                "id": power.id,
                "name":power.name,
                "description": power.description 
            }
            powers_list.append(power_dict)
        return make_response(jsonify(powers_list), 200)
    
api.add_resource(Powers, "/powers")


class PowerById(Resource):
    def get(self, id):
        power=Power.query.get(id)
        if not power:
            return make_response({
  "error": "Power not found"
}, 404)
      

        power_dict={
                "id": power.id,
                "name":power.name,
                "description": power.description 
        }

        return make_response(jsonify(power_dict), 200)

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return make_response({
                "error": "Power not found"
            }, 404)
        
        data = request.get_json()
        power.description = data.get("description")
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response({
                "errors": [str(e)]
            }, 400)
        
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        
        return make_response(jsonify(power_dict), 200)
    

api.add_resource(PowerById, "/powers/<int:id>")




if __name__ == '__main__':
    app.run(port=5555)
