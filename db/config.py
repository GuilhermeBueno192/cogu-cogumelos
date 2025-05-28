import os

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"), #"hopper.proxy.rlwy.net"
    "user": os.getenv("DB_USER"), #"root"
    "password": os.getenv("DB_PASSWORD"), #"XSfSTYdadqgRBhKchGXpjSJCxHlDSgvU"
    "database": os.getenv("DB_DATABASE"), #"railway"
    "port": os.getenv("DB_PORT") #36504
}