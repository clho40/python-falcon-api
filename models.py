from mongoengine import *
connect('configapi')

class WSDL_URLS(EmbeddedDocument):
    session_url = StringField(required=True)
    booking_url = StringField(required=True)

class Configuration(EmbeddedDocument):
    username = StringField(required=True)
    password = StringField(required=True)
    wsdl_urls = EmbeddedDocumentField(WSDL_URLS)

class Service(Document):
    tenant = StringField(required=True)
    integration_type = StringField(required=True)
    configuration = EmbeddedDocumentField(Configuration)
