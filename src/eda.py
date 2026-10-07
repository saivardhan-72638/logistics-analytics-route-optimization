import matplotlib.pyplot as plt

def run_eda(d,out):
    out.mkdir(parents=True,exist_ok=True); paths=[]
    specs=[('delivery_time_distribution.png',lambda ax:(ax.hist(d.delivery_days,bins=30),ax.set_title('Delivery Time Distribution'),ax.set_xlabel('Delivery days'),ax.set_ylabel('Orders'))),('freight_vs_order_value.png',lambda ax:(ax.scatter(d.order_value,d.freight_value,alpha=.25),ax.set_title('Freight Cost vs Order Value'),ax.set_xlabel('Order value'),ax.set_ylabel('Freight value')))]
    for fn,draw in specs:
        fig,ax=plt.subplots(figsize=(9,5)); draw(ax); fig.tight_layout(); p=out/fn; fig.savefig(p,dpi=150); plt.close(fig); paths.append(p)
    s=d.groupby('customer_state').late_flag.mean().sort_values(ascending=False).head(10)*100; fig,ax=plt.subplots(figsize=(9,5)); s.sort_values().plot.barh(ax=ax); ax.set_title('Highest Late-Delivery Rates by State'); ax.set_xlabel('Late rate (%)'); fig.tight_layout(); p=out/'late_rate_by_state.png'; fig.savefig(p,dpi=150); plt.close(fig); paths.append(p)
    m=d.groupby('purchase_month').late_flag.mean()*100; fig,ax=plt.subplots(figsize=(11,5)); m.plot(ax=ax,marker='o'); ax.set_title('Monthly Late-Delivery Rate'); ax.set_ylabel('Late rate (%)'); ax.tick_params(axis='x',rotation=45); fig.tight_layout(); p=out/'monthly_late_rate.png'; fig.savefig(p,dpi=150); plt.close(fig); paths.append(p)
    return paths
