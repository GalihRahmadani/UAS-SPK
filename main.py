from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import Helm as HelmModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from tabulate import tabulate

session = Session(engine)

app = Flask(__name__)
api = Api(app)


class BaseMethod():

    def __init__(self):
        self.raw_weight = {'harga': 5, 'berat':3,'double_visor': 4, 
                           'sertifikasi': 5, 'garansi': 4}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(HelmModel.no, HelmModel.nama_helm, HelmModel.harga, HelmModel.berat,
                       HelmModel.double_visor, HelmModel.sertifikasi, HelmModel.garansi)
        result = session.execute(query).fetchall()
        print(result)
        return [{'no': Helm.no,'nama_helm': Helm.nama_helm, 'harga': Helm.harga,
                'berat': Helm.berat, 'double_visor': Helm.double_visor, 'sertifikasi': Helm.sertifikasi, 'garansi': Helm.garansi} for Helm in result]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nama_helm_values = [] # max
        harga_values = []  # min
        berat_values = []  # max
        double_visor_values = []  # max
        sertifikasi_values = []  # max
        garansi_values = []  # max

        for data in self.data:
            # Nama_Helm
            nama_helm_spec = data['nama_helm']
            numeric_values = [int(value.split()[0]) for value in nama_helm_spec.split(
                ',') if value.split()[0].isdigit()]
            max_nama_helm_value = max(numeric_values) if numeric_values else 1
            nama_helm_values.append(max_nama_helm_value)

            # Harga
            harga_cleaned = ''.join(
                char for char in data['harga'] if char.isdigit())
            harga_values.append(float(harga_cleaned)
                                if harga_cleaned else 0)  # Convert to float
            
            # Berat
            berat_spec = data['berat']
            berat_numeric_values = [int(
                value.split()[0]) for value in berat_spec.split() if value.split()[0].isdigit()]
            max_berat_value = max(
                berat_numeric_values) if berat_numeric_values else 1
            berat_values.append(max_berat_value)

            # Double_Visor
            double_visor_spec = data['double_visor']
            double_visor_numeric_values = [float(value.split()[0]) for value in double_visor_spec.split(
            ) if value.replace('.', '').isdigit()]
            max_double_visor_value = max(
                double_visor_numeric_values) if double_visor_numeric_values else 1
            double_visor_values.append(max_double_visor_value)

            # Sertifikasi
            sertifikasi_spec = data['sertifikasi']
            sertifikasi_numeric_values = [
                int(value) for value in sertifikasi_spec.split() if value.isdigit()]
            max_sertifikasi_value = max(
                sertifikasi_numeric_values) if sertifikasi_numeric_values else 1
            sertifikasi_values.append(max_sertifikasi_value)

            # Garansi
            garansi_spec = data['garansi']
            garansi_numeric_values = [
                int(value) for value in garansi_spec.split() if value.isdigit()]
            max_garansi_value = max(
                garansi_numeric_values) if garansi_numeric_values else 1
            garansi_values.append(max_garansi_value)

        return [
    {
        'no': data['no'],
        'nama_helm': nama_helm_value / max(nama_helm_values),
        'harga': min(harga_values) / max(harga_values) if max(harga_values) != 0 else 0,
        'berat': berat_value / max(berat_values),
        'double_visor': double_visor_value / max(double_visor_values),
        'sertifikasi': sertifikasi_value / max(sertifikasi_values),
        'garansi': garansi_value / max(garansi_values),
    }
    for data, nama_helm_value, harga_value, berat_value, double_visor_value, sertifikasi_value, garansi_value
    in zip(self.data, nama_helm_values, harga_values, berat_values, double_visor_values, sertifikasi_values, garansi_values)
]


    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'no': row['no'],
                'produk': row['harga']**self.weight['harga'] *
                row['berat']**self.weight['berat'] *
                row['double_visor']**self.weight['double_visor'] *
                row['sertifikasi']**self.weight['sertifikasi'] *
                row['garansi']**self.weight['garansi'],
                'nama_helm': row.get('nama_helm', '')
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'ID': product['no'],
                'score': round(product['produk'], 3)
            }
            for product in sorted_produk
        ]
        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return sorted(result, key=lambda x: x['score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'helm': sorted(result, key=lambda x: x['score'], reverse=True)}, HTTPStatus.OK.value


class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = [
            {
                'ID': row['no'],
                'Score': round(row['harga'] * weight['harga'] +
                               row['berat'] * weight['berat'] +
                               row['double_visor'] * weight['double_visor'] +
                               row['sertifikasi'] * weight['sertifikasi'] +
                               row['garansi'] * weight['garansi'], 3)
            }
            for row in self.normalized_data
        ]
        sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return sorted(result, key=lambda x: x['Score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'helm': sorted(result, key=lambda x: x['Score'], reverse=True)}, HTTPStatus.OK.value


class Helm(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None

        if page > page_count or page < 1:
            abort(404, description=f'Data Tidak Ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next_page,
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = session.query(HelmModel).order_by(HelmModel.no)
        result_set = query.all()
        data = [{'no': row.no, 'nama_helm': row.nama_helm, 'harga': row.harga,
                 'berat': row.berat, 'double_visor': row.double_visor, 'sertifikasi': row.sertifikasi, 'garansi': row.garansi}
                for row in result_set]
        return self.get_paginated_result('helm/', data, request.args), 200


api.add_resource(Helm, '/helm')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)