"""Fisher identifiability + linear mismatch bias with the FLEXIBLE 10-parameter
inference family (2-parameter anisotropy + profile curvature).
Reconstructed verbatim from the inline run of 2026-09-02 (session artifact).
Reported results: sigma_eta full = 0.1003; no-shape-priors = 0.1702; IFU@1% = 0.0806;
biases: tanh-beta -0.0070, gamma-bump +0.0226, tracer 4% -0.0135."""
import numpy as np
from model import observables, LensDyn, RBINS

P0 = dict(s0=0.1503, gamma=2.0, s_sh=0.03, k_los=0.02, beta=0.20,
          eta=1.0, ddt=1.0, beta_s=0.10)
NAMES = ['ln_s0','gamma','gcurv','s_sh','k_los','beta','ra','eta','ln_ddt','beta_s']

def gf_make(g0, gc):
    return lambda r: g0 + gc*np.tanh(np.log(r))
def bf_make(b0, ra):
    return lambda r: b0*r**2/(r**2+ra**2)

def obs(x):
    p = dict(s0=np.exp(x[0]), gamma=x[1], s_sh=x[3], k_los=x[4],
             beta=x[5], eta=x[7], ddt=np.exp(x[8]), beta_s=x[9])
    return observables(p, gamma_func=gf_make(x[1],x[2]), beta_func=bf_make(x[5],x[6]))

x0 = np.array([np.log(0.1503), 2.0, 0.0, 0.03, 0.02, 0.35, 1.2, 1.0, 0.0, 0.10])
d0 = obs(x0)
frac = np.array([0.002,0.002,0.010,0.015]+[0.02]*8)
sig_d = np.abs(d0)*frac
PR = {'k_los':0.02,'ln_ddt':0.010,'s_sh':0.05,'ra':1.0,'gcurv':0.10}

steps = np.array([0.01,0.01,0.01,0.005,0.005,0.02,0.05,0.01,0.005,0.002])
J = np.zeros((len(d0),len(x0)))
for j in range(len(x0)):
    xp=x0.copy(); xp[j]+=steps[j]; xm=x0.copy(); xm[j]-=steps[j]
    J[:,j]=(obs(xp)-obs(xm))/(2*steps[j])

def cov_of(rows, priors=('k_los','ln_ddt','s_sh','ra','gcurv'), sd=None):
    sd = sig_d if sd is None else sd
    F=(J[rows]/sd[rows,None]).T@(J[rows]/sd[rows,None])
    for pn in priors:
        i=NAMES.index(pn); F[i,i]+=1.0/PR[pn]**2
    return np.linalg.inv(F)

ALL=np.arange(len(d0)); ie=NAMES.index('eta')
c=cov_of(ALL)
print("FLEXIBLE FAMILY (10 params):")
print("  sigma_eta full            = %.4f"%np.sqrt(c[ie,ie]))
c2=cov_of(ALL,priors=('k_los','ln_ddt','s_sh'))
print("  sigma_eta no-shape-priors = %.4f"%np.sqrt(c2[ie,ie]))
c3=cov_of(ALL, sd=np.concatenate([sig_d[:4],np.abs(d0[4:])*0.01]))
print("  sigma_eta IFU@1%%          = %.4f"%np.sqrt(c3[ie,ie]))

def bias_from(d_true, priors=('k_los','ln_ddt','s_sh','ra','gcurv')):
    delta=d_true-d0
    F=(J/sig_d[:,None]).T@(J/sig_d[:,None])
    for pn in priors:
        i=NAMES.index(pn); F[i,i]+=1.0/PR[pn]**2
    rhs=(J/sig_d[:,None]).T@(delta/sig_d)
    return np.linalg.solve(F,rhs)[ie]

p0d = dict(P0)
bf_t = lambda r: 0.2+0.25*np.tanh(np.log(r/0.5))
d1 = observables(p0d, gamma_func=gf_make(2.0,0.0), beta_func=bf_t)
print("bias: tanh-beta truth vs OM family     d_eta = %+.4f"%bias_from(d1))
gf_t = lambda r: 2.0+0.06*np.exp(-np.log(r)**2/0.5)
d2 = observables(p0d, gamma_func=gf_t, beta_func=bf_make(0.35,1.2))
print("bias: gamma-bump truth vs tanh family  d_eta = %+.4f"%bias_from(d2))

class LD2(LensDyn):
    def sigma_los(self, Rbins):
        a=0.57
        from model import R, LNR
        nu=1.0/(R*(R+a)**3); b=self.beta_func(R)
        lnI=np.concatenate([[0.0],np.cumsum(0.5*(2*b[1:]+2*b[:-1])*np.diff(LNR))])
        I=np.exp(lnI-lnI[len(lnI)//2])
        integ=I*nu*self.M/R**2*R
        tail=np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(LNR))[::-1])[::-1],[0.0]])
        nusr2=tail/I; lr=np.log(R)
        ln_ns2=np.log(np.maximum(nusr2,1e-300)); ln_nu=np.log(nu)
        out=np.empty(len(Rbins)); u=np.linspace(1e-4,8,400)
        for i,Rp in enumerate(Rbins):
            rr=Rp*np.cosh(u); lnr=np.log(rr)
            ns2=np.exp(np.interp(lnr,lr,ln_ns2)); nuv=np.exp(np.interp(lnr,lr,ln_nu))
            bb=np.interp(lnr,lr,b)
            out[i]=np.sqrt(2*np.trapezoid((1-bb*Rp**2/rr**2)*ns2*rr,u)/(2*np.trapezoid(nuv*rr,u)))
        return out
m=LD2(P0, gamma_func=gf_make(2.0,0.0), beta_func=bf_make(0.35,1.2))
thA,thB=m.images()
d3=np.concatenate([[thA,thB,m.theta_E2(),m.time_delay()],m.sigma_los(RBINS)])
print("bias: tracer scale off 4%%              d_eta = %+.4f"%bias_from(d3))
