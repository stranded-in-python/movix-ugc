from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.database import Postgresql
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django

with Diagram("movix-admin", show=False, outformat="png"):
    client = Mobile("Client")
    endpoints = Nginx("API gateway")
    dj_admin = Django("Admin")

    with Cluster("movie API"):
        detail = Django("DetailView")
        lst = Django("ListView")
        apis = [detail, lst]

    db = Postgresql("movies_db")

    client >> endpoints
    endpoints >> dj_admin
    endpoints >> apis
    dj_admin >> Edge(label="Add/Delete movies, persons, genres") >> db
    apis[0] >> Edge(label="Get single movie") >> db
    apis[1] >> Edge(label="Get list ") >> db
