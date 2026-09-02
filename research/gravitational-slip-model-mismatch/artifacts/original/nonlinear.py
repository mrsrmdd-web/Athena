import numpy as np, json, time, sys
from scipy.optimize import least_squares
from model import observables, LensDyn, RBINS, R, LNR

NAMES = ['ln_s0','gamma','gcurv','s_sh','k_los','b0','ra','eta','ln_ddt','beta_s']
LO = np.array([-3.0, 1.5, -0.3, -0.05, -0.1, -0.5, 0.3, 0.5, -0.2, 0.01])
HI = np.array([ 0.0, 2.5,  0.3,  0.30,  0.2,  0.8, 5.0, 1.5,  0.2, 0.30])
GAUSS = {'k_los':(0.0,0.02), 'ln_ddt':(0.0,0.01), 's_sh':(0.0,0.05)}

def gf_make(g0, gc): return lambda r: g0 + gc*np.tanh(np.log(r))
def bf_make(b0, ra): return lambda r: b0*r**2/(r**2+ra**2)

def forward(x, tracer_a=0.55):
    p = dict(s0=np.exp(x[0]), gamma=x[1], s_sh=x[3], k_los=x[4],
             beta=x[5], eta=x[7], ddt=np.exp(x[8]), beta_s=x[9])
    return observables(p, gamma_func=gf_make(x[1],x[2]), beta_func=bf_make(x[5],x[6]))

# ---- truth generators ----
def truth_outside(eta):
    """gamma bump + tanh anisotropy + tracer a=0.57: none in inference family."""
    p = dict(s0=0.1503, gamma=2.0, s_sh=0.03, k_los=0.02, beta=0.2, eta=eta, ddt=1.0, beta_s=0.10)
    gf = lambda r: 2.0 + 0.06*np.exp(-np.log(r)**2/0.5)
    bf = lambda r: 0.2 + 0.25*np.tanh(np.log(r/0.5))
    m = LensDyn(p, gamma_func=gf, beta_func=bf)
    # tracer with a=0.57
    a = 0.57
    nu = 1.0/(R*(R+a)**3); b = bf(R)
    lnI = np.concatenate([[0.0], np.cumsum(0.5*(2*b[1:]+2*b[:-1])*np.diff(LNR))]); I = np.exp(lnI-lnI[len(lnI)//2])
    integ = I*nu*m.M/R**2*R
    tail = np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(LNR))[::-1])[::-1],[0.0]])
    nusr2 = tail/I; lr = np.log(R); lns2 = np.log(np.maximum(nusr2,1e-300)); lnnu = np.log(nu)
    u = np.linspace(1e-4,8,400); sig = np.empty(len(RBINS))
    for i,Rp in enumerate(RBINS):
        rr = Rp*np.cosh(u); lnr = np.log(rr)
        ns2 = np.exp(np.interp(lnr,lr,lns2)); nuv = np.exp(np.interp(lnr,lr,lnnu)); bb = np.interp(lnr,lr,b)
        sig[i] = np.sqrt(np.trapezoid((1-bb*Rp**2/rr**2)*ns2*rr,u)/np.trapezoid(nuv*rr,u))
    thA,thB = m.images()
    return np.concatenate([[thA,thB,m.theta_E2(),m.time_delay()],sig])

def truth_inside(eta):
    x = np.array([np.log(0.1503),2.0,0.0,0.03,0.02,0.35,1.2,eta,0.0,0.10])
    return forward(x)

FRAC = np.array([0.002,0.002,0.010,0.015]+[0.02]*8)

def lnpost(x, d, sd):
    if np.any(x<LO) or np.any(x>HI): return -np.inf
    try: m = forward(x)
    except Exception: return -np.inf
    if not np.all(np.isfinite(m)): return -np.inf
    lp = -0.5*np.sum(((m-d)/sd)**2)
    for k,(mu,s) in GAUSS.items():
        lp += -0.5*((x[NAMES.index(k)]-mu)/s)**2
    lp += -np.log(x[6])   # log-uniform on ra
    return lp

def resid(x, d, sd):
    if np.any(x<LO) or np.any(x>HI): return np.full(len(d)+3, 1e3)
    try: m = forward(x)
    except Exception: return np.full(len(d)+3, 1e3)
    r = list((m-d)/sd)
    for k,(mu,s) in GAUSS.items(): r.append((x[NAMES.index(k)]-mu)/s)
    return np.array(r)

X_INIT = np.array([np.log(0.15),2.0,0.0,0.03,0.02,0.3,1.2,1.0,0.0,0.10])

