import dearpygui.dearpygui as dpg
import threading
import time
import os

class main():
    def __init__(self):
        self._plot = None

        dpg.create_context()
        dpg.create_viewport(vsync=True)
        dpg.setup_dearpygui()

        self._mainWin = dpg.add_window(autosize=True)

        threading.Thread(target=self._app).start()

        dpg.set_primary_window(self._mainWin, True)

        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def _app(self):
        while (not dpg.is_dearpygui_running()):
            time.sleep(0.004)
        dpg.maximize_viewport()
        time.sleep(0.1)
        with dpg.group(parent=self._mainWin, horizontal=True):
            dpg.add_button(label="Speedtests", callback=self.s_S)
            dpg.add_button(label="All", callback=self.s_A_D)
            dpg.add_button(label="Daily Mean of All", callback=self.s_A_D_A)
            with dpg.menu(label="Day"):
                for filename in os.listdir(b'./'):
                    if (filename[-4:] == b'.csv') and (filename[:-4] != b'speed'):
                        with dpg.menu(label=str(filename[:-4])[2:-1]):
                            with dpg.group(horizontal=True):
                                dpg.add_button(label="All", callback=self.s_D, user_data=filename[:-4])
                                dpg.add_button(label="Rolling", callback=self.s_D_R_A, user_data=filename[:-4])

    # Show speedtests
    def s_S(self, sender, data, user_data):
        f = open(b'speed.csv', "rb")
        data = f.read()
        f.close()
        days = data.split(b'\n')
        xData = list(range(1, len(days) + 1))
        down = []
        up = []
        for test in range(len(days)):
            down.append(float(days[test].split(b',')[0]))
            up.append(float(days[test].split(b',')[1]))
        if (self._plot != None):dpg.delete_item(self._plot)
        with dpg.plot(label="Speedtest", parent=self._mainWin, anti_aliased=True, width=-1, height=-1, pan_button=-1, tracked=False) as self._plot:
            dpg.add_plot_legend()
            axisA = dpg.add_plot_axis(dpg.mvXAxis, label="Day", no_gridlines=True)
            axisB = dpg.add_plot_axis(dpg.mvYAxis, label="Mbps", no_gridlines=True, lock_min=True)
            dpg.add_line_series(xData, down, label="Download", parent=axisB)
            dpg.add_line_series(xData, up, label="Upload", parent=axisB)
            time.sleep(1 / dpg.get_frame_rate())
            dpg.configure_item(axisA, lock_max=True)
            dpg.configure_item(axisB, lock_max=True)
            dpg.configure_item(axisA, lock_min=True)

    # Show all days
    def s_A_D(self, sender, data, user_data):
        data = b''
        names = []
        for filename in os.listdir(b'./'):
            if (filename[-4:] == b'.csv') and (filename[:-4] != b'speed'):
                f = open(filename, "rb")
                fileData = f.read()
                if (names == []):
                    names = fileData[:fileData.index(b'\n')].split(b',')
                data += fileData[fileData.index(b'\n') + 1:]
                f.close()
        del names[0]
        points = data.replace(b'\n', b',').split(b',')
        del points[len(points) - 1]
        # timestamps = []
        desired = []
        # for i in range(3, len(points), 3):
        #     timestamps.append(points[i])
        for i in range(1, len(names) + 1):
            desired.append([])
            for j in range(int(len(names)) + 1 + i, int(len(points)), int(len(names)) + 1):
                desired[i - 1].append(float(points[j]))
        if (self._plot != None):dpg.delete_item(self._plot)
        with dpg.plot(label="Ping", parent=self._mainWin, anti_aliased=True, width=-1, height=-1, pan_button=-1, tracked=False) as self._plot:
            dpg.add_plot_legend()
            axisA = dpg.add_plot_axis(dpg.mvXAxis, label="Number of pings", no_gridlines=True, lock_min=True)
            axisB = dpg.add_plot_axis(dpg.mvYAxis, label="Milliseconds", no_gridlines=True, lock_min=True)
            for name in range(len(names)):
                dpg.add_line_series(list(range(int((len(points) - (len(names)+1)) / (len(names)+1)))), desired[name], label=str(names[name])[2:-1], parent=axisB)
            time.sleep(1 / dpg.get_frame_rate())
            dpg.configure_item(axisA, lock_max=True)
            dpg.configure_item(axisB, lock_max=True)

    # Show daily average for all days
    def s_A_D_A(self, sender, data, user_data):
        data = b''
        names = []
        values = []
        averages = []
        xAxis = []
        count = 1
        for filename in os.listdir(b'./'):
            if (filename[-4:] == b'.csv') and (filename[:-4] != b'speed'):
                f = open(filename, "rb")
                fileData = f.read()
                f.close()
                if (names == []):
                    names = fileData[:fileData.index(b'\n')].split(b',')
                data = fileData[fileData.index(b'\n') + 1:]
                points = data.replace(b'\n', b',').split(b',')
                del points[len(points) - 1]
                for x in list(range(0, len(names) - 1)):
                    values.append([])
                    averages.append([])
                    for val in range(x + 1, len(points), len(names)):
                        values[x].append(float(points[val]))
                    averages[x].append(sum(values[x]) / (len(points) / len(names)))
                xAxis.append(count)
                count+=1
        del names[0]
        if (self._plot != None):dpg.delete_item(self._plot)
        with dpg.plot(label="Ping", parent=self._mainWin, anti_aliased=True, width=-1, height=-1, pan_button=-1, tracked=False) as self._plot:
            dpg.add_plot_legend()
            axisA = dpg.add_plot_axis(dpg.mvXAxis, label="Day", no_gridlines=True)
            axisB = dpg.add_plot_axis(dpg.mvYAxis, label="Milliseconds", no_gridlines=True)
            for name in range(len(names)):
                dpg.add_line_series(xAxis, averages[name], label=str(names[name])[2:-1], parent=axisB)
            time.sleep(1 / dpg.get_frame_rate())
            dpg.configure_item(axisA, lock_min=True)
            dpg.configure_item(axisB, lock_min=True)
            dpg.configure_item(axisA, lock_max=True)
            dpg.configure_item(axisB, lock_max=True)

    # Show day
    def s_D(self, sender, data, user_data):
        f = open(user_data + b'.csv', "rb")
        data = f.read()
        f.close()
        names = data[:data.index(b'\n')].split(b',')
        del names[0]
        points = data.replace(b'\n', b',').split(b',')
        del points[len(points) - 1]
        # timestamps = []
        desired = []
        # for i in range(3, len(points), 3):
        #     timestamps.append(points[i])
        for i in range(1, len(names) + 1):
            desired.append([])
            for j in range(int(len(names)) + 1 + i, int(len(points)), int(len(names)) + 1):
                desired[i - 1].append(float(points[j]))
        if (self._plot != None):dpg.delete_item(self._plot)
        with dpg.plot(label="Ping", parent=self._mainWin, anti_aliased=True, width=-1, height=-1, pan_button=-1, tracked=False) as self._plot:
            dpg.add_plot_legend()
            axisA = dpg.add_plot_axis(dpg.mvXAxis, label="Number of pings", no_gridlines=True, lock_min=True)
            axisB = dpg.add_plot_axis(dpg.mvYAxis, label="Milliseconds", no_gridlines=True, lock_min=True)
            for name in range(len(names)):
                dpg.add_line_series(list(range(int((len(points) - (len(names)+1)) / (len(names)+1)))), desired[name], label=str(names[name])[2:-1], parent=axisB)
            time.sleep(1 / dpg.get_frame_rate())
            dpg.configure_item(axisA, lock_max=True)
            dpg.configure_item(axisB, lock_max=True)

    # Show day with 50 ping rolling averages
    def s_D_R_A(self, sender, data, user_data):
        f = open(user_data + b'.csv', "rb")
        data = f.read()
        f.close()
        names = data[:data.index(b'\n')].split(b',')
        del names[0]
        points = data.replace(b'\n', b',').split(b',')
        del points[len(points) - 1]
        desired = []
        rollingAvgs = []
        for i in range(1, len(names) + 1):
            desired.append([])
            rollingAvgs.append([])
            for j in range(int(len(names)) + 1 + i, int(len(points)), int(len(names)) + 1):
                desired[i - 1].append(float(points[j]))
                if ((len(desired[i - 1]) % 50) == 0):
                    rollingAvgs[i - 1].append(sum(desired[i -1][-50:]) / 50)
            rollingAvgs[i - 1].append(sum(desired[i - 1][-1 * (len(desired[i - 1]) % 50):]) / (len(desired[i - 1]) % 50))
        if (self._plot != None):dpg.delete_item(self._plot)
        with dpg.plot(label="Ping", parent=self._mainWin, anti_aliased=True, width=-1, height=-1, pan_button=-1, tracked=False) as self._plot:
            dpg.add_plot_legend()
            axisA = dpg.add_plot_axis(dpg.mvXAxis, label="Number of pings", no_gridlines=True, lock_min=True)
            axisB = dpg.add_plot_axis(dpg.mvYAxis, label="Milliseconds", no_gridlines=True, lock_min=True)
            for name in range(len(names)):
                dpg.add_line_series(list(range(0, int((len(points) - (len(names)+1)) / (len(names)+1)), 50)), rollingAvgs[name], label=str(names[name])[2:-1], parent=axisB)
            time.sleep(1 / dpg.get_frame_rate())
            dpg.configure_item(axisA, lock_max=True)
            dpg.configure_item(axisB, lock_max=True)

if (__name__ == "__main__"):
    main()