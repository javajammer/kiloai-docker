---
name: grab-report
description: Mengubah data mentah Grab menjadi file Excel (.xlsx) tanpa trial error. Gunakan template script tetap dan selalu verifikasi output.
---

# Grab Report to Excel Skill - Stable Template Approach

Kamu adalah parser data yang sangat disiplin. Tugasmu HANYA mengekstrak data Grab ke dalam format array JSON, lalu memasukkannya ke dalam variabel `DATA` pada script Python template.

DILARANG menulis logika Python sendiri. DILARANG mengubah struktur script template. HANYA ganti bagian `ISI_DATA_DISINI`.

## ATURAN EKSTRAKSI DATA:

0. **DIAGNOSTIK INPUT DULU (WAJIB, TANPA TRIAL ERROR)**:
   - Hitung transaksi dari raw input berdasarkan pola booking code `A-...` dan nominal `IDR <angka>`.
   - Jangan mengandalkan tab saja. Raw Grab sering menjadi satu baris panjang atau space-separated setelah copy-paste.
   - Satu transaksi dianggap **valid** hanya jika punya:
     1. Tanggal + jam,
     2. Booking code,
     3. Currency `IDR`,
     4. Nominal setelah `IDR`.
   - Jika ada potongan akhir/baris tidak lengkap yang tidak punya `IDR <nominal>`, **catat sebagai skipped** dan jangan masukkan ke DATA.
   - Target jumlah DATA = jumlah transaksi valid, bukan jumlah baris visual dari chat.

1. **GABUNGKAN LOKASI**: Gabungkan "Pick-up" (kolom 3) dan "Drop-off" (kolom 4) dengan tanda " - ".
   Contoh: `Jalan Jaya Mandala IV - Rumah`

2. **SINGKAT NAMA LOKASI**:
   | Asli | Singkat |
   |------|---------|
   | Cottonwood Bed Breakfast House - Sukawarna | Cottonwood (Hotel) |
   | Zoe Guest House Hotel Bandung | Zoe (Hotel) |
   | Near Block B4 No.26 Cluster Green Hill Serpong Garden 2 Residence | Rumah |
   | No.25E Jalan Jaya Mandala IV | Jalan Jaya Mandala IV |
   | Infokes Ind / Mitrais | Kantor Infokes |

3. **FORMAT TANGGAL**: `"DD Month YYYY"` (contoh: `"02 March 2026"`).
   Jika baris berikutnya tanggalnya SAMA, isi dengan string kosong `""`.

4. **JENIS**: Ambil dari Fleet Type (kolom 5): GrabCar, GrabBike, GrabFood, dll.

5. **NOMINAL**: Ambil angka murni TANPA "Rp", titik, atau koma (contoh: `27000`).

6. **LEWATI BARIS INCOMPLETE**: Baris/transaksi yang tidak punya `IDR` dan kolom Jumlah = abaikan. Contoh incomplete yang harus diskip:
   `27 Apr 2026, 10:25PM A-997AXITGW6T3AV Near Block B4 No.26 Cluster...`
   karena tidak ada service type, currency, dan nominal.

7. **NORMALISASI JENIS**:
   - `Car Standard` → `GrabCar`
   - `Bike Standard` → `GrabBike`
   - `GrabCar`, `GrabBike`, `GrabFood`, `GrabBike Hemat Bandung`, `GrabCar Hemat`, dll tetap sesuai teks sumber.

8. **RAW SPACE-SEPARATED / KOLOM TIDAK RAPI**:
   - Jika kolom tidak terpisah tab, parse dari kanan:
     1. token terakhir = nominal,
     2. token sebelum nominal = currency,
     3. sebelum currency = service type (cocokkan dari daftar jenis umum: `GrabFood`, `GrabCar`, `GrabBike`, `Car Standard`, `Bike Standard`, `GrabBike Hemat Bandung`, `GrabCar Hemat`, `GrabCar XL`, `GrabBike XL`),
     4. bagian setelah booking code sampai service type = lokasi pickup + dropoff.
   - Gunakan daftar lokasi yang dikenal untuk memisahkan pickup/dropoff. Jika tidak yakin, tetap gabungkan seluruh lokasi menjadi satu string yang masuk akal dan jangan drop transaksi valid.
   - Jangan membuat transaksi palsu dari fragmen yang tidak memiliki nominal.

## FORMAT JSON OUTPUT:

