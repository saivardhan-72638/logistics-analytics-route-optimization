import pandas as pd

def calculate_kpis(d):
    return {'total_delivered_orders':int(d.order_id.nunique()),'on_time_delivery_rate_pct':round((1-d.late_flag.mean())*100,2),'late_delivery_rate_pct':round(d.late_flag.mean()*100,2),'average_delivery_days':round(d.delivery_days.mean(),2),'median_delivery_days':round(d.delivery_days.median(),2),'average_freight_per_order':round(d.freight_value.mean(),2),'average_order_value':round(d.order_value.mean(),2),'freight_to_order_value_pct':round(d.freight_ratio.mean()*100,2),'average_review_score':round(d.review_score.mean(),2) if d.review_score.notna().any() else None}

def save_kpis(k,p): pd.DataFrame([k]).to_csv(p,index=False)
