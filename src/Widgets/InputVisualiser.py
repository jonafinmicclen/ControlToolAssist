import matplotlib.pyplot as plt

class Visualiser:
    def __init__(self, x, y):

        self.num_points = len(x)
        self.x = x
        self.y = y

        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter(self.x, self.y, picker=True)

        self.dragging = False
        self.picked_point = None

        self.fig.canvas.mpl_connect('pick_event', self.update)
        self.fig.canvas.mpl_connect('motion_notify_event', self.update)
        self.fig.canvas.mpl_connect('button_release_event', self.update)

        plt.show()

    def update(self, event):
        if event.name == 'pick_event' and event.mouseevent.button == 1:

            self.picked_point = event.ind[0]
            self.dragging = True

        elif event.name == 'motion_notify_event' and self.dragging:

            self.y[self.picked_point] = event.ydata
            self.scatter.set_offsets(list(zip(self.x, self.y)))
            self.fig.canvas.draw_idle()

        elif event.name == 'button_release_event':

            self.dragging = False


if __name__ == "__main__":
    x = [0,1,2,3,4,5,6,7,8,9]
    y = [0,0,0,0,0,0,0,0,0,0]
    newPlot = Visualiser(x,y)