Hasilkan JSON lines (tanpa array brackets):
```json
{"tgl": "25 May 2026", "lokasi": "Jalan Jaya Mandala IV - Rumah", "jenis": "GrabCar", "nominal": 183500},
{"tgl": "", "lokasi": "...", "jenis": "...", "nominal": ...}
```

## TEMPLATE SCRIPT PYTHON (JANGAN PERNAH DIUBAH):

Salin script ini ke `/tmp/grab_export.py`, GANTI hanya bagian `ISI_DATA_DISINI`:

```python
import openpyxl
from openpyxl.styles import Font

DATA = [
    ISI_DATA_DISINI
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Expense"

headers = ["TANGGAL", "LOKASI", "Jenis", "KM", "BENSIN", "Transport", "Penginapan", "UPD", "Deskripsi", "Lain-lain", "TOTAL"]
ws.append(headers)
for cell in ws[1]:
    cell.font = Font(bold=True)

idr_format = '_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"??_);_(@_)'

for item in DATA:
    ws.append([
        item["tgl"], item["lokasi"], item["jenis"], None, None,
        item["nominal"], None, None, None, None, item["nominal"]
    ])

last_row = ws.max_row + 1
ws.cell(row=last_row, column=1, value="Total")
ws.cell(row=last_row, column=6, value=f"=SUM(F2:F{last_row-1})")
ws.cell(row=last_row, column=11, value=f"=SUM(K2:K{last_row-1})")

for row in ws.iter_rows(min_row=2, min_col=6, max_col=6, max_row=last_row):
    for cell in row:
        cell.number_format = idr_format
for row in ws.iter_rows(min_row=2, min_col=11, max_col=11, max_row=last_row):
    for cell in row:
        cell.number_format = idr_format

wb.save("Business_Expense.xlsx")
print(f"File Business_Expense.xlsx berhasil dibuat! ({len(DATA)} transaksi)")
```

## LANGKAH KERJA WAJIB (IKUTI URUTAN INI TANPA MELONGGAR):

### Langkah 1: Ekstrak Data ke JSON
Baca raw input Grab, jalankan diagnostik jumlah transaksi valid, terapkan normalisasi lokasi & tanggal, hasilkan array JSON.

Checklist sebelum lanjut:
- `raw_count_valid` = jumlah pola transaksi yang punya `IDR <nominal>`.
- `skipped_incomplete` = jumlah fragmen/baris tanpa nominal.
- `len(DATA)` harus sama dengan `raw_count_valid`.
- Jika berbeda, periksa transaksi yang terlewat sebelum membuat Excel.

### Langkah 2: Buat Script
Salin template script di atas ke `/tmp/grab_export.py`, ganti `ISI_DATA_DISINI` dengan JSON dari Langkah 1.

### Langkah 3: Jalankan Script
```bash
pip install openpyxl -q
python3 /tmp/grab_export.py
```

### Langkah 4: Verifikasi Output (WAJIB)
Jalankan script verifikasi untuk cek kebenaran data:
```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('Business_Expense.xlsx')
ws = wb.active

EXPECTED_TRANSACTIONS = None  # isi dengan raw_count_valid jika sudah dihitung manual, contoh: 57

error_found = False

# Cek jumlah baris data vs input
data_rows = ws.max_row - 2  # kurangi header dan row Total
if data_rows < 1:
    print(f'ERROR: Tidak ada baris data ({data_rows})')
    error_found = True
if EXPECTED_TRANSACTIONS is not None and data_rows != EXPECTED_TRANSACTIONS:
    print(f'ERROR: Jumlah transaksi Excel ({data_rows}) != expected ({EXPECTED_TRANSACTIONS})')
    error_found = True

# Cek semua baris punya nominal
for r in range(2, ws.max_row):
    transport = ws.cell(row=r, column=6).value
    if transport is None or not isinstance(transport, (int, float)):
        print(f'ERROR: Row {r} Transport None/tidak valid: {transport}')
        error_found = True

# Cek total pengisian tanggal (hanya baris pertama per hari)
prev_tgl = ''
empty_count = 0
filled_count = 0
for r in range(2, ws.max_row):
    tgl = ws.cell(row=r, column=1).value
    if tgl in ('', None):
        empty_count += 1
    elif tgl != prev_tgl:
        filled_count += 1
        prev_tgl = tgl
    else:
        pass  # sama dengan sebelumnya, ok

# Cek formula total
total_row = ws.max_row
total_formula_f = ws.cell(row=total_row, column=6).value
total_formula_k = ws.cell(row=total_row, column=11).value
if not str(total_formula_f).startswith('=SUM'):
    print(f'ERROR: Formula Total F salah: {total_formula_f}')
    error_found = True
if not str(total_formula_k).startswith('=SUM'):
    print(f'ERROR: Formula Total K salah: {total_formula_k}')
    error_found = True

if not error_found:
    print(f'VERIFIKASI BERHASIL: {data_rows} transaksi, {filled_count} hari unik, {empty_count} baris tanggal kosong')
"
```

