from diagrams import Cluster, Diagram, Edge
from diagrams.elastic.saas import Elastic
from diagrams.generic.device import Mobile
from diagrams.generic.storage import Storage
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Fastapi

with Diagram("movix-api", show=False, outformat="png"):
    client = Mobile("client")
    endpoints = Nginx("API gateway")

    with Cluster("Services"):
        film_serv = Fastapi("films")
        genres_serv = Fastapi("genres")
        persons_serv = Fastapi("persons")
        services = [film_serv, genres_serv, persons_serv]

    with Cluster("Storages"):
        films_stor = Storage("films")
        genres_stor = Storage("genres")
        persons_stor = Storage("persons")
        storages = [films_stor, genres_stor, persons_stor]

    cache = Redis("Cache")
    storage = Elastic("AsyncElasticSearch")

    client >> endpoints >> services
    film_serv >> films_stor
    genres_serv >> genres_stor
    persons_serv >> persons_stor
    storages >> cache
    cache >> Edge(label="if no cached response") >> storage
