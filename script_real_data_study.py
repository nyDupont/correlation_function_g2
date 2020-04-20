import real_images as ri
import PCF
import matplotlib.pyplot as plt

# real data study
magn = 8
# data files

name, ann = 'sBC24_A24_3.txt', (730, 849, 399)

img = ri.tab_img(name, magnitude=magn)

# computing g2r from g2xy
"""
r1, r2, bin = 0/8*magn, ann[2]/8*magn, 3
centre = int(ann[0]/8*magn), int(ann[1]/8*magn)
g2r = ri.annular_sampling(img[2], r1, r2, bin, centre=centre)
"""

g2r = PCF.radial_dens(img[2])
# g2r = PCF.radial_dens(PCF.cart_pcf(img[2][440:620, 760:980]))
# g2r = PCF.radial_dens(PCF.cart_pcf(img[2], mask=mask))

"""
# fitting a gaussian on the first peak, whose ~fwhm is the measured average radius of clusters
popt = PCF.g_fit(PCF.gauss2, g2r[0][1:10], g2r[1][1:10])
fwhm = 4/3.43*abs(popt[0])  # calibrate with artifical data
x = linspace(0, int(len(g2r[0])), 2000)  # to plot the obtained gaussian if wanted
y = PCF.gauss2(x, popt[0], popt[1])
"""

# K = [PCF.k_r(g2r[1], r) for r in g2r[0]]
# Lr = [PCF.l_rm(K, r) for r in g2r[0]]

# plotting
police = 12

fig = plt.figure(1)
fig.subplots_adjust(wspace=0.44, bottom=0.14)

plt.subplot(121)
plt.plot(img[0], img[1], 'k,')
xmin, xmax = min(img[0]), max(img[0])
ymin, ymax = min(img[0]), max(img[0])
print(xmin, xmax, ymin, ymax)
plt.xlim(int(xmin), int(xmax)+1)
plt.ylim(int(ymin), int(ymax)+1)
plt.xticks(fontsize=int(0.8 * police))
plt.yticks(fontsize=int(0.8 * police))
plt.title(name, fontsize=police)
plt.xlabel("x [pixels]", fontsize=police)
plt.ylabel("y [pixels]", fontsize=police)


plt.subplot(122)
plt.plot(g2r[0][:100], g2r[1][:100])
plt.title("B : g$_2$(r)", fontsize=police)
plt.xticks(fontsize=int(0.8 * police))
plt.yticks(fontsize=int(0.8 * police))
plt.grid(color='grey', linestyle='--', linewidth=0.5)
plt.xlabel("r = $\sqrt{x^2+y^2}$ [pixels]", fontsize=police)
plt.ylabel("g$_2$(r)", fontsize=police)

"""

subplot(121)
plot(img[0], img[1], 'k,')
theta = linspace(0, 2*pi, 200)
for r in range(1,bin+1):
X, Y = [], []
ray = r1+(r2-r1)*r/bin
for t in theta:
    X.append(centre[1]+ray*cos(t))
    Y.append(centre[0]+ray*sin(t))
plot(X, Y)
xticks(fontsize=int(0.8 * police))
yticks(fontsize=int(0.8 * police))
title("A : {} en {} anneaux".format(name[:-4], bin), fontsize=police)
xlabel("x [pixels]", fontsize=police)
ylabel("y [pixels]", fontsize=police)
"""

# plt.imshow(img[2], 'Greys')

"""
subplot(222)
imshow(img[2], 'Greys', norm=LogNorm(vmin=0.001, vmax=1))
subplot(223)
# plot(g2r[0], g2r[1])
plot([i for i in range(1, len(g2r)+1)], g2r)
"""
"""
subplot(122)
for i in range(bin):
plot([j for j in range(1, int(len(g2r)/bin)+1)], g2r[i*int(len(g2r)/bin):(i+1)*int(len(g2r)/bin)],
     label='de ' + str(i*int(len(g2r)/bin)) + ' à ' + str((i+1)*int(len(g2r)/bin)) + ' pix du centre')
legend(prop={'size': int(0.8*police)})
xticks(fontsize=int(0.8 * police))
yticks(fontsize=int(0.8 * police))
title("B : g$_2$(r) sur chaque anneau", fontsize=police)
xlabel("x [pixels]", fontsize=police)
ylabel("y [pixels]", fontsize=police)
# plot(x, y, 'r-')
# subplot(223)
# plot(g2r[0], K)
# subplot(224)
# plot(g2r[0], Lr)
"""
# print('supposed averaged cluster radius : {} pix = {} nm'
#       .format(str(trunc(fwhm*100)/100), str(trunc(fwhm*160/magn*100)/100)))

plt.show()

