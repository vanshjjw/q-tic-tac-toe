import matplotlib.pyplot as plt
from PIL import Image

def display_board(myBoard, holder=None):
    plt.close()
    plt.figure(figsize=(5, 5))

    for imageNo in range(0, 9):

        if myBoard[0][imageNo // 3][imageNo % 3] != -1 and myBoard[2][imageNo // 3][imageNo % 3] == -1:

            if myBoard[0][imageNo // 3][imageNo % 3] == 100:
                img = Image.open("display-presets/Up.png")
                plt.subplot(3, 3, imageNo + 1)
                plt.imshow(img)
                plt.axis('off')
                plt.text(120, 200, str(myBoard[0][imageNo // 3][imageNo % 3]), color="white",
                         fontdict={"fontsize": 15, "fontweight": 'bold', "ha": "left", "va": "baseline"})

            elif myBoard[0][imageNo // 3][imageNo % 3] == 0:
                img = Image.open("display-presets/Down.png")
                plt.subplot(3, 3, imageNo + 1)
                plt.imshow(img)
                plt.axis('off')
                plt.text(155, 180, str(myBoard[0][imageNo // 3][imageNo % 3]), color="white",
                         fontdict={"fontsize": 20, "fontweight": 'bold', "ha": "left", "va": "baseline"})
            else:
                img = Image.open("display-presets/Plain.png")
                plt.subplot(3, 3, imageNo + 1)
                plt.imshow(img)
                plt.axis('off')
                plt.text(70, 170, str(myBoard[0][imageNo // 3][imageNo % 3]), color="white",
                         fontdict={"fontsize": 20, "fontweight": 'bold', "ha": "left", "va": "baseline"})
                plt.text(185, 210, str(100 - myBoard[0][imageNo // 3][imageNo % 3]), color="white",
                         fontdict={"fontsize": 20, "fontweight": 'bold', "ha": "left", "va": "baseline"})

        elif myBoard[0][imageNo // 3][imageNo % 3] != -1 and myBoard[2][imageNo // 3][imageNo % 3] != -1:

            img = Image.open("display-presets/Plain2.png")
            plt.subplot(3, 3, imageNo + 1)
            plt.imshow(img)
            plt.axis('off')

            if myBoard[2][imageNo // 3][imageNo % 3] < 79:
                plt.text(95, 185, "E+" + str(myBoard[2][imageNo // 3][imageNo % 3] - 70), color="white",
                         fontdict={"fontsize": 20, "fontweight": 'bold', "ha": "left", "va": "baseline"})

            else:
                plt.text(95, 185, "E-" + str(myBoard[2][imageNo // 3][imageNo % 3] - 80), color="white",
                         fontdict={"fontsize": 20, "fontweight": 'bold', "ha": "left", "va": "baseline"})

        else:
            img = Image.open("display-presets/Empty.png")
            plt.subplot(3, 3, imageNo + 1)
            plt.imshow(img)
            plt.axis('off')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.1)
    plt.show(block=False)
