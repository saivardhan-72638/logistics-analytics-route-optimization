from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; RAW.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(42); n=2500
states=np.array(['SP','RJ','MG','PR','BA','RS','SC','GO','PE','CE']); cities=np.array(['Sao Paulo','Rio de Janeiro','Belo Horizonte','Curitiba','Salvador','Porto Alegre','Florianopolis','Goiania','Recife','Fortaleza']); ids=[f'order_{i:06d}' for i in range(n)]; cust=[f'cust_{i:06d}' for i in range(n)]
purchase=pd.to_datetime('2017-01-01')+pd.to_timedelta(rng.integers(0,730,n),unit='D')+pd.to_timedelta(rng.integers(0,86400,n),unit='s'); state=rng.choice(states,n,p=[.28,.12,.12,.1,.08,.08,.07,.06,.05,.04]); est_days=rng.gamma(2.2,2,n)+2; estimated=purchase+pd.to_timedelta(est_days,unit='D'); delay=rng.normal(0,2.3,n)+np.where(np.isin(state,['BA','PE','CE']),1.2,0); actual=estimated+pd.to_timedelta(delay,unit='D')
orders=pd.DataFrame({'order_id':ids,'customer_id':cust,'order_status':'delivered','order_purchase_timestamp':purchase,'order_approved_at':purchase+pd.to_timedelta(rng.integers(1,24,n),unit='h'),'order_delivered_carrier_date':purchase+pd.to_timedelta(rng.integers(1,4,n),unit='D'),'order_delivered_customer_date':actual,'order_estimated_delivery_date':estimated}); customers=pd.DataFrame({'customer_id':cust,'customer_zip_code_prefix':rng.integers(10000,99999,n),'customer_city':rng.choice(cities,n),'customer_state':state})
rows=[]
for i,oid in enumerate(ids):
 k=int(rng.integers(1,4))
 for j in range(k): rows.append((oid,j+1,f'prod_{rng.integers(1,400):05d}',f'seller_{rng.integers(1,180):05d}',round(float(rng.lognormal(3.3,.65)),2),round(float(rng.lognormal(2,.55)),2)))
items=pd.DataFrame(rows,columns=['order_id','order_item_id','product_id','seller_id','price','freight_value']); reviews=pd.DataFrame({'order_id':ids,'review_score':np.clip(np.rint(4-delay*.35+rng.normal(0,.8,n)),1,5).astype(int)})
for n_,df in [('olist_orders_dataset.csv',orders),('olist_customers_dataset.csv',customers),('olist_order_items_dataset.csv',items),('olist_order_reviews_dataset.csv',reviews)]: df.to_csv(RAW/n_,index=False)
print(f'Generated {n:,} synthetic orders and {len(items):,} item rows.')
