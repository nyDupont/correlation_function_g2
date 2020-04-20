from matplotlib.pyplot import imshow, plot, figure, subplot #, title, xlabel, ylabel, grid
from numpy import array


def graph(data):
    figure(1)
    i = 1
    disp = ['11', '12', '22', '22']
    for element in data:
        ind = int(disp[len(data)-1] + str(i))
        subplot(ind)
        if array(element).ndim == 1:
            plot([i for i in range(1, len(element)+1)], element, 'k-')
        if array(element).ndim == 2:
            imshow(element, 'Greys')
        i += 1
