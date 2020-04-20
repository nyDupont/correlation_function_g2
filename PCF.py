from numpy import real, ones, sum, fft, absolute, pi, sqrt, array, exp
from scipy import integrate as itg
from scipy.optimize import curve_fit


def cart_pcf(tab_f, *, mask=0):
    print('g2xy...')
    # numerator
    num = real(fft.fftshift(fft.ifft2((absolute(fft.fft2(tab_f))) ** 2)))

    # denominator
    # if mask == 0:
    #     mask = ones((tab_f.shape[0], tab_f.shape[1]))
    # if trim != 0:
    #     roi(mask, rroi[0], rroi[1], rroi[2])
    smask = sum(mask)

    rho = sum(tab_f) / smask

    denom = rho ** 2 * real(fft.fftshift(fft.ifft2((absolute(fft.fft2(mask)))**2)))

    g2xy_f = num / denom
    # print('g2xy.')
    return g2xy_f  # ,mask  # , min_g2xy_f  # returning mask for one to plot if wanted


def radial_dens(tab_f, *, centre=0):  # , range_g=0):
    print('radial density...')
    h, w = tab_f.shape
    if centre == 0:
        centre = h/2, w/2
        range_g = int(round((sqrt(h**2+w**2)/2)))
    else:
        range_g = 0
        for i in 0, 1:
            for j in 0, 1:
                dist_corner = int(round((sqrt((centre[0]-i*h)**2+((centre[1]-j*w)**2)))))
                if dist_corner > range_g:
                    range_g = dist_corner
    # diag = [i for i in range(1, range_g+1)]
    raddens = (range_g+1)*[(0, 0)]  # (objects at r, places at r)
    for i in range(h):
        for j in range(w):
            r = int(round(sqrt((centre[0]-i)**2+(centre[1]-j)**2)))
            raddens[r] = (raddens[r][0]+tab_f[i, j], raddens[r][1]+1)
    for i in range(1, len(raddens)):
        if raddens[i][1] == 0:
            break
        raddens[i] = raddens[i][0]/raddens[i][1]
    return [i for i in range(1, len(raddens))], raddens[1:]


# Ripley's K function
def k_r(g_r_f, r_f):  # x, y, upper x limit (third arg is the right argument of k)
    return 2*pi*itg.simps(array(g_r_f[:r_f])*array(range(0, r_f
                                                         )))


# Modified Ripley's L-r function
def l_rm(k_r_f, r_f):
    return sqrt(k_r_f[r_f-1]/pi)-r_f


# a gaussian centered around zero and translated upward by 1 unit ;
# for the FWHM of the first peak to give average radius
def gauss2(x_f, s, a):
    return 1 + a * exp(-x_f**2 / (2 * s**2))


def power(x, s):
    return 1+1/(s*x**2)


def veatchfit(x, sigma, rho, A, xi, C):
    return exp(-x**2/2/sigma**2)/sqrt(2*pi)/sigma/rho + A*exp(-x/xi) + C


# fitting the above gaussian, returning amp and std
def g_fit(fct, x, y):
    popt, pcov = curve_fit(fct, x, y, maxfev=1000000)
    return popt
