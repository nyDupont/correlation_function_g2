from re import findall
from numpy import zeros, ones
from artificial_images import triming
from numpy import linspace
import PCF


def tab_img(strfichiertxt, *, magnitude=1):
    print('importing image...')
    string = ''

    with open("data/"+strfichiertxt, 'r') as coords:
        for ligne in coords:
            string += ligne

    listestr = findall('[0-9]{1,3}[.][0-9]{6}', string)  # finding all coordinates, [x1,y1,x2,y2,etc.]

    listefloat = []
    for i in listestr:
        listefloat.append(magnitude*float(i))  # applying magnitude factor (== cutting the opt pix into several num pix)

    coordx_f, coordy_f = listefloat[::2], listefloat[1::2]  # index f to avoid shadow name from outer scope
    minx_f, miny_f, maxx_f, maxy_f = min(coordx_f), min(coordy_f), max(coordx_f), max(coordy_f)
    wimg_f, himg_f = int(minx_f + maxx_f), int(miny_f + maxy_f)
    nbpoints_f = len(coordx_f)

    # generating the corresponding 2d pixels grid
    tab_f = zeros((himg_f+1, wimg_f+1))
    for i in range(len(coordx_f)):
        tab_f[int(coordy_f[i]), int(coordx_f[i])] += 1
    tab_f /= tab_f.max()

    # min_tab_f = 1
    # for i in range(int(maxy_f)):
    #     for j in range(int(maxx_f)):
    #         if tab_f[i, j] != 0 and tab_f[i, j] < min_tab_f:
    #             min_tab_f = tab_f[i, j]

    print('image imported with magnitude {}\nlist length : {}\n'
          'dimensions (y,x) : {}'.format(magnitude, nbpoints_f, tab_f.shape))
    return coordx_f, coordy_f, tab_f  # , nbpoints_f, wimg_f, himg_f, minx_f, miny_f, maxx_f, maxy_f , min_tab_f


def annular_triming(tabf, r1, r2, *, centre=0):
    if r1 != 0:
        triming(tabf, ('circle', r1), centre=centre, side='-')
    triming(tabf, ('circle', r2), centre=centre, side='+')


def annular_sampling(tabf, r1, r2, nb, *, centre=0):
    g2r = []
    binf = int((r2-r1)/nb)
    for i in range(nb):
        mask = ones(tabf.shape)
        wtab = tabf.copy()  # ?
        annular_triming(wtab, r1+i*binf, r1+(i+1)*binf, centre=centre)
        annular_triming(mask, r1+i*binf, r1+(i+1)*binf, centre=centre)
        wg2r = PCF.radial_dens(PCF.cart_pcf(wtab, mask=mask))

        # fitting a gaussian on the first peak, whose ~fwhm is the measured average radius of clusters
        # popt = PCF.g_fit(PCF.gauss2, wg2r[0][1:binf], wg2r[1][1:binf])
        # popt = PCF.g_fit(PCF.veatchfit, wg2r[0][1:binf], wg2r[1][1:binf])
        # print(popt)
        # fwhm = 4 / 3.43 * abs(popt[0])  # calibrate with artifical data
        # x = linspace(0, int(len(g2r[0])), 2000)  # to plot the obtained gaussian if wanted
        # y = PCF.gauss2(x, popt[0], popt[1])
        
        g2r += wg2r[1][0:binf]
    return g2r

