import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from skimage import measure

from PIL import Image
from skimage.color import rgb2gray

import os

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


def listfiles(path, extension):
    # Get the list of all files and directories
    files = []
    print("The files found in the specified path with given extension")
    for x in os.listdir(path):
        if x.endswith(extension):
            # Prints only files present in path with .extension
            print(x)
            files.append(x)
    return files


def pointcloudcreation(imagepath):

    mpl.rcParams["legend.fontsize"] = 100

    img = Image.open(imagepath)

    np_img = np.array(img)

    print("Sahpe of the image array: ", np_img.shape)

    np_img = rgb2gray(np_img)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    title = imagepath

    ax.set_title(title)

    ax.set_xlabel("X")

    ax.set_ylabel("Y")

    ax.set_zlabel("Z")

    filepath = imagepath.strip(".tif") + ".xyz"

    outputfile = open(filepath, "w")

    for i in range(1, 255, 1):
        try:
            contours = measure.find_contours(np_img, i)
            for contour in contours:
                if 5000 > len(contour) > 300:

                    z = np.ones_like(contour)
                    z = z * i
                    label = str(i)
                    ax.plot(contour[:, 1], contour[:, 0], z[:, 0])

                    for j in range(0, contour.shape[0], 1):
                        outputfile.write(
                            str(contour[j, 0])
                            + "\t"
                            + str(contour[j, 1])
                            + "\t"
                            + str(i)
                            + "\n"
                        )

        except:
            print("There is no contour to find. Continuing for the next itteration.")
            continue

    print("The calculations are done!\n")
    outputfile.close()
    savepath = imagepath.strip(".tif") + ".png"
    plt.savefig(savepath)
    # plt.show()


def main():
    basefolderpath = (os.getcwd())
    paths = listfiles(basefolderpath, "tif")

    for path in paths:
        
        pointcloudcreation(path)


if __name__ == "__main__":
    main()
