import numpy as np
from model import observables, LensDyn, RBINS

# ---------------- fiducial ----------------
P0 = dict(s0=0.32, gamma=2.0, s_sh=0.03, k_los=0.02, beta=0.20,
          eta=1.0, ddt=1.0, beta_s=0.10)
NAMES = ['ln_s0','gamma','s_sh','k_los','beta','eta','ln_ddt','beta_s']

# calibrate s0 so theta_E1 ~ 1 (images near +-1)
from scipy.optimize import brentq
def thE1_of_s0(s0):
    p = dict(P0); p['s0']=s0; p['beta_s']=1e-4
    m = LensDyn(p)
    a,b = m.images()
    return a-1.0
P0['s0'] = brentq(thE1_of_s0, 0.05, 0.4, xtol=1e-6)
print("calibrated s0 =", round(P0['s0'],4))

def pack(p):
    return np.array([np.log(p['s0']), p['gamma'], p['s_sh'], p['k_los'],
                     p['beta'], p['eta'], np.log(p['ddt']), p['beta_s']])
def unpack(x):
    return dict(s0=np.exp(x[0]), gamma=x[1], s_sh=x[2], k_los=x[3],
                beta=x[4], eta=x[5], ddt=np.exp(x[6]), beta_s=x[7])

x0 = pack(P0)
d0 = observables(P0)
print("fiducial obs:", np.round(d0,4))

# ---------------- error model ----------------
# [thA, thB, thE2, dt, sig x8]; fractional except positions treated fractional too
frac = np.array([0.002, 0.002, 0.010, 0.015] + [0.02]*8)
sig_d = np.abs(d0)*frac
# priors as pseudo-observations: k_los ~ +/-0.02 (abs), ln_ddt ~ +/-0.01,
# s_sh weak physical prior +/-0.05 (abs)
PRIORS = {'k_los':0.02, 'ln_ddt':0.010, 's_sh':0.05}

steps = np.array([0.01, 0.01, 0.005, 0.005, 0.02, 0.01, 0.005, 0.002])
J = np.zeros((len(d0), len(x0)))
for j in range(len(x0)):
    xp = x0.copy(); xp[j] += steps[j]
    xm = x0.copy(); xm[j] -= steps[j]
    J[:, j] = (observables(unpack(xp)) - observables(unpack(xm)))/(2*steps[j])

def fisher_cov(rows, use_priors=('k_los','ln_ddt','s_sh'), extra_sig=None):
    sd = sig_d if extra_sig is None else extra_sig
    F = (J[rows]/sd[rows,None]).T @ (J[rows]/sd[rows,None])
    for pn in use_priors:
        i = NAMES.index(pn)
        F[i,i] += 1.0/PRIORS[pn]**2
    return np.linalg.inv(F)

ALL = np.arange(len(d0))
cov = fisher_cov(ALL)
i_eta = NAMES.index('eta')
print("\n=== FULL CONFIG (2 src planes + dt + 8-bin IFU + priors) ===")
print("sigma_eta = %.4f" % np.sqrt(cov[i_eta,i_eta]))
corr = cov/np.sqrt(np.outer(np.diag(cov),np.diag(cov)))
for k,n in enumerate(NAMES):
    if n!='eta':
        print("  corr(eta,%s) = %+.2f" % (n, corr[i_eta,k]))

# ---------------- ablations ----------------
def report(label, rows, priors=('k_los','ln_ddt','s_sh'), extra_sig=None):
    try:
        c = fisher_cov(rows, priors, extra_sig)
        print("%-38s sigma_eta = %.4f" % (label, np.sqrt(c[i_eta,i_eta])))
        return np.sqrt(c[i_eta,i_eta])
    except np.linalg.LinAlgError:
        print("%-38s NOT IDENTIFIABLE (singular)" % label)
        return np.inf

