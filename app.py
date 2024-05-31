from flask import Flask, render_template, request
from pyDatalog import pyDatalog

app = Flask(__name__)

def sistem_pakar(gejala_list, keyakinan_list):
    pyDatalog.clear()
    pyDatalog.create_terms('gejala, penyakit, bobot')
    
    # Fakta-fakta gejala dan penyakit beserta bobotnya
    gejala_bobot = {
        'Tidak Berminyak': ('Kulit Normal', 0.8),
        'Segar dan Halus': ('Kulit Normal', 0.8),
        'Bahan Bahan Kosmetik Mudah Menempel diKulit': ('Kulit Normal', 0.8),
        'Terlihat sehat': ('Kulit Normal', 0.8),
        'Tidak berjerawat': ('Kulit Normal', 0.8),
        'Mudah dalam memilih kosmetik': ('Kulit Normal', 0.8),
        'Pori-pori kulit besar terutama di area hidung pipi dagu': ('Kulit Berminyak', 0.8),
        'Kulit di bagian wajah terlihat mengkilat': ('Kulit Berminyak', 0.8),
        'Sering ditumbuhi jerawat': ('Kulit Berminyak', 0.8),
        'Kulit kelihatan kering sekali': ('Kulit Kering', 0.8),
        'Pori-pori halus': ('Kulit Kering', 0.6),
        'Tekstur kulit wajah tipis': ('Kulit Kering', 0.6),
        'Cepat menampakkan kerutan-kerutan': ('Kulit Kering', 0.8),
        'Sebagian kulit kelihatan berminyak': ('Kulit Kombinasi', 0.4),
        'Sebagian kulit kelihatan kering': ('Kulit Kombinasi', 0.6),
        'Kadang berjerawat': ('Kulit Kombinasi', 0.4),
        'Susah mendapat hasil polesan kosmetik yang sempurna': ('Kulit Kombinasi', 0.6),
        'Mudah Alergi': ('Kulit Sensitif', 0.8),
        'Mudah iritasi dan terluka': ('Kulit Sensitif', 0.8),
        'Kulit Mudah terlihat Kemerahan': ('Kulit Sensitif', 0.8),
    }

    # Memasukkan fakta ke pyDatalog
    for gejala, (penyakit, bobot) in gejala_bobot.items():
        pyDatalog.assert_fact('gejala', gejala, penyakit, bobot)
    
    # Menghitung score untuk setiap jenis kulit berdasarkan keyakinan
    score = {}
    for gejala, keyakinan in zip(gejala_list, keyakinan_list):
        penyakit_bobot = pyDatalog.ask(f'gejala("{gejala.strip()}", X, Y)')
        if penyakit_bobot:
            for penyakit, bobot in penyakit_bobot.answers:
                score[penyakit] = score.get(penyakit, 0) + (bobot * keyakinan)
    
    # Menentukan hasil akhir
    if score:
        most_likely_disease = max(score, key=score.get)
        return most_likely_disease
    else:
        return "Tidak ada penyakit yang sesuai dengan gejala yang dimasukkan."

@app.route('/', methods=['GET', 'POST'])
def index():
    gejala_options = [
        'Tidak Berminyak', 'Segar dan Halus', 'Bahan Bahan Kosmetik Mudah Menempel diKulit', 'Terlihat sehat', 'Tidak berjerawat', 
        'Mudah dalam memilih kosmetik', 'Pori-pori kulit besar terutama di area hidung pipi dagu', 'Kulit di bagian wajah terlihat mengkilat', 'Sering ditumbuhi jerawat', 'Kulit kelihatan kering sekali', 
        'Pori-pori halus', 'Tekstur kulit wajah tipis', 'Cepat menampakkan kerutan-kerutan', 'Sebagian kulit kelihatan berminyak', 'Sebagian kulit kelihatan kering', 
        'Kadang berjerawat', 'kosmetik yang sempurnakosmetik yang sempurna', 'Mudah Alergi', 'Mudah iritasi dan terluka', 'Kulit Mudah terlihat Kemerahan'
    ]
    keyakinan_options = [
        (0, ' Tidak Tahu'), (0.2, ' Tidak Yakin'), 
        (0.4, ' Agak Yakin'), (0.6, ' Cukup Yakin'), 
        (0.8, ' Yakin'), (1, ' Sangat Yakin')
    ]
    
    if request.method == 'POST':
        gejala_input = [request.form[f'gejala{i}'] for i in range(1, 6)]
        keyakinan_input = [float(request.form[f'keyakinan{i}']) for i in range(1, 6)]

        if len(gejala_input) < 5 or len(keyakinan_input) < 5:
            return render_template('index.html', hasil="Masukkan minimal 5 gejala dan tingkat keyakinan.", gejala_options=gejala_options, keyakinan_options=keyakinan_options)

        hasil = sistem_pakar(gejala_input, keyakinan_input)
        return render_template('index.html', hasil=hasil, gejala_options=gejala_options, keyakinan_options=keyakinan_options)

    return render_template('index.html', gejala_options=gejala_options, keyakinan_options=keyakinan_options)

if __name__ == '__main__':
    app.run(debug=True)

