USER = 'postgres'
PASSWORD = '123'
HOST = 'localhost'
PORT = '5432'
DATABASE_NAME = 'dbhelm'

DEV_SCALE = {
    'harga': {
        '100000 - 199999': 5,
        '200000 - 349999': 4, 
        '350000 - 399999': 3, 
        '400000 - 649999': 2, 
        '650000 - 700000': 1, 
    },
    'berat': {
        '1400 gram': 5, 
        '1300 gram': 4, 
        '1200 gram': 3, 
        '1100 gram': 2, 
        '1000 gram': 1
    },
    'double_visor': {
        'Ada': 5,
        'Tidak Ada': 2,
    },
    'sertifikasi' : {
        'SNI': 5,
        'SNI DOT': 4,
    },
    'garansi' : {
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
        '1': 1,
    },
}