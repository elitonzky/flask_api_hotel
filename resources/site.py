from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}
    

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404 # Not found
    
    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": f"The site {url} already exists."}, 400 #bad request
        site = SiteModel(url)
        try:    
            site.save_site()
        except:
            return {'message': 'Internal error ocurred Trying to create a new site.'}
        return site.json()
    
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'site has been deleted'}