from suds.client import Client
from suds.client import WebFault
from suds.sudsobject import asdict
from model.project import Project
import xml.etree.ElementTree as ET
import  xml.etree.cElementTree as CET
from pysimplesoap import simplexml
from pysimplesoap.client import SoapClient
from bs4 import BeautifulSoup

import logging
#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

class SoapHelper:

    def __init__(self, app):
        self.app = app
        #self.soapuser = soapuser
        #self.soappass = soappass
        #self.password = password




    def mc_projects_get_user_accessible(self, soapuser, soappass):
        client = Client("http://localhost/mantisbt-2.20.0/api/soap/mantisconnect.php?wsdl")
        proj_list = []
        dict = {}
        #dict = client.service.mc_projects_get_user_accessible(soapuser, soappass)

        try:


            for row in (client.service.mc_projects_get_user_accessible(soapuser, soappass)):
                id = row.id
                name =row.name
                status=(row.status.id, row.status.name)
                access_min = (row.access_min.id, row.access_min.name)
                file_path = row.file_path
                description = row.description
                subprojects = [row.subprojects]
                #row.enabled, (row.view_state.id), row.view_state.name), (str(row.access_min.id), row.access_min.name), row.file_path, row.description, row.subprojects
                proj_list.append(Project(id=str(id), name=str(name), description=str(description)))
                #print(proj_list)

             #   id = row.get('id')
              #  name = row.get('name')
               # proj_list.append(Project(id=str(id), name=name))
            return proj_list

        except WebFault:
            return False

    #def destroy(self):
     #   self.connection.close()

    #def can_login(self, username, password):
     #   client = Client("http://localhost/mantisbt-2.20.0/api/soap/mantisconnect.php?wsdl")
      #  try:
       #     client.service.mc_login(username, password)
        #    return True
        #except:
         #   return False