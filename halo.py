# from flask import Flask, render_template, request
# from pyDatalog import pyDatalog

# app = Flask(__name__)

# def sistem_pakar(gejala_list):
#     pyDatalog.clear()
#     pyDatalog.create_terms('gejala, penyakit')

#     # Fakta-fakta gejala dan penyakit
#     pyDatalog.assert_fact('gejala', 'A01', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A02', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A03', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A04', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A05', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A06', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A11', 'Kulit Normal')
#     pyDatalog.assert_fact('gejala', 'A30', 'Kulit Normal')

#     pyDatalog.assert_fact('gejala', 'A07', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A08', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A09', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A16', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A23', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A24', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A25', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A26', 'Kulit Berminyak')
#     pyDatalog.assert_fact('gejala', 'A27', 'Kulit Berminyak')
    
#     pyDatalog.assert_fact('gejala', 'A01', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A05', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A10', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A11', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A12', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A13', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A20', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A27', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A30', 'Kulit Kering')
#     pyDatalog.assert_fact('gejala', 'A31', 'Kulit Kering')
    
#     pyDatalog.assert_fact('gejala', 'A07', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A14', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A15', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A16', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A17', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A23', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A25', 'Kulit Kombinasi')
#     pyDatalog.assert_fact('gejala', 'A26', 'Kulit Kombinasi')
    
#     pyDatalog.assert_fact('gejala', 'A09', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A12', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A18', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A19', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A20', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A21', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A22', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A28', 'Kulit Sensitif')
#     pyDatalog.assert_fact('gejala', 'A29', 'Kulit Sensitif')

#     # Mencari penyakit yang sesuai dengan gejala yang dimasukkan pengguna
#     scores = {}
#     for gejala in gejala_list:
#         penyakit_gejala = pyDatalog.ask('gejala("' + gejala.strip() + '", X)')
#         if penyakit_gejala:
#             for penyakit in penyakit_gejala.answers:
#                 scores[penyakit[0]] = scores.get(penyakit[0], 0) + 1
    
#     # Mengurutkan penyakit berdasarkan skor
#     sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
#     # Memilih penyakit dengan skor tertinggi
#     if sorted_scores:
#         most_likely_disease = max(sorted_scores, key=lambda x: x[1])[0]
#         return most_likely_disease
#     else:
#         return "Tidak ada penyakit yang sesuai dengan gejala yang dimasukkan."

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gejala_input = request.form['gejala']
#         gejala_list = gejala_input.split(',')

#         if len(gejala_list) < 5:
#             return render_template('index.html', hasil="Masukkan minimal 5 gejala.")

#         hasil = sistem_pakar(gejala_list)
#         return render_template('index.html', hasil=hasil)

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
