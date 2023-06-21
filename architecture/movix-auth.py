from diagrams import Diagram, Cluster, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Fastapi
from diagrams.generic.storage import Storage
from diagrams.onprem.database import Postgresql
from diagrams.onprem.network import Nginx
from diagrams.ibm.devops import ConfigurationManagement
from diagrams.oci.security import KeyManagement
from diagrams.ibm.blockchain import MembershipServicesProviderApi
from diagrams.oci.governance import Groups, Policies
from diagrams.oci.security import Encryption, IDAccess

with Diagram("movix-auth", show=False, outformat="png"):
    client = Mobile("Client")
    endpoints = Nginx("API gateway")
    routers = Fastapi("Routers")
    oauth_router = Fastapi("oauth2")
    providers = IDAccess("Resource Owners")

    with Cluster("Managers"):
        jwt = Encryption("jwt")
        rights = Policies("access rights")
        role = Policies("role")
        user = Groups("user")
        managers = [jwt, rights, role, user]
    
    with Cluster("JWT Token Strategy"):
        refresh = KeyManagement("refresh")
        access = KeyManagement("access")
        tokens = [refresh, access]
    
    blacklist = Redis("Blacklist")

    db_objects = Storage("Storage Objects")

    cache = Redis("Cache")

    database = Postgresql("Database")

    client >> endpoints >> routers
    routers - Edge(style="dashed") - oauth_router >> providers
    routers >> managers
    
    jwt >> tokens >> blacklist
    
    managers >> db_objects >> Edge(label="Except for user") >> cache
    cache >> Edge(label="If no cached response", style="dashed") >> database
