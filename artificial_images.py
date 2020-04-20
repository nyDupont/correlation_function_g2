from numpy import sqrt, ones
from random import uniform, gauss, random


def deviation(tabf, rdev_stdf):  # rdev_mf, rdev_stdf):
    for i in range(tabf.shape[0]):
        for j in range(tabf.shape[1]):
            if tabf[i, j] == 1:
                tabf[i, j] = 0
                fdw = int(gauss(0, rdev_stdf))
                fdh = int(gauss(0, rdev_stdf))
                # fdw = rm.uniform(-rdev_max, rdev_max)
                # fdh = rm.uniform(-rdev_max, rdev_max)
                """
                d = sqrt(fdh ** 2 + fdw ** 2)
                
                while d > rdev_mf:
                    fdw = int(gauss(0, rdev_stdf))
                    fdh = int(gauss(0, rdev_stdf))
                    d = sqrt(fdh ** 2 + fdw ** 2)
                """
                # ensuring points do not get out of tab
                if 0 <= i+fdh < tabf.shape[0] and 0 <= j+fdw < tabf.shape[1]:
                    tabf[i+fdh, j+fdw] = random()


def clustering(tabf, coordf, radius_m, sd):
    for i in range(len(coordf)):
        radf = int(gauss(radius_m, sd))  # cclm/10))  # 2e agrument std sigma. = 0 pour ccl = cclm fixe
        # clustering around centers
        for j in range(-radf, radf + 1):
            for k in range(-radf, radf + 1):
                # doing so in a circle shape
                if sqrt(j ** 2 + k ** 2) <= radf:
                    # ensuring points do not get out of tab
                    if 0 <= coordf[i][0] + j < + tabf.shape[0] and 0 <= coordf[i][1] + k < + tabf.shape[1]:
                        tabf[coordf[i][0] + j, coordf[i][1] + k] = random()


def noise_making(tabf, bruit):
    bx, by = [], []
    for b in range(bruit):
        bx.append(int(uniform(0, tabf.shape[1])))
        by.append(int(uniform(0, tabf.shape[0])))
    for i in range(len(bx)):
        tabf[by[i], bx[i]] = random()


def triming(tabf, roi_f, *, centre=0, side='+'):
    shape, dim1, dim2 = roi_f[0], roi_f[1], roi_f[2:]
    himgf, wimgf = tabf.shape[0], tabf.shape[1]
    if centre == 0:
        centre = int(himgf/2), int(wimgf/2)
    if shape == 'square':
        yf = [i for i in range(int((himgf-dim1)/2))]+[i for i in range(int((himgf+dim1)/2), himgf)]
        for i in yf:
            for j in range(wimgf):
                tabf[i, j] = 0
        xf = [i for i in range(int((wimgf-dim1)/2))]+[i for i in range(int((wimgf+dim1)/2), wimgf)]
        for j in xf:
            for i in range(himgf):
                tabf[i, j] = 0
        # return int(sqrt(2)*dim1)

    if shape in ['rect', 'rectangle', 'quad']:
        yf = [i for i in range(int((himgf - dim1) / 2))] + [i for i in range(int((himgf + dim1) / 2), himgf)]
        for i in yf:
            for j in range(wimgf):
                tabf[i, j] = 0
        xf = [i for i in range(int((wimgf - dim2[0]) / 2))] + [i for i in range(int((wimgf + dim2[0]) / 2), wimgf)]
        for j in xf:
            for i in range(himgf):
                tabf[i, j] = 0
        # return int(sqrt(dim1**2+dim2[0]**2))

    if shape == 'circle':
        for i in range(-centre[0], centre[0]):
            if centre[0]+i < himgf:
                for j in range(-centre[1], centre[1]):
                    if centre[1]+abs(j) < wimgf:
                        if side == '+':
                            if sqrt(i**2+j**2) > dim1:
                                tabf[centre[0]+i, centre[1]+j] = 0
                        elif side == '-':
                            if sqrt(i**2+j**2) < dim1:
                                tabf[centre[0]+i, centre[1]+j] = 0
        # return int(dim1)


def imaging(tab, structure, step, presence_trim, roi, presence_dev,
            rdev_std, cclm, cclsd, presence_noise, bruit):

    if structure in [0, 'hex', 'hexa', 'hexagonal', 'equi', 'equilateral']:
        opp = int(7 * step / 8)  # to simulate a hexagonal lattice :
        adj = int(step / 2)  # (~60.25, 60.25 and 59.50 degrees angles in the ~equilateral triangles for 8|step)
        tab[::2*opp, adj::2*adj] = 1
        tab[opp::2*opp, ::2 * adj] = 1

    elif structure in [1, 'square', 'grid', 'quad']:
        tab[::step, ::step] = 1

    if presence_dev:
        deviation(tab, rdev_std)

    coordgen_d = []
    for i in range(tab.shape[0]):
        for j in range(tab.shape[1]):
            if tab[i, j] != 0:
                coordgen_d.append((i, j))  # mind order (y, x)

    if cclm != 0:
        clustering(tab, coordgen_d, cclm, cclsd)

    if presence_noise:
        noise_making(tab, bruit)

    mask = ones(tab.shape)

    if presence_trim:
        triming(tab, roi)  # , side="-") # range_g is up to where g2 will be computed ; also trims.
        triming(mask, roi)

    return mask


"""
# # image characteristics # #
# image size
himg, wimg = 512, 512
presence_trim = 1  # 1 or True for deviation
roi = 'circle', 200

# lattice step
structure = 'equi'
tab = zeros((himg, wimg))
step = 56  # characteristic distance, ideally a multiple of 8
opp = int(7*step/8)  # to simulate a hexagonal lattice :
adj = int(step/2)  # (~60.25, 60.25 and 59.50 degrees angles in the ~equilateral triangles for 8|step)

# disorder
presence_dev = 1   # 1 or True for deviation
rdev_max = 50
rdev_std = 25

# clusters radius
cclm = 10  # average clusters radius
cclsd = 3  # sd of radii distribution

# white noise
presence_noise = 1  # 1 or True for noise
bruit = 5000  # amount of noise pixels


# # image generation # #
# imaging()

# plt.imshow(tab, 'Greys')
# plt.show()
"""