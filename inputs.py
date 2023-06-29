# -----------------------------------------------
# specify your InfluxDB details
influx_bucket = "HyTime"
#influx_bucket = "GENZE"
token = "9Mb7LIddgV-u7RkmbOhyi_9TGQ2VCy4Zjoo29x5LUIxDMoKA078TpcAA2bFMaNlG3rvdsz6eREdNBPeLvaMo8w=="
influx_url = "http://localhost:8086"
org_id = "e596ec1517ee6a33"

# -----------------------------------------------
# specify devices to process from local disk via ["folder/device_id"] or S3 via ["bucket/device_id"]
devices = ["hytime/26656490"]
#devices = ["genze/DF88D1C6"]
# -----------------------------------------------
# specify DBC paths and a list of signals to process ([]: include all signals)
# optionally include signal prefixes to make CAN ID, PGN and/or BusChannel explicit
dbc_paths = ["dbc_files/HF831-102-A-Dataloggers_CH1_CH2_database.dbc"]
# dbc_paths = ["dbc_files/HF831-Data logger_CH1_CH2.dbc"]
signals = []
can_id_prefix = False
pgn_prefix = False
bus_prefix = False

# specify resampling frequency. Setting this to "" means no resampling (much slower)
res = "5S"

# -----------------------------------------------
# specify whether to load data from S3 (and add server details if relevant)
s3 = True
key = "HYPER"
secret = "MOTIVE2023"
endpoint = "http://192.168.95.189:9000"  # e.g. http://s3.us-east-1.amazonaws.com or http://192.168.0.1:9000
region = "us-east-1" # only relevant if you are using more recent builds of MinIO S3 as the backend
# cert = "path/to/cert.crt"  # if MinIO + TLS, add path to cert and update utils.py/setup_fs to verify

# -----------------------------------------------
# if dynamic = True, data is loaded dynamically based on most recent data in InfluxDB - else default_start is used
dynamic = True
default_start = "2023-05-22 00:00:00"
days_offset = None  # offsets data to start at 'today - days_offset'. Set to None to use original timestamps

# if you're using data encryption, you can add the password below
pw = {"default": "password"}

# if you need to process multi-frame data, set tp_type to "uds", "j1939" or "nmea"
tp_type = ""
