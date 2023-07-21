from matplotlib import pyplot as plt
import pandas as pd
import imageio
import os
from time import sleep

class PlotMarket:
    
    def __init__(self,frames=1,
                 file = "./data/re-netto_2_simulation.csv",path="./figures"):
        self.output_path = path
        self.input_file = file
        self.frames = frames
        self.minute = 0

    def get_time(self):
        """current time in HH:MM format,
        """
        hour = 7 + self.minute // 60
        minutes = self.minute % 60
        timestamp = f"{hour:02d}:{minutes:02d}" 
        return timestamp

    def create_plots(self):

        counter = 0
        df = pd.read_csv(self.input_file)
        PATH = "market.png"
          
        img = plt.imread(PATH)

        for _ in df["time"].unique():
            
            time = self.get_time()
            X = df[df['time'] == time]['x'].values
            y = df[df['time'] == time]['y'].values
            plt.axis((0, 120, 0, 60))
            plt.imshow(img, extent=[-5, 120, -2, 60])
            plt.scatter(x=X,y=y, s=100)
            plt.savefig(fname = f'{self.output_path}/market{counter}.png', dpi=72, format="png", bbox_inches='tight', pad_inches=0.5)
            print(f'saved to {self.output_path}/market{counter}.png')
            plt.close()
            counter += 1
            self.minute += 1
        return None
    
    def create_giph(self):
        images = []

        all_pics = os.listdir(self.output_path)
        for pic in all_pics:
               pic_path = f'{self.output_path}/{pic}'
               if os.path.isfile(pic_path):
                   images.append(imageio.imread(pic_path))
               else: print('Skipped file')

        imageio.mimsave('output.gif', images, fps=self.frames)
        return None


    
