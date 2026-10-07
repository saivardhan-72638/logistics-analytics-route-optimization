from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def run_clustering(d,out):
    z=d.groupby('customer_state').agg(orders=('order_id','nunique'),avg_delivery_days=('delivery_days','mean'),late_rate=('late_flag','mean'),avg_freight=('freight_value','mean')).reset_index(); cols=['orders','avg_delivery_days','late_rate','avg_freight']; X=StandardScaler().fit_transform(z[cols]); k=min(4,max(2,len(z)-1)); z['cluster']=KMeans(n_clusters=k,n_init=20,random_state=42).fit_predict(X); score=silhouette_score(X,z.cluster) if len(z)>k else None; z.to_csv(out,index=False); return {'clusters':k,'silhouette_score':round(float(score),3) if score is not None else None}
