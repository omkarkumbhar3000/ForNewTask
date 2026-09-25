import io, os, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
G=1024**3; M=1024**2
rows=[]
for line in io.open('headtree.txt', encoding='utf-8', errors='replace'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    meta, path = line.split('\t', 1)
    parts = meta.split()
    if len(parts)<4 or parts[1]!='blob': continue
    try: size=int(parts[3])
    except ValueError: continue
    rows.append((size, path, parts[2]))

tot=sum(r[0] for r in rows)
print(f"HEAD tree: {tot/G:.3f} GiB across {len(rows):,} blobs\n")

byext=defaultdict(lambda:[0,0])
for s,p,_ in rows:
    e=os.path.splitext(p)[1].lower() or '(none)'
    byext[e][0]+=s; byext[e][1]+=1
print("=== HEAD by extension (CORRECTED, tab-split) — top 14 ===")
for e,(s,n) in sorted(byext.items(), key=lambda x:-x[1][0])[:14]:
    print(f"  {s/G:>7.3f} GiB {100*s/tot:>5.1f}%  {n:>6,}  {e}")

bybase=defaultdict(lambda:[0,0,set()])
for s,p,sha in rows:
    b=os.path.basename(p)
    bybase[b][0]+=s; bybase[b][1]+=1; bybase[b][2].add(sha)
print("\n=== duplicate basenames in HEAD (CORRECTED) — top 14 by total bytes ===")
print(f"  {'total MB':>10} {'copies':>7} {'distinct':>9}  name")
for b,(s,n,shas) in sorted(bybase.items(), key=lambda x:-x[1][0])[:14]:
    if n<2: continue
    print(f"  {s/M:>10.1f} {n:>7} {len(shas):>9}  {b[:52]}")

waste=sum(s-(s/n) for b,(s,n,_) in bybase.items() if n>1)
identical=sum(s-(s/n) for b,(s,n,shas) in bybase.items() if n>1 and len(shas)==1)
print(f"\n  redundant bytes from duplicate basenames : {waste/G:.2f} GiB")
print(f"  ...of which byte-identical (git dedups in .git): {identical/G:.2f} GiB")

for ext in ('.mp4','.db','.bak','.zip','.exe','.dll','.msi','.cs'):
    m=[r for r in rows if r[1].lower().endswith(ext)]
    print(f"  {ext:<6} {sum(x[0] for x in m)/G:>8.3f} GiB  {len(m):>6,} files")
