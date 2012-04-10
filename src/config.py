global MONGO_SERVER
global PUGG_DB

try:
  MONGO_SERVER
except NameError:
  MONGO_SERVER="127.0.0.1"
  PUGG_DB="pugg_production"
