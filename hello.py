from flask import Flask, redirect, render_template, request, url_for
from pyDatalog import pyDatalog
import urllib.parse

hello = Flask(__name__)

def sistem_pakar(gejala_list, keyakinan_list):
    pyDatalog.clear()
    pyDatalog.create_terms('gejala, penyakit, bobot')
    
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

    for gejala, (penyakit, bobot) in gejala_bobot.items():
        pyDatalog.assert_fact('gejala', gejala, penyakit, bobot)
    
    score = {}
    for gejala, keyakinan in zip(gejala_list, keyakinan_list):
        penyakit_bobot = pyDatalog.ask(f'gejala("{gejala.strip()}", X, Y)')
        if penyakit_bobot:
            for penyakit, bobot in penyakit_bobot.answers:
                score[penyakit] = score.get(penyakit, 0) + (bobot * keyakinan)
    
    total_score = sum(score.values())
    if total_score > 0:
        percentage = {penyakit: round((score[penyakit] / total_score) * 100, 2) for penyakit in score}
        most_likely_disease = max(score, key=score.get)
        return most_likely_disease, percentage
    else:
        return "Tidak ada penyakit yang sesuai dengan gejala yang dimasukkan.", {}


@hello.route('/', methods=['GET', 'POST'])
def index():
    gejala_options = [
        'Tidak Berminyak', 'Segar dan Halus', 'Bahan Bahan Kosmetik Mudah Menempel diKulit', 'Terlihat sehat', 'Tidak berjerawat', 
        'Mudah dalam memilih kosmetik', 'Pori-pori kulit besar terutama di area hidung pipi dagu', 'Kulit di bagian wajah terlihat mengkilat', 'Sering ditumbuhi jerawat', 'Kulit kelihatan kering sekali', 
        'Pori-pori halus', 'Tekstur kulit wajah tipis', 'Cepat menampakkan kerutan-kerutan', 'Sebagian kulit kelihatan berminyak', 'Sebagian kulit kelihatan kering', 
        'Kadang berjerawat', 'kosmetik yang sempurnakosmetik yang sempurna', 'Mudah Alergi', 'Mudah iritasi dan terluka', 'Kulit Mudah terlihat Kemerahan'
    ]
    keyakinan_options = [
        (0, 'Tidak Tahu'), (0.2, 'Tidak Yakin'), 
        (0.4, 'Agak Yakin'), (0.6, 'Cukup Yakin'), 
        (0.8, 'Yakin'), (1, 'Sangat Yakin')
    ]
    
    if request.method == 'POST':
        gejala_input = request.form.getlist('gejala[]')
        keyakinan_input = [float(k) for k in request.form.getlist('keyakinan[]')]
        nama = request.form['nama']
        usia = request.form['usia']
        jeniskelamin = request.form['jeniskelamin']

        if len(gejala_input) < 1 or len(keyakinan_input) < 1:
            return render_template('index.html', hasil="Masukkan minimal 1 gejala dan tingkat keyakinan.", gejala_options=gejala_options, keyakinan_options=keyakinan_options)

        hasil, persentase = sistem_pakar(gejala_input, keyakinan_input)
        persentase_str = urllib.parse.urlencode(persentase)

        if hasil == 'Kulit Berminyak':
            if jeniskelamin == 'Laki-Laki':
                return redirect(url_for('minyak', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
            else:
                return redirect(url_for('minyakPerempuan', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))    
            
        elif hasil == 'Kulit Kering':
            if jeniskelamin == 'Laki-Laki':
                return redirect(url_for('kering', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
            else:
                return redirect(url_for('keringPerempuan', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
        elif hasil == 'Kulit Normal':
            if jeniskelamin == 'Laki-Laki':
                return redirect(url_for('normal', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
            else:
                return redirect(url_for('normalPerempuan', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
        elif hasil == 'Kulit Kombinasi':
            if jeniskelamin == "Laki-Laki":
                return redirect(url_for('kombinasi', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
            else:
                return redirect(url_for('kombinasiPerempuan', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
        elif hasil == 'Kulit Sensitif':
            if jeniskelamin == 'Laki-Laki':
                return redirect(url_for('sensitif', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
            else:
                return redirect(url_for('sensitifPerempuan', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase_str))
        else:
            return render_template('index.html', hasil="Tidak ada penyakit yang sesuai dengan gejala yang dimasukkan.", gejala_options=gejala_options, keyakinan_options=keyakinan_options)

    return render_template('index.html', gejala_options=gejala_options, keyakinan_options=keyakinan_options)

@hello.route('/minyakPerempuan')
def minyakPerempuan():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('minyakPerempuan.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/minyakLaki')
def minyak():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('minyak.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

# Ulangi cara ini untuk route lainnya seperti 'kering', 'normal', 'kombinasi', dan 'sensitif'
@hello.route('/keringLaki')
def kering():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('kering.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/keringPerempuan')
def keringPerempuan():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('keringPerempuan.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/normalLaki')
def normal():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('normal.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/normalPerempuan')
def normalPerempuan():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('normalPerempuan.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/kombinasiLaki')
def kombinasi():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('kombinasi.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/kombinasiPerempuan')
def kombinasiPerempuan():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('kombinasiPerempuan.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/sensitifLaki')
def sensitif():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('sensitif.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)

@hello.route('/sensitifPerempuan')
def sensitifPerempuan():
    nama = request.args.get('nama')
    usia = request.args.get('usia')
    jeniskelamin = request.args.get('jeniskelamin')
    persentase = {k: float(v[0]) for k, v in urllib.parse.parse_qs(request.args.get('persentase')).items()}
    return render_template('sensitifPerempuan.html', nama=nama, usia=usia, jeniskelamin=jeniskelamin, persentase=persentase)


if __name__ == '__main__':
    hello.run(debug=True)