def map_fit(d, sd, rng, nstart=3):
    best=None
    for k in range(nstart):
        x0 = X_INIT.copy()
        if k>0: x0 = x0 + rng.normal(0,1,10)*np.array([0.05,0.05,0.05,0.02,0.01,0.15,0.5,0.1,0.005,0.02])
        x0 = np.clip(x0, LO+1e-3, HI-1e-3)
        try:
            r = least_squares(resid, x0, args=(d,sd), method='trf', bounds=(LO,HI), x_scale='jac', max_nfev=400)
        except Exception: continue
        if best is None or r.cost<best.cost: best=r
    J = best.jac
    cov = np.linalg.pinv(J.T@J)
    return best.x, cov, best.cost

def stretch_mcmc(lnp, x0, nwalk, nstep, rng, a=2.0):
    ndim = len(x0)
    walkers = x0 + rng.normal(0,1,(nwalk,ndim))*np.array([0.02,0.02,0.03,0.01,0.005,0.08,0.3,0.05,0.003,0.005])
    walkers = np.clip(walkers, LO+1e-4, HI-1e-4)
    lp = np.array([lnp(w) for w in walkers])
    chain = np.empty((nstep,nwalk,ndim)); acc=0
    half = nwalk//2
    for s in range(nstep):
        for grp in (slice(0,half), slice(half,nwalk)):
            other = walkers[slice(half,nwalk)] if grp.start==0 else walkers[slice(0,half)]
            idx = np.arange(nwalk)[grp]
            for i in idx:
                j = rng.integers(len(other))
                z = ((a-1)*rng.random()+1)**2/a
                prop = other[j] + z*(walkers[i]-other[j])
                lpp = lnp(prop)
                if np.log(rng.random()) < (ndim-1)*np.log(z) + lpp - lp[i]:
                    walkers[i]=prop; lp[i]=lpp; acc+=1
        chain[s]=walkers
        if s%100==0: print("  step",s,"acc %.2f"%(acc/((s+1)*nwalk)), "eta med %.3f"%np.median(chain[max(0,s-100):s+1,:,7]), flush=True)
    return chain, acc/(nstep*nwalk)

if __name__=="__main__":
    mode = sys.argv[1]
    rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 1)
    out = {}
    if mode=="mcmc":
        cases = [("inside",1.00),("outside",1.00),("outside",0.98),("outside",0.95),("outside",0.90)]
        for fam,eta in cases:
            d_true = truth_inside(eta) if fam=="inside" else truth_outside(eta)
            sd = np.abs(d_true)*FRAC
            d = d_true + rng.normal(0,1,len(d_true))*sd
            t=time.time()
            xm, cov, cost = map_fit(d, sd, rng, nstart=4)
            print(f"[{fam} eta={eta}] MAP eta={xm[7]:.4f} +- {np.sqrt(cov[7,7]):.4f} chi2={2*cost:.1f}", flush=True)
            chain, acc = stretch_mcmc(lambda x: lnpost(x,d,sd), xm, nwalk=20, nstep=900, rng=rng)
            post = chain[300:].reshape(-1,10)
            q = np.percentile(post[:,7],[16,50,84])
            out[f"{fam}_{eta}"] = dict(inj=eta, map=float(xm[7]), lap_sig=float(np.sqrt(cov[7,7])),
                p16=float(q[0]),p50=float(q[1]),p84=float(q[2]), acc=float(acc), chi2=float(2*cost),
                corr_eta=[float(np.corrcoef(post[:,7],post[:,k])[0,1]) for k in range(10)],
                time=time.time()-t)
            print("   posterior eta = %.4f (+%.4f/-%.4f)  acc=%.2f  %.0fs"%(q[1],q[2]-q[1],q[1]-q[0],acc,time.time()-t), flush=True)
            json.dump(out, open("mcmc_results.json","w"), indent=1)
    elif mode=="coverage":
        NREAL = 30
        for eta in [1.00, 0.98, 0.95]:
            d_true = truth_outside(eta); sd = np.abs(d_true)*FRAC
            ests=[]; sigs=[]
            for k in range(NREAL):
                d = d_true + rng.normal(0,1,len(d_true))*sd
                xm,cov,cost = map_fit(d,sd,rng,nstart=2)
                ests.append(xm[7]); sigs.append(np.sqrt(cov[7,7]))
                if k%10==0: print(f" eta={eta} real {k}: {xm[7]:.3f}+-{np.sqrt(cov[7,7]):.3f}", flush=True)
            ests=np.array(ests); sigs=np.array(sigs)
            z = (ests-eta)/sigs
            out[str(eta)] = dict(inj=eta, mean=float(ests.mean()), scatter=float(ests.std()), mean_sig=float(sigs.mean()),
                bias=float(ests.mean()-eta), cov68=float(np.mean(np.abs(z)<1)), cov95=float(np.mean(np.abs(z)<2)),
                claim_rate=float(np.mean(np.abs(ests-1.0)>2*sigs)))
            print(out[str(eta)], flush=True)
            json.dump(out, open("coverage_results.json","w"), indent=1)
