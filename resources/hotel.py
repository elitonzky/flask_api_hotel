from importlib.resources import path
from multiprocessing import connection
from flask_restful import Resource, reqparse
from pkg_resources import require
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from models.hotel import HotelModel 
from flask_jwt_extended import jwt_required
import sqlite3


        
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        request = Struct(**parametros)
        
        if not parametros.get('cidade'):
            consulta = consulta_sem_cidade(request.estrelas_min, request.estrelas_max, request.diaria_min, 
                                           request.diaria_max, request.limit, request.offset)
            
        else:
            consulta = consulta_com_cidade(request.estrelas_min, request.estrelas_max, request.diaria_min, 
                                           request.diaria_max, request.cidade, request.limit, request.offset)
            
        resultado = cursor.execute(consulta)  
        hoteis = []
        
        for linha in resultado:
            hoteis.append(
                {'hotel_id': linha[0],
                 'nome': linha[1],
                 'estrelas': linha[2],
                 'diaria' : linha[3],
                 'cidade' : linha[4],
                 'site_id' : linha[5]
                     
                }
            )
        #hoteis = HotelModel.get_hoteis()
        
        if hoteis:
            print('tem hoteis')
            return hoteis, 200
        return {'message':'Not found'}, 404 #bad request


class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    arguments.add_argument('estrelas', type=float, required=True, help="the field 'estrelas' cannot be left blank. " )
    arguments.add_argument('diaria')
    arguments.add_argument('cidade')
    arguments.add_argument('site_id', type=int, required=True, help= "every hotel need be link with a site")


    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return {'message': f'{hotel.json()}'}, 200 # Success
        return {'message': 'Hotel not found'}, 404 # not found

    @jwt_required()
    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel {hotel_id} already exists '} , 400 # Bad Request

        dados = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {"message": 'The hotel must be associated to a valid site id'}, 400 # Bad request
        
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal erro ocurred trying to sava hotel.'}, 500 # Internal server error

        return {'message': f'Hotel created succes- {hotel.json()}'}, 200 #suceces
    
    @jwt_required()
    def put(self,hotel_id):
        dados = Hotel.arguments.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return {'message': f'Hotel has updated {hotel_encontrado.json()}'}, 200 # success
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal erro ocurred trying to sava hotel.'}, 500 # Internal server error
        return {'message': f'Hotel has created {hotel.json()}'}, 201 # created
    
    @jwt_required()
    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500 # internal server error
            return {'message': f'Hotel #{hotel_id} has ben deleted'}, 200 # success

        return {'message': f'Hotel #{hotel_id} not found'}, 404 # Not Found


class HoteisAll(Resource):
    def get(self):
        hoteis = HotelModel.get_hoteis()
        if hoteis:
            return hoteis, 200
        return {'message':'Not found'}, 404 #bad request
    
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)