from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Recipes
from blueprints.recipeDetail.model import RecipeDetails
from blueprints.step.model import Steps
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import ast

bp_recipes = Blueprint('recipes', __name__)
api = Api(bp_recipes)


class RecipesResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        recipeQry = Recipes.query.get(id)
        if recipeQry is not None:
            return {'code': 200, 'message': 'oke',
                    'data': marshal(recipeQry, Recipes.responseFields)}, 200
        return {'code': 404, 'message': 'Recipe Not Found'}, 404

    # @jwt_required
    # @non_internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recipes', location='json')
        parser.add_argument('recipeDetails', location='json')
        parser.add_argument('steps', location='json')
        data = parser.parse_args()

        # convert string into dict or list
        dataRecipesDict = ast.literal_eval(data['recipes'])
        dataRecipeDetailsDict = ast.literal_eval(data['recipeDetails'])
        dataSteps = ast.literal_eval(data['steps'])

        # check all data's recipes is not null
        for key in dataRecipesDict:
            if type(dataRecipesDict[key]) == int:
                continue

            # to remove space at end
            dataRecipesDict[key] = dataRecipesDict[key].strip()
            if dataRecipesDict[key] == "":
                return {'code': 400,
                        'message': f'{key} tidak boleh kosong'}, 400

        # check all data's recipeDetails is not null
        for key in dataRecipeDetailsDict:
            if type(dataRecipeDetailsDict[key]) == int:
                continue

            # to remove space at end
            dataRecipeDetailsDict[key] = dataRecipeDetailsDict[key].strip()
            if dataRecipeDetailsDict[key] == "":
                return {'code': 400,
                        'message': f'{key} tidak boleh kosong'}, 400

        # check all data's steps is not null
        if dataSteps == []:
            return {'code': 400,
                    'message': 'Steps tidak boleh kosong'}, 400
        for stepDict in dataSteps:
            for key in stepDict:
                if type(stepDict[key]) == int:
                    continue

                stepDict[key] = stepDict[key].strip()  # to remove space at end
                if stepDict[key] == "":
                    return {'code': 400,
                            'message': f'{key} tidak boleh kosong'}, 400

        recipeDataInt = ['methodID', 'beanID', 'difficulty']

        # validate input data int for recipe
        for data in recipeDataInt:
            try:
                dataRecipesDict[data] = int(dataRecipesDict[data])
            except Exception as e:
                return {'code': 400, 'message': f'{data} harus integer'}, 400

        # validate input data int for recipeDetails
        for key in dataRecipeDetailsDict:
            if key != 'note':
                try:
                    dataRecipeDetailsDict[key] = int(
                        dataRecipeDetailsDict[key])
                except Exception as e:
                    return {'code': 400,
                            'message': f'{key} harus integer'}, 400

        # validate input data int for recipeDetails
        for stepDict in dataSteps:
            for key in stepDict:
                if key != 'note':
                    try:
                        stepDict[key] = int(stepDict[key])
                    except Exception as e:
                        return {'code': 400,
                                'message': f'{key} harus integer'}, 400


class RecipesListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('userID', type=int, location='args')
        parser.add_argument('methodID', type=int, location='args')
        parser.add_argument('orderby', location='args',
                            choices=('favoriteCount', 'difficulty'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        recipeQry = Recipes.query

        # to filter by userID or methodID
        if data['userID'] is not None:
            recipeQry = recipeQry.filter_by(userID=data['userID'])
        if data['methodID'] is not None:
            recipeQry = recipeQry.filter_by(methodID=data['methodID'])

        # to handle orderby difficulty or favouriteCount
        if data['orderby'] is not None:
            if data['orderby'] == 'favoriteCount':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.favoriteCount))
                else:
                    recipeQry = recipeQry.order_by((Recipes.favoriteCount))
            elif data['orderby'] == 'difficulty':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.difficulty))
                else:
                    recipeQry = recipeQry.order_by((Recipes.difficulty))

        recipes = []
        for recipe in recipeQry.limit(data['rp']).offset(offset).all():
            recipes.append(marshal(recipe, Recipes.responseFields))

        if recipes == []:
            return {'code': 404, 'message': 'Recipe Not Found'}, 404
        else:
            return {'code': 200, 'message': 'oke', 'data': recipes}, 200


api.add_resource(RecipesListResource, '')
api.add_resource(RecipesResource, '', '/<id>')
