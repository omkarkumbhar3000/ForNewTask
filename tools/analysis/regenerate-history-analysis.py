import io, sys, os, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blobs=[]   # (size, path, sha)
tot={'blob':0,'tree':0,'commit':0,'tag':0}
cnt=defaultdict(int)
seen_sha={}
for line in io.open('objsizes.txt', encoding='utf-8', errors='replace'):
    parts=line.rstrip('\n').split(' ', 3)
    if len(parts)<3: continue
    typ, sha, size = parts[0], parts[1], parts[2]
    path = parts[3] if len(parts)>3 else ''
    try: size=int(size)
    except ValueError: continue
    tot[typ]=tot.get(typ,0)+size
    cnt[typ]+=1
    if typ=='blob':
        blobs.append((size, path, sha))
        seen_sha[sha]=size

G=1024**3; M=1024**2
print("=== OBJECT TOTALS (uncompressed logical bytes) ===")
for t in ('blob','tree','commit','tag'):
    print(f"  {t:7} {cnt[t]:>8,} objects   {tot.get(t,0)/G:>9.2f} GiB")
uniq=sum(seen_sha.values())
print(f"  distinct blob SHAs: {len(seen_sha):,}  totalling {uniq/G:.2f} GiB (git stores each once)")
print(f"  blob path-entries : {len(blobs):,} (a blob reachable at N paths/commits counts N times here)")

print("\n=== TOP 30 LARGEST BLOB VERSIONS IN HISTORY ===")
for s,p,sha in sorted(blobs, reverse=True)[:30]:
    print(f"  {s/M:>9.1f} MB  {p[:100]}")

# aggregate by extension over DISTINCT blobs (dedup by sha+path)
byext=defaultdict(lambda:[0,0])
bypath=defaultdict(lambda:[0,0])
bybase=defaultdict(lambda:[0,0,set()])
uniqpairs=set()
for s,p,sha in blobs:
    if (sha,p) in uniqpairs: continue
    uniqpairs.add((sha,p))
    ext=os.path.splitext(p)[1].lower() or '(none)'
    byext[ext][0]+=s; byext[ext][1]+=1
    top=p.split('/')[1] if p.startswith('PAM/') and p.count('/')>1 else (p.split('/')[0] or '(root)')
    bypath[top][0]+=s; bypath[top][1]+=1
    b=os.path.basename(p)
    bybase[b][0]+=s; bybase[b][1]+=1; bybase[b][2].add(sha)

print("\n=== HISTORY BYTES BY EXTENSION (distinct sha+path versions) — top 22 ===")
print(f"  {'ext':<12} {'GiB':>8} {'%':>6} {'versions':>10}")
tots=sum(v[0] for v in byext.values())
for e,(s,n) in sorted(byext.items(), key=lambda x:-x[1][0])[:22]:
    print(f"  {e:<12} {s/G:>8.2f} {100*s/tots:>5.1f}% {n:>10,}")

print("\n=== HISTORY BYTES BY TOP-LEVEL AREA — top 15 ===")
for e,(s,n) in sorted(bypath.items(), key=lambda x:-x[1][0])[:15]:
    print(f"  {s/G:>8.2f} GiB  {n:>8,} versions  {e[:60]}")

print("\n=== WORST CHURN: one filename, many distinct content versions — top 25 ===")
print(f"  {'GiB':>7} {'vers':>6} {'distinct':>9}  filename")
for b,(s,n,shas) in sorted(bybase.items(), key=lambda x:-x[1][0])[:25]:
    print(f"  {s/G:>7.2f} {n:>6,} {len(shas):>9,}  {b[:64]}")

json.dump({'blob_gib':tot['blob']/G,'distinct_blob_gib':uniq/G,
           'counts':{k:cnt[k] for k in cnt}}, io.open('an_summary.json','w'))
