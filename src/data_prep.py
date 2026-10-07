import pandas as pd

def load_olist(raw):
    fs={k:raw/v for k,v in {'orders':'olist_orders_dataset.csv','items':'olist_order_items_dataset.csv','customers':'olist_customers_dataset.csv','reviews':'olist_order_reviews_dataset.csv'}.items()}
    miss=[p.name for p in fs.values() if not p.exists()]
    if miss: raise FileNotFoundError('Missing Olist files: '+', '.join(miss))
    return tuple(pd.read_csv(fs[k]) for k in ['orders','items','customers','reviews'])

def build_order_table(orders,items,customers,reviews):
    for c in ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']:
        if c in orders: orders[c]=pd.to_datetime(orders[c],errors='coerce')
    ia=items.groupby('order_id',as_index=False).agg(order_value=('price','sum'),freight_value=('freight_value','sum'),item_count=('order_item_id','count'),seller_count=('seller_id','nunique'))
    df=orders.merge(ia,on='order_id',how='left').merge(customers[['customer_id','customer_zip_code_prefix','customer_city','customer_state']],on='customer_id',how='left')
    if reviews is not None and 'review_score' in reviews: df=df.merge(reviews.groupby('order_id',as_index=False).agg(review_score=('review_score','mean')),on='order_id',how='left')
    else: df['review_score']=pd.NA
    d=df[(df.order_status=='delivered') & df.order_delivered_customer_date.notna()].copy()
    d['delivery_days']=(d.order_delivered_customer_date-d.order_purchase_timestamp).dt.total_seconds()/86400
    d['estimated_days']=(d.order_estimated_delivery_date-d.order_purchase_timestamp).dt.total_seconds()/86400
    d['late_flag']=(d.order_delivered_customer_date>d.order_estimated_delivery_date).astype(int)
    d['freight_ratio']=d.freight_value/d.order_value.replace(0,pd.NA)
    d['purchase_month']=d.order_purchase_timestamp.dt.to_period('M').astype(str)
    d['purchase_weekday']=d.order_purchase_timestamp.dt.day_name()
    return d[d.delivery_days>=0].copy()
