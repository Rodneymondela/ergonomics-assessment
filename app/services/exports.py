import io, pandas as pd
from flask import send_file
def export_assessments_csv(rows: list[dict]):
    buf = io.BytesIO()
    pd.DataFrame(rows).to_csv(buf, index=False)
    buf.seek(0)
    return send_file(buf, mimetype='text/csv', as_attachment=True, download_name='ergonomics_export.csv')
