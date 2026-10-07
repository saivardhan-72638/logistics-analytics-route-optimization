from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA_RAW=ROOT/'data/raw'; DATA_PROCESSED=ROOT/'data/processed'; OUTPUTS=ROOT/'outputs'; FIGURES=OUTPUTS/'figures'; REPORTS=OUTPUTS/'reports'; MODELS=OUTPUTS/'models'
for p in [DATA_RAW,DATA_PROCESSED,FIGURES,REPORTS,MODELS]: p.mkdir(parents=True,exist_ok=True)
