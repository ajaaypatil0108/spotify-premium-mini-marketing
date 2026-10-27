# All figures are illustrative assumptions for a strategy exercise.
BUDGET = 50_00_000  # ₹50 lakh
alloc = [  # channel, share, role
 ("Instagram & Facebook (Reels, Stories)", .30, "Reach + retargeting"),
 ("YouTube (Shorts, pre-roll)", .20, "Reach + video storytelling"),
 ("Creator partnerships", .20, "Credibility with students"),
 ("Google Search & App campaigns", .15, "Capture high-intent searches"),
 ("Creative production & A/B tests", .05, "Assets, variants"),
 ("CRM & in-app (push, email, banners)", .05, "Upsell existing free users"),
 ("Reserve for festive bursts", .05, "Holi, IPL, summer travel"),
]
assert abs(sum(s for _,s,_ in alloc)-1)<1e-9
working = sum(BUDGET*s for n,s,_ in alloc[:4])
CPM = 100  # ₹ per 1,000 impressions, blended assumption
scen = {"Bear":(0.005,0.50,0.05),"Base":(0.008,0.60,0.08),"Bull":(0.012,0.70,0.12)}
# Unit economics per first-time payer (gross, before royalties/fees)
weekly, monthly = 25, 119
passes = 3; upg = 0.10; months = 6
rev = passes*weekly + upg*monthly*months
out={}
for k,(ctr,lp,cr) in scen.items():
    imp = working/CPM*1000; clicks=imp*ctr; views=clicks*lp; buyers=views*cr
    cpa = working/buyers
    out[k]=dict(imp=imp,clicks=clicks,views=views,buyers=buyers,cpa=cpa,rev=buyers*rev)
if __name__=="__main__":
    for n,s,r in alloc: print(f"{n:42s} {s:4.0%} ₹{BUDGET*s/1e5:5.1f}L")
    print("working media ₹",working/1e5,"L")
    print("rev per payer",rev, " per-day monthly",monthly/30," per-day weekly",weekly/7, " 30 days via weekly", weekly*30/7)
    for k,v in out.items(): print(k,{a:round(b) for a,b in v.items()})
