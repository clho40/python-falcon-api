import falcon
import json
import common
from models import Service, Configuration, WSDL_URLS


class ConfigResource(object):
    def on_get(self,request,response):
        # Return 400 if <tenant> query string does not exist
        if not request.get_param("tenant"):
            raise falcon.HTTPBadRequest('Argument <tenant> is missing')

        # Return 400 if <integration_type> query string does not exist
        if not request.get_param("integration_type"):
            raise falcon.HTTPBadRequest('Argument <integration_type> is missing')
        
        tenant = request.get_param("tenant")
        integration_type = request.get_param("integration_type")

        # Query data from database
        result = Service.objects(tenant__iexact=tenant, integration_type__iexact=integration_type).exclude('id')

        # Return bad request if no data
        if result.count() < 1:
            raise falcon.HTTPBadRequest('No result')

        # Response
        response.status = falcon.HTTP_200
        response.body = result.to_json()

    def on_post(self,request,response):
        # Get raw data from request body
        try:
            raw_data = request.stream.read()
        except Exception as ex:
            raise falcon.HTTPBadRequest(ex.message)
        
        # Jsonify the raw data
        try:
            data = json.loads(raw_data,encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,'Unrecognized JSON','Unable to decode request body')

        # Return 404 if <tenant> does not exist
        if not data['tenant']:
            response.status = falcon.HTTP_404
            return

        # Return 404 if <integration_type> does not exist
        if not data['integration_type']:
            response.status = falcon.HTTP_404
            return

        # Validate data
        emptyValueKey = common.isEmpty(data['configuration'])
        if emptyValueKey:
            raise falcon.HTTPBadRequest('{} is missing'.format(emptyValueKey))
            return

        emptyValueKey = common.isEmpty(data['configuration']['wsdl_urls'])
        if emptyValueKey:
            raise falcon.HTTPBadRequest('{} is missing'.format(emptyValueKey))
            return

        # Query data from database
        result = Service.objects(tenant__iexact=data['tenant'], integration_type__iexact=data['integration_type']).exclude('id')
        
        ## No record found - insert new record. Else, update the existing record
        if result.count() < 1:
            new_config = Service(**data)
            new_config.save()
        else:
            result.modify(upsert=True, new=True, set__configuration=data['configuration'])

        # Response
        response.status = falcon.HTTP_200
        response.body = result.to_json()
        
def create():
    app = falcon.API()
    config = ConfigResource()
    app.add_route('/config',config)
    return app

app = create()



