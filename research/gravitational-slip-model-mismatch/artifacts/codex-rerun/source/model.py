"""
Reduced-order same-object gravitational-slip identifiability model.

Physics conventions:
- Dynamics (non-relativistic tracers) feel Psi:  M_dyn(r) from rho(r).
- Lensing/photons feel (Phi+Psi)/2 = Psi*(1+eta)/2 for constant slip eta.
- Internal near-uniform component s_sh (e.g. large-core halo term): visible
  to lensing as a sheet, negligible force on kinematic-aperture tracers
  (worst-case internal mass-sheet realization).
- External LOS convergence k_los: lensing-sector only, scales with lensing
  efficiency ratio f2 for the second source plane.
- Time delay: Fermat potential * ddt (time-delay distance, external
  cosmology prior).

Units: theta_E1 ~ 1, Sigma_cr,1 = 1, G absorbed. Fractional errors only.
"""
import numpy as np

LNR = np.linspace(-8.0, 8.0, 2200)   # ln r grid
R = np.exp(LNR)

def rho_of(gamma_func, s0):
    """rho(r) = s0 * exp(-int gamma dlnr), normalized rho(1)=s0."""
    g = gamma_func(R)
    lnrho = -np.concatenate([[0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(LNR))])
    i1 = np.searchsorted(LNR, 0.0)
    lnrho = lnrho - lnrho[i1]
    return s0*np.exp(lnrho)

def mass_of(rho):
    """M(r) = 4 pi int rho r^2 dr  (dr = r dlnr)."""
    integrand = 4*np.pi*rho*R**3
    m = np.concatenate([[0.0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(LNR))])
    return m

def sigma_proj(rho, Rp):
    """Sigma(Rp) = 2 int_0^inf rho(sqrt(Rp^2+z^2)) dz, z = Rp sinh u."""
    u = np.linspace(0, 12, 500)
    out = np.empty_like(Rp)
    lr = np.log(R)
    lrho = np.log(np.maximum(rho, 1e-300))
    for i, rp in enumerate(Rp):
        rr = rp*np.cosh(u)
        f = np.exp(np.interp(np.log(rr), lr, lrho))*rp*np.cosh(u)
        out[i] = 2*np.trapezoid(f, u)
    return out

class LensDyn:
    def __init__(self, p, gamma_func=None, beta_func=None):
        # p: dict with s0, gamma, s_sh, k_los, beta, eta, ddt, beta_s
        self.p = p
        gf = gamma_func if gamma_func else (lambda r: np.full_like(r, p['gamma']))
        self.rho = rho_of(gf, p['s0'])
        self.M = mass_of(self.rho)
        self.beta_func = beta_func if beta_func else (lambda r: np.full_like(r, p['beta']))
        # lensing effective Sigma on theta grid
        self.thg = np.logspace(-2.5, 1.2, 420)
        Sd = sigma_proj(self.rho, self.thg)
        fac = 0.5*(1.0+p['eta'])
        self.Sig_L = fac*(Sd + p['s_sh'])          # slip applies to all metric-sourcing mass
        # kbar(theta) = 2/theta^2 int Sig_L t dt   (+ k_los outside integral, const)
        cum = np.concatenate([[0.0], np.cumsum(0.5*(self.Sig_L[1:]*self.thg[1:]+self.Sig_L[:-1]*self.thg[:-1])*np.diff(self.thg))])
        self.kbar1 = 2*cum/self.thg**2 + p['k_los']
        self.alpha1 = self.thg*self.kbar1
        self.psi1 = np.concatenate([[0.0], np.cumsum(0.5*(self.alpha1[1:]+self.alpha1[:-1])*np.diff(self.thg))])

    def _interp(self, x, xg, yg):
        return np.interp(x, xg, yg)

    def images(self):
        """Solve theta - alpha(theta) = beta_s on both sides."""
        bs = self.p['beta_s']
        f = self.thg - self.alpha1 - bs      # positive side
        # positive image: outermost sign change
        s = np.where(np.diff(np.sign(f)))[0]
        iA = s[-1]
        thA = self.thg[iA] - f[iA]*(self.thg[iA+1]-self.thg[iA])/(f[iA+1]-f[iA])
        g = -self.thg + self.alpha1 - bs     # negative-side image at -theta
        s2 = np.where(np.diff(np.sign(g)))[0]
        iB = s2[-1]
        thB = self.thg[iB] - g[iB]*(self.thg[iB+1]-self.thg[iB])/(g[iB+1]-g[iB])
        return thA, -thB

    def theta_E2(self, f2=1.35):
        kb2 = f2*(self.kbar1 - self.p['k_los']) + f2*self.p['k_los']
        h = kb2 - 1.0
        s = np.where(np.diff(np.sign(h)))[0]
        i = s[-1]
        return self.thg[i] - h[i]*(self.thg[i+1]-self.thg[i])/(h[i+1]-h[i])

    def time_delay(self):
        thA, thB = self.images()
        bs = self.p['beta_s']
        psiA = self._interp(thA, self.thg, self.psi1)
        psiB = self._interp(abs(thB), self.thg, self.psi1)
        fermA = 0.5*(thA-bs)**2 - psiA
        fermB = 0.5*(thB-bs)**2 - psiB
        return self.p['ddt']*(fermB - fermA)

    def sigma_los(self, Rbins):
        """Spherical Jeans with radial anisotropy beta(r), Hernquist tracer."""
        a = 0.55
        nu = 1.0/(R*(R+a)**3)
        b = self.beta_func(R)
        # integrating factor I(r) = exp( int 2 b dlnr )
        lnI = np.concatenate([[0.0], np.cumsum(0.5*(2*b[1:]+2*b[:-1])*np.diff(LNR))])
        I = np.exp(lnI - lnI[len(lnI)//2])
        integ = I*nu*self.M/R**2 * R          # * r dlnr
        tail = np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(LNR))[::-1])[::-1], [0.0]])
        nusr2 = tail/I
        lr = np.log(R)
        ln_nusr2 = np.log(np.maximum(nusr2, 1e-300))
        ln_nu = np.log(nu)
        lb_r, lb_v = lr, b
        out = np.empty(len(Rbins))
        u = np.linspace(1e-4, 8, 400)
        for i, Rp in enumerate(Rbins):
            rr = Rp*np.cosh(u)
            lnr = np.log(rr)
            ns2 = np.exp(np.interp(lnr, lr, ln_nusr2))
            nuv = np.exp(np.interp(lnr, lr, ln_nu))
            bb = np.interp(lnr, lb_r, lb_v)
            # los integrand: (1 - beta R^2/r^2) nu sr2 * r/sqrt(r^2-R^2) dr ; dr = Rp sinh u du ; sqrt = Rp sinh u
            num = 2*np.trapezoid((1 - bb*Rp**2/rr**2)*ns2*rr, u)
            den = 2*np.trapezoid(nuv*rr, u)
            out[i] = np.sqrt(num/den)
        return out

RBINS = np.array([0.15, 0.30, 0.45, 0.60, 0.80, 1.00, 1.20, 1.50])

def observables(p, gamma_func=None, beta_func=None, f2=1.35):
    m = LensDyn(p, gamma_func, beta_func)
    thA, thB = m.images()
    return np.concatenate([[thA, thB, m.theta_E2(f2), m.time_delay()],
                           m.sigma_los(RBINS)])
