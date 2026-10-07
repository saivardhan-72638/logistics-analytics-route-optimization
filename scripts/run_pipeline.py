import argparse,json
from src.config import DATA_RAW,DATA_PROCESSED,FIGURES,REPORTS,MODELS
from src.data_prep import load_olist,build_order_table
from src.kpis import calculate_kpis,save_kpis
from src.eda import run_eda
from src.models import train_models
from src.clustering import run_clustering
from src.routing import optimize,dist

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--real-data',action='store_true'); args=ap.parse_args(); o,i,c,r=load_olist(DATA_RAW); d=build_order_table(o,i,c,r); d.to_csv(DATA_PROCESSED/'delivered_orders.csv',index=False); k=calculate_kpis(d); save_kpis(k,REPORTS/'kpis.csv'); figs=run_eda(d,FIGURES); models=train_models(d,MODELS); cl=run_clustering(d,REPORTS/'state_clusters.csv')
 coords=[(-23.55,-46.63),(-22.91,-43.17),(-19.92,-43.94),(-25.43,-49.27),(-12.97,-38.50),(-30.03,-51.23),(-27.59,-48.55),(-16.68,-49.25)]; route,method=optimize(coords); rr={'method':method,'route_indices':route,'estimated_haversine_km':round(dist(coords,route),2)}; (REPORTS/'route_optimization.json').write_text(json.dumps(rr,indent=2)); summary={'mode':'real-data' if args.real_data else 'synthetic-demo','kpis':k,'model_results':models,'clustering':cl,'route_optimization':rr,'figures':[str(x) for x in figs]}; (REPORTS/'project_summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
