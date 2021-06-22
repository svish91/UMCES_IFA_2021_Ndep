
import numpy as np

# this is to change the resolution of the raster
def f_changingResolution(imarray, desiredCellSize, originalCellSize, desiredMatrixSz ):

    # this is the size of division of the grid
    sz = np.int(np.round(desiredCellSize/originalCellSize))

    lat = np.arange(0, imarray.shape[0], sz)
    lon = np.arange(0, imarray.shape[1], sz)
    outMatrix = np.zeros((desiredMatrixSz[0], desiredMatrixSz[1]), dtype="float")

    for lat1 in range(1, len(lat)):
        for lon1 in range(1, len(lon)):
            if lon1 == len(lon) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(imarray[lat[lat1-1]:lat[lat1], lon[lon1-1]:imarray.shape[1]-1])

            elif lat1 == len(lat) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(imarray[lat[lat1-1]:imarray.shape[0]-1, lon[lon1-1]:lon[lon1]])

            elif lon1 == len(lon) - 1 and lat1 == len(lat) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(imarray[lat[lat1-1]:imarray.shape[0]-1, lon[lon1-1]:imarray.shape[1]-1])

            else:
                outMatrix[lat1-1, lon1-1] = np.nansum(imarray[lat[lat1-1]:lat[lat1], lon[lon1-1]:lon[lon1]])

    return(outMatrix)