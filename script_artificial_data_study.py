import artificial_images as ai
import PCF
from numpy import zeros, linspace, log, sqrt, trunc, pi, sin, cos, ones
from matplotlib.pyplot import imshow, plot, show, figure, subplot, title, xlabel, ylabel, grid, legend, xticks, yticks
from matplotlib.colors import LogNorm
from graph import graph

# image size
himg, wimg = 512, 512
presence_trim = 1  # 1 or True for deviation
roi = 'circle', 200
# roi = 0
# lattice kind and step
structure = 'equi'
tab = zeros((himg, wimg))
step = 48  # characteristic distance, ideally a multiple of 8

# disorder
presence_dev = 1  # 1 or True for deviation
rdev_std = 15  # around a null deviation

# clusters radius
cclm = 5  # average clusters radius
cclsd = 1.5  # sd of radii distribution

# white noise
presence_noise = 1  # 1 or True for noise
bruit = 5000  # amount of noise pixels

mask = ai.imaging(tab, structure, step, presence_trim, roi, presence_dev, rdev_std,
              cclm, cclsd, presence_noise, bruit)

g2xy = PCF.cart_pcf(tab, mask=mask)
g2r = PCF.radial_dens(g2xy)

# popt = PCF.g_fit(PCF.gauss2, g2r[0][1:int(2*cclm)], g2r[1][1:int(2*cclm)])
# fwhm = 2 * sqrt(2 * log(2)) * popt[0]
# fwhm = 4/2.53*abs(popt[0])  # calibrate for a 4 pix radius
# fwhm = 10/7.29*abs(popt[0])
# x = linspace(0.1, int(len(g2r[0])), 2000)
# y = PCF.gauss2(x, popt[0], popt[1])
# y = PCF.pow(x, popt[0])

K = [PCF.k_r(g2r[1], r) for r in g2r[0]]
Lr = [PCF.l_rm(K, r) for r in g2r[0]]

figure(1)
police = 12


subplot(131)
imshow(tab, 'Greys')
xticks(fontsize=int(0.8 * police))
yticks(fontsize=int(0.8 * police))
title("A : image", fontsize=police)
xlabel("x [px]", fontsize=police)
ylabel("y [px]", fontsize=police)


subplot(132)
A = imshow(g2xy, 'Greys', extent=[-wimg / 2, wimg / 2, -himg / 2, himg / 2], norm=LogNorm(0.01, 100))
xticks(fontsize=int(0.8 * police))
yticks(fontsize=int(0.8 * police))
title("B : g$_2$(x, y)", fontsize=police)
xlabel("x [px]", fontsize=police)

subplot(133)
plot(g2r[0][:100], g2r[1][:100])
title("C : g$_2$(r)")
grid()
xticks(fontsize=int(0.8 * police))
yticks(fontsize=int(0.8 * police))
xlabel("r = $\sqrt{x^2+y^2}$ [px]", fontsize=police)
ylabel("g$_2$(r)", fontsize=police)

# plot(g2r[0][:100], K[:100], 'c-')
# title("C : fonction de Ripley K$_{2}$(r)", fontsize=police)
# grid(color='grey', linestyle='--', linewidth=0.5)
# xticks(fontsize=int(0.8 * police))
# yticks(fontsize=int(0.8 * police))
# xlabel("r = $\sqrt{x^2+y^2}$ [pixels]", fontsize=police)
# ylabel("K$_{2}$(r)", fontsize=police)

# subplot(224)
# plot(g2r[0][:100], Lr[:100], 'b-')
# title("B : fonction de Ripley modifiée L$_{2}$(r)-r" , fontsize=police)
# grid(color='grey', linestyle='--', linewidth=0.5)
# xticks(fontsize=int(0.8 * police))
# yticks(fontsize=int(0.8 * police))
# xlabel("r = $\sqrt{x^2+y^2}$ [pixels]", fontsize=police)
# ylabel("L$_{2}$(r)-r", fontsize=police)

show()