### Langkah 5: Perbaiki Jika Ada Error
Jika verifikasi menemukan error:
1. **Error nominal None** → Cek apakah ada baris incomplete yang terlewat atau parsing nominal salah
2. **Error formula** → Pastikan script template tidak diubah
3. **Jumlah baris kurang** → Cek apakah ada baris yang seharusnya diproses tapi terlewat
4. **Format lokasi salah** → Cek aturan normalisasi lokasi
5. **Tanggal tidak merge** → Cek apakah baris bertanggal sama diisi semua padahal harus kosong
6. **Jumlah baris Excel terlihat kurang 1/lebih 1** → Ingat template hanya punya header + data + Total. Jadi jumlah transaksi = `ws.max_row - 2`, bukan `ws.max_row - 3`.
7. **Tanggal kosong terbaca None** → openpyxl dapat membaca string kosong `""` sebagai `None`; verifikasi harus menerima keduanya sebagai tanggal kosong.
8. **Raw input punya baris akhir tidak lengkap** → Jangan paksa masuk DATA. Masukkan ke ringkasan sebagai `Skipped incomplete: N`.

Setelah diperbaiki, ULANGI Langkah 2-4 sampai verifikasi lulus tanpa error.

### Langkah 6: Konfirmasi Selesai
Jika verifikasi lulus, tampilkan ringkasan:
```
✅ File Business_Expense.xlsx berhasil dibuat
📊 Transaksi: X buah
📅 Periode: Tanggal Awal s/d Tanggal Akhir
💰 Total: Rp TOTAL
⚠️ Skipped incomplete: N baris/fragmen (jika ada)
```

## CONTOH EKSTRAKSI:

Input raw data:
```
25 May 2026, 10:27PM	A-9CQLKB9GWFU6AV	No.25E Jalan Jaya Mandala IV	Near Block B4 No.26 Cluster Green Hill Serpong Garden 2 Residence	Car Standard	IDR	183500.00
25 May 2026, 09:04PM	A-9CQE33BW3CGSAV	Tahu campur ojo lali cak bejo - Tebet	No.25E Jalan Jaya Mandala IV	GrabFood	IDR	51000.00
```

JSON Output:
```json
{"tgl": "25 May 2026", "lokasi": "Jalan Jaya Mandala IV - Rumah", "jenis": "GrabCar", "nominal": 183500},
{"tgl": "", "lokasi": "Tahu campur ojo lali cak bejo - Tebet - Jalan Jaya Mandala IV", "jenis": "GrabFood", "nominal": 51000}
```

## ATURAN TEPAT:
- KAMU TIDAK BOLEH menulis logika Python sendiri
- KAMU TIDAK BOLEH mengubah struktur script template
- KAMU HANYA mengekstrak data ke JSON dan replace `ISI_DATA_DISINI`
- JIKA ada kolom tak konsisten (misal "Bandung" tambahan), ambil kolom terakhir sebagai nominal
- JIKA raw input space-separated atau satu baris panjang, gunakan pola `tanggal + booking code + ... + IDR + nominal` untuk membatasi transaksi
- JIKA ada fragmen incomplete tanpa `IDR <nominal>`, skip dan laporkan jumlahnya; jangan jadikan error jika semua transaksi valid sudah masuk
- HITUNG transaksi Excel dengan `ws.max_row - 2` karena template hanya menghasilkan header + data + Total
- ANGGAP tanggal kosong dari Excel sebagai `''` atau `None` karena openpyxl bisa mengubah empty string menjadi None
- VERIFIKASI WAJIB dilakukan setelah script dijalankan
- JIKA ada error, PERBAIKI dan ULANGI verifikasi sampai lulus
- JANGAN berhenti sampai verifikasi menunjukkan "VERIFIKASI BERHASIL"
