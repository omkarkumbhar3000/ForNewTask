import io, os, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
G=1024**3
# verify-pack -v: <sha> <type> <size> <size-in-packfile> <offset> [depth base]
packed={}
for line in io.open('verifypack.txt', encoding='utf-8', errors='replace'):
    p=line.split()
    if len(p)<5 or p[1] not in ('blob','tree','commit','tag'): continue
    try: packed[p[0]]=(p[1], int(p[3]))
    except ValueError: continue
print(f"objects with on-disk size: {len(packed):,}")
tot=defaultdict(int)
for t,s in packed.values(): tot[t]+=s
for t in ('blob','tree','commit','tag'):
    print(f"  {t:7} {tot[t]/G:>8.3f} GiB on disk")
print(f"  TOTAL   {sum(tot.values())/G:>8.3f} GiB")

# map sha -> path from objsizes.txt
path={}
for line in io.open('objsizes.txt', encoding='utf-8', errors='replace'):
    q=line.rstrip('\n').split(' ',3)
    if len(q)>3 and q[0]=='blob': path[q[1]]=q[3]

byext=defaultdict(lambda:[0,0]); bybase=defaultdict(lambda:[0,0])
for sha,(t,s) in packed.items():
    if t!='blob': continue
    p=path.get(sha)
    if not p: continue
    e=os.path.splitext(p)[1].lower() or '(none)'
    byext[e][0]+=s; byext[e][1]+=1
    b=os.path.basename(p); bybase[b][0]+=s; bybase[b][1]+=1
bt=sum(v[0] for v in byext.values())
print(f"\n=== ON-DISK pack bytes by extension (authoritative) — top 12 ===")
for e,(s,n) in sorted(byext.items(), key=lambda x:-x[1][0])[:12]:
    print(f"  {s/G:>7.3f} GiB {100*s/bt:>5.1f}%  {n:>6,} versions  {e}")
print(f"\n=== ON-DISK pack bytes by filename — top 12 ===")
for b,(s,n) in sorted(bybase.items(), key=lambda x:-x[1][0])[:12]:
    print(f"  {s/G:>7.3f} GiB  {n:>5,} versions  {b[:50]}")
