# Committee Assignment Optimization

Proyek ini membandingkan Hungarian Algorithm, Genetic Algorithm, dan Hill-Climbing dengan Random Restart untuk menempatkan panitia ke divisi berdasarkan skor kecocokan sintetis.

## Batasan model
- Setiap panitia ditempatkan tepat pada satu divisi.
- Setiap divisi memiliki kapasitas sama pada eksperimen ini.
- Jumlah panitia harus habis dibagi jumlah divisi.
- Skor 20–100 dibuat secara acak dan bukan penilaian orang sungguhan.
- Tujuan adalah memaksimalkan total skor kecocokan.

## Menjalankan di Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/generate_data.py --members 30 --divisions 5 --seed 20261048 --output data/synthetic_scores.csv
python src/run_experiments.py --input data/synthetic_scores.csv --repeats 5 --output results/benchmark_results.csv
```

## Catatan eksperimen
Waktu komputasi bergantung pada perangkat dan konfigurasi. Untuk laporan akademik, jalankan ulang pada komputer sendiri dan laporkan kondisi pengujian aktual. Hasil contoh yang disertakan dalam laporan dibuat dari eksperimen lokal dengan konfigurasi yang dijelaskan.
