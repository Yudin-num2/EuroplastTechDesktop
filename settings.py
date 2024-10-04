import configparser

config = configparser.ConfigParser()
config.read('server_config.ini')


# ---------------------------- Postgres settings ----------------------------#

PG_USER = config.get('Postgres', 'PG_USER')
PG_PASSW = config.get('Postgres', 'PG_PASSW')
PG_HOST = config.get('Postgres', 'PG_HOST')
PG_PORT = config.get('Postgres', 'PG_PORT')
PG_DB_NAME = config.get('Postgres', 'PG_DB_NAME')

# ---------------------------------------------------------------------------#


print(PG_USER, PG_PASSW, PG_HOST, PG_PORT, PG_DB_NAME)
