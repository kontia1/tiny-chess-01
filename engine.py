import json,os,sys,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
VL={"p":100,"n":320,"b":330,"r":500,"q":900,"k":0}
PST={
"p":[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0],
"n":[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
"b":[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20],
"r":[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0],
"q":[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],
"k":[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]}
KD=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
BD=[(1,1),(1,-1),(-1,1),(-1,-1)]
RD=[(1,0),(-1,0),(0,1),(0,-1)]
DD={"n":KD,"b":BD,"r":RD,"q":BD+RD,"k":BD+RD}
N=0
LIM=60000
DEP=5


def P(p,b):
    q=urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
    return json.load(urllib.request.urlopen(q))


def parse(fen):
    ps=fen.split()
    b=["."]*64
    r=7
    for row in ps[0].split("/"):
        f=0
        for c in row:
            if c.isdigit():
                f+=int(c)
            else:
                b[r*8+f]=c
                f+=1
        r-=1
    ep=-1
    if ps[3]!="-":
        ep=(int(ps[3][1])-1)*8+"abcdefgh".index(ps[3][0])
    return b,1 if ps[1]=="w" else 0,ps[2],ep


def king(b,w):
    k="K" if w else "k"
    for i in range(64):
        if b[i]==k:
            return i
    return -1


def att(b,sq,w):
    if sq<0:
        return 1
    f0=sq%8
    r0=sq//8
    for df,dr in KD:
        f=f0+df
        r=r0+dr
        if 0<=f<8 and 0<=r<8:
            p=b[r*8+f]
            if p=="n" or p=="N":
                if p.isupper()==bool(w):
                    return 1
    for df,dr in BD+RD:
        f=f0+df
        r=r0+dr
        d=1
        while 0<=f<8 and 0<=r<8:
            p=b[r*8+f]
            if p!=".":
                if p.isupper()==bool(w):
                    lp=p.lower()
                    if lp=="q" or (lp=="k" and d==1) or (lp=="r" and (df==0 or dr==0)) or (lp=="b" and df!=0 and dr!=0):
                        return 1
                break
            f+=df
            r+=dr
            d+=1
    pd=-1 if w else 1
    for df in (-1,1):
        f=f0+df
        r=r0+pd
        if 0<=f<8 and 0<=r<8:
            p=b[r*8+f]
            if (p=="P" if w else p=="p"):
                return 1
    return 0


def mk2(b,m,cast,ep):
    f,t,pr=m
    b2=list(b)
    p=b2[f]
    b2[t]=pr if pr else p
    b2[f]="."
    lp=p.lower()
    ep2=-1
    if lp=="p" and t==ep and f%8!=t%8 and b[t]==".":
        b2[t+(8 if p.isupper() else -8)]="."
    if lp=="p" and abs(t-f)==16:
        ep2=(f+t)//2
    if lp=="k" and abs(t-f)==2:
        if t>f:
            b2[f+1]=b2[f+3]
            b2[f+3]="."
        else:
            b2[f-1]=b2[f-4]
            b2[f-4]="."
    c=cast
    if p=="K":
        c=c.replace("K","").replace("Q","")
    elif p=="k":
        c=c.replace("k","").replace("q","")
    if f==0 or t==0:
        c=c.replace("Q","")
    if f==7 or t==7:
        c=c.replace("K","")
    if f==56 or t==56:
        c=c.replace("q","")
    if f==63 or t==63:
        c=c.replace("k","")
    return b2,c,ep2


def gen(b,stm,cast,ep):
    ms=[]
    w=bool(stm)
    for i in range(64):
        p=b[i]
        if p=="." or p.isupper()!=w:
            continue
        lp=p.lower()
        f0=i%8
        r0=i//8
        if lp=="p":
            d=8 if w else -8
            r1=r0+(1 if w else -1)
            if 0<=r1<8 and b[i+d]==".":
                if r1==7 or r1==0:
                    for q in "qrbn":
                        ms.append((i,i+d,q))
                else:
                    ms.append((i,i+d,""))
                    if r0==(1 if w else 6) and b[i+2*d]==".":
                        ms.append((i,i+2*d,""))
            for df in (-1,1):
                f1=f0+df
                if 0<=f1<8 and 0<=r1<8:
                    t=r1*8+f1
                    q=b[t]
                    if (q!="." and q.isupper()!=w) or (t==ep and q=="."):
                        if r1==7 or r1==0:
                            for z in "qrbn":
                                ms.append((i,t,z))
                        else:
                            ms.append((i,t,""))
        else:
            for df,dr in DD[lp]:
                f=f0+df
                r=r0+dr
                while 0<=f<8 and 0<=r<8:
                    t=r*8+f
                    q=b[t]
                    if q==".":
                        ms.append((i,t,""))
                    else:
                        if q.isupper()!=w:
                            ms.append((i,t,""))
                        break
                    if lp=="n" or lp=="k":
                        break
                    f+=df
                    r+=dr
        if lp=="k":
            if w and b[4]=="K":
                if "K" in cast and b[5]=="." and b[6]=="." and b[7]=="R" and not att(b,4,0) and not att(b,5,0):
                    ms.append((4,6,""))
                if "Q" in cast and b[3]=="." and b[2]=="." and b[1]=="." and b[0]=="R" and not att(b,4,0) and not att(b,3,0):
                    ms.append((4,2,""))
            elif not w and b[60]=="k":
                if "k" in cast and b[61]=="." and b[62]=="." and b[63]=="r" and not att(b,60,1) and not att(b,61,1):
                    ms.append((60,62,""))
                if "q" in cast and b[59]=="." and b[58]=="." and b[57]=="." and b[56]=="r" and not att(b,60,1) and not att(b,59,1):
                    ms.append((60,58,""))
    return ms


def ev(b):
    s=0
    for i in range(64):
        p=b[i]
        if p==".":
            continue
        lp=p.lower()
        v=VL[lp]
        if p.isupper():
            s+=v+PST[lp][(7-i//8)*8+i%8]
        else:
            s-=v+PST[lp][i]
    return s


def order(b,ms,stm):
    o=[]
    w=bool(stm)
    for m in ms:
        c=b[m[1]]
        s=0
        if c!="." and c.isupper()!=w:
            s=VL[c.lower()]*8-VL[b[m[0]].lower()]
        if m[2]=="q":
            s+=900
        elif m[2]:
            s+=400
        o.append((-s,m))
    o.sort()
    return [m for _,m in o]


def legal(b,stm,cast,ep):
    out=[]
    for m in gen(b,stm,cast,ep):
        b2,c2,e2=mk2(b,m,cast,ep)
        k=king(b2,stm==1)
        if k>=0 and not att(b2,k,stm==0):
            out.append(m)
    return out


def qs(b,stm,cast,ep,a,bt,d):
    global N
    N+=1
    st=ev(b) if stm else -ev(b)
    if st>=bt or d<=0 or N>LIM:
        return st
    if st>a:
        a=st
    for m in order(b,[x for x in gen(b,stm,cast,ep) if b[x[1]]!="." or x[2]],stm):
        b2,c2,e2=mk2(b,m,cast,ep)
        k=king(b2,stm==1)
        if k<0 or att(b2,k,stm==0):
            continue
        v=-qs(b2,1-stm,c2,e2,-bt,-a,d-1)
        if v>=bt:
            return v
        if v>a:
            a=v
    return a


def se(b,stm,cast,ep,d,a,bt):
    global N
    N+=1
    if N>LIM:
        return ev(b) if stm else -ev(b)
    ms=gen(b,stm,cast,ep)
    ok=0
    if d<=0:
        return qs(b,stm,cast,ep,a,bt,3)
    for m in order(b,ms,stm):
        b2,c2,e2=mk2(b,m,cast,ep)
        k=king(b2,stm==1)
        if k<0 or att(b2,k,stm==0):
            continue
        ok=1
        v=-se(b2,1-stm,c2,e2,d-1,-bt,-a)
        if v>=bt:
            return v
        if v>a:
            a=v
    if not ok:
        k=king(b,stm==1)
        if k>=0 and att(b,k,stm==0):
            return -90000+d
        return 0
    return a


def choose(fen,legal_uci):
    global N
    b,stm,cast,ep=parse(fen)
    L={}
    for m in legal_uci:
        f="abcdefgh".index(m[0])+(int(m[1])-1)*8
        t="abcdefgh".index(m[2])+(int(m[3])-1)*8
        L[(f,t,m[4] if len(m)>4 else "")]=m
    keys=list(L)
    N=0
    best=keys[0]
    for d in range(1,DEP+1):
        bv=-99999
        cb=None
        for m in order(b,keys,stm):
            b2,c2,e2=mk2(b,m,cast,ep)
            v=-se(b2,1-stm,c2,e2,d-1,-99999,99999)
            if v>bv:
                bv=v
                cb=m
            if N>LIM:
                break
        if cb is not None and bv>-90000:
            best=cb
        if N>LIM or bv>90000:
            break
    return L[best]


while True:
    g=P("/game",{})
    if g["status"]=="done":
        break
    while g["status"]=="your_move":
        g=P("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
    print("game %s %s"%(g["game"],g["outcome"]),file=sys.stderr)
print("done %s %s %s"%(g.get("wins"),g.get("draws"),g.get("losses")),file=sys.stderr)