print("\n=== ABLATIONS ===")
report("full", ALL)
report("- time delay", np.array([0,1,2]+list(range(4,12))))
report("- 2nd source plane", np.array([0,1,3]+list(range(4,12))))
report("- dt AND 2nd plane (SLACS-like)", np.array([0,1]+list(range(4,12))))
# single aperture dispersion instead of resolved IFU
sig_ap = sig_d.copy(); rows_ap = np.array([0,1,2,3,7])  # keep one sigma bin
sig_ap[7] = d0[7]*0.03
report("- resolved IFU -> 1 aperture @3%", rows_ap, extra_sig=sig_ap)
report("- k_los prior removed", ALL, priors=('ln_ddt','s_sh'))
report("- ddt prior removed", ALL, priors=('k_los','s_sh'))
report("- s_sh prior removed", ALL, priors=('k_los','ln_ddt'))
report("IFU at 1% (systematics-free dream)", ALL,
       extra_sig=np.concatenate([sig_d[:4], np.abs(d0[4:])*0.01]))

# ---------------- mismatch bias injections ----------------
print("\n=== MODEL-MISMATCH BIAS (truth != inference family) ===")
def bias_from(d_true, rows=ALL, priors=('k_los','ln_ddt','s_sh')):
    delta = d_true - d0
    sd = sig_d
    F = (J[rows]/sd[rows,None]).T @ (J[rows]/sd[rows,None])
    for pn in priors:
        i = NAMES.index(pn); F[i,i] += 1.0/PRIORS[pn]**2
    rhs = (J[rows]/sd[rows,None]).T @ (delta[rows]/sd[rows])
    dp = np.linalg.solve(F, rhs)
    return dp[i_eta]

# (1) Osipkov-Merritt anisotropy gradient, truth beta(r)=r^2/(r^2+ra^2), ra=1.5
bf = lambda r: r**2/(r**2 + 1.5**2)
d_om = observables(P0, beta_func=bf)
print("beta(r) OM gradient (fit const beta):  d_eta = %+.4f" % bias_from(d_om))

# (2) mild non-power-law: gamma(r) = 2 - 0.08 tanh(ln r)
gf = lambda r: 2.0 - 0.08*np.tanh(np.log(r))
p2 = dict(P0)
d_gr = observables(p2, gamma_func=gf)
print("gamma(r) curvature +-0.08 (fit PL):    d_eta = %+.4f" % bias_from(d_gr))

# (3) k_los truth 0.01 off the prior center
p3 = dict(P0); p3['k_los'] = 0.03
d_kl = observables(p3)
print("k_los off by 0.01 vs prior center:     d_eta = %+.4f" % bias_from(d_kl))

# (4) tracer profile wrong: a=0.75 truth vs 0.55 assumed -> emulate via sigma shift
import model as M
M_a_backup = None
# quick hack: recompute sigma with different tracer scale by monkeypatching
import types
def sigma_los_a(self, Rbins, a=0.75):
    import numpy as np
    from model import R, LNR
    nu = 1.0/(R*(R+a)**3)
    b = self.beta_func(R)
    lnI = np.concatenate([[0.0], np.cumsum(0.5*(2*b[1:]+2*b[:-1])*np.diff(LNR))])
    I = np.exp(lnI - lnI[len(lnI)//2])
    integ = I*nu*self.M/R**2 * R
    tail = np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(LNR))[::-1])[::-1],[0.0]])
    nusr2 = tail/I
    lr = np.log(R)
    ln_nusr2 = np.log(np.maximum(nusr2,1e-300)); ln_nu = np.log(nu)
    out = np.empty(len(Rbins)); u = np.linspace(1e-4,8,400)
    for i,Rp in enumerate(Rbins):
        rr = Rp*np.cosh(u); lnr = np.log(rr)
        ns2 = np.exp(np.interp(lnr,lr,ln_nusr2)); nuv = np.exp(np.interp(lnr,lr,ln_nu))
        bb = np.interp(lnr, lr, b)
        num = 2*np.trapezoid((1-bb*Rp**2/rr**2)*ns2*rr, u)
        den = 2*np.trapezoid(nuv*rr, u)
        out[i] = np.sqrt(num/den)
    return out
m4 = LensDyn(P0)
sig4 = sigma_los_a(m4, RBINS)
d_tr = d0.copy(); d_tr[4:] = sig4
print("tracer light profile mis-modeled:      d_eta = %+.4f" % bias_from(d_tr))
