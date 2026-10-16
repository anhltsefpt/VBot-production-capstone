# (tier, tasks/person/day, turns/task)
common=[(1,2.97,2),(1,1.61,1),(1,1.20,2),(2,0.40,3),(2,0.075,3)]
lead_common=[(1,2.97,2),(1,1.61,1),(1,1.20,2),(2,0.92,3),(2,0.075,3)]
D={
'Kinh doanh, CSKH':(500,common+[(3,0.10,4),(4,0.10,2),(5,0.03,3)]),
'Kế toán':(240,common+[(3,0.80,4),(3,0.30,1),(4,0.05,2)]),
'Nhân sự, HC, pháp chế':(260,common+[(1,0.09,2),(2,0.15,3),(3,0.08,4),(4,0.05,2)]),
'Marketing':(200,common+[(1,0.80,2),(5,0.25,3),(3,0.12,4),(4,0.075,2)]),
'Quản lý dự án, vận hành':(300,common+[(4,0.90,2),(4,0.10,3),(5,0.08,3),(3,0.12,4)]),
'Mua hàng, SCM':(200,common+[(3,0.56,4),(4,0.05,2)]),
'IT':(200,common+[(3,0.16,8),(3,0.08,2),(1,0.60,2),(4,0.20,2),(5,0.05,3)]),
'Lãnh đạo, trợ lý':(100,lead_common+[(4,0.92,1),(4,0.20,2),(2,0.10,3)]),
}
tot=[0]*6; turns=[0]*6; people=0
for k,(n,rows) in D.items():
    s=sum(r[1] for r in rows); people+=n
    print(f"{k}: {s:.2f}/người, {s*n:,.0f}/phòng")
    for t,v,tu in rows: tot[t]+=v*n; turns[t]+=v*tu*n
T=sum(tot); TU=sum(turns)
print("people",people,"tasks/day",round(T),"per person",round(T/people,2),"tasks/month",round(T*22))
print("turns/day",round(TU),"turns/person",round(TU/people,2))
for t in range(1,6): print(f"T{t}: tasks {tot[t]:.0f} ({tot[t]/T*100:.1f}%), turns {turns[t]:.0f} ({turns[t]/TU*100:.1f}%)")
for p in (.12,.15,.20): print(f"peak {p}: {T*p:.0f} tasks/h = {T*p/3600:.2f}/s; turns {TU*p/3600:.2f}/s")
