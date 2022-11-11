from controller.adbconnecter import AdbConnecter
from model.utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, buildDataFolder

class ScreenOperator:
    coordsfilename_ = "static_coords.json"
    specificcoordsfilename = "static_specific_coords.json"

    def __init__(self, connecter: AdbConnecter, width_: int, height_: int) -> None:
        self.connecter_ = connecter
        self.width_ = width_
        self.height_ = height_
        self.debug = False

        self.datPath_ = "C:/Users/NOX/Documents/work/westgame_bot/datas/{}x{}/coords/".format(
			self.width_, self.height_)

        self.static_coords = loadJsonData(self.datPath_ + self.coordsfilename_)
        self.specific_checks_coords = loadJsonData(self.datPath_ + self.specificcoordsfilename)

    def pixel_equals(self, px_readed, px_expected, around=5):
        arr = [5, 5, 5]
        if isinstance(around, int):
            arr = [around, around, around]
        elif isinstance(around, list):
            arr = [around[0], around[1], around[2]]
        # checking only RGB from RGBA
        return px_expected[0] - arr[0] <= px_readed[0] <= px_expected[0] + arr[0] \
               and px_expected[1] - arr[1] <= px_readed[1] <= px_expected[1] + arr[1] \
               and px_expected[2] - arr[2] <= px_readed[2] <= px_expected[2] + arr[2]

    def getFrameAttr(self, frame, attributes):
        attr_data = []
        for attr in attributes:
            x = int(attr[0] * self.width_)
            y = int(attr[1] * self.height_)
            attr_data.append(frame[int(y * self.width_ + x)])
        return attr_data

    def _check_screen_points_equal(self, frame, points_list, points_value, around=2):
        """
        Gets 2 lists of x,y coordinates where to get values and list of values to comapre.
        Returns true if current frame have those values
        :param points_list: a list of x,y coordinates (absolute, not normalized)
        :param points_value: a list (same size of points_list) with values for equals check (values are 4d)
        :param around: an integer for interval of search: +around and -around.
        :return:
        """
        if len(points_list) != len(points_value):
            print("Wrong size between points and values!")
            return False
        if self.debug: print("-----------------------------------")
        if self.debug: print("|   Smartphone   |     Values     |")
        attr_data = self.getFrameAttr(frame, points_list)
        equal = True
        for i in range(len(attr_data)):
            if self.debug: print("| %4d %4d %4d | %4d %4d %4d |" % (
                attr_data[i][0], attr_data[i][1], attr_data[i][2], points_value[i][0], points_value[i][1],
                points_value[i][2]))
            if not self.pixel_equals(attr_data[i], points_value[i], around=around):
                equal = False
        if self.debug: print("|-->         %s" % ("  equal           <--|" if equal else "not equal         <--|"))
        if self.debug: print("-----------------------------------")
        return equal

    def checkFrame(self, coords_name: str, frame=None):
        """
        Given a coordinates name it checkes if the Frame has those pixels.
        If no Frame given , it will take a screenshot.
        :return:
        """
        print(coords_name)
        print("Checking screen....")
        dict_to_take = []
        if coords_name in self.static_coords.keys():
            dict_to_take = self.static_coords
        elif coords_name in self.specific_checks_coords.keys():
            dict_to_take = self.specific_checks_coords
        else:
            print("No coordinates called %s is saved in memory! Returning false." % coords_name)
            return False
        if self.debug: print("Checking %s" % (coords_name))
        if frame is None:
            frame = self.getFrame()
        around = 2 if "around" not in dict_to_take[coords_name].keys() else dict_to_take[coords_name]["around"]
        is_equal = self._check_screen_points_equal(frame, dict_to_take[coords_name]["coordinates"],
                                                   dict_to_take[coords_name]["values"], around=around)

        return is_equal

    def getFrame(self):
        if self.connecter_.connectedToDevice() == False:
            exit()
        return self.connecter_.adb_screen_getpixels()

    def getFrameStateComplete(self, frame=None) -> dict:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a dictionary with all known states with boolean value assigned.
        :return:
        """
        result = {}
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            around = 2 if "around" not in self.static_coords[k].keys() else self.static_coords[k]["around"]
            if self.debug: print("Checking %s, around = %d" % (k, around))
            result[k] = self._check_screen_points_equal(frame, v["coordinates"], v["values"], around=around)
        return result

    def getFrameState(self, frame=None) -> str:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a string with the name of current state, or unknown if no state found.
        :return:
        """
        state = "unknown"
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            around = 2 if "around" not in self.static_coords[k].keys() else self.static_coords[k]["around"]
            if self.debug: print("Checking %s, around = %d" % (k, around))
            if self._check_screen_points_equal(frame, v["coordinates"], v["values"], around=around):
                state = k
                break
        return state

    def _getHorLine(self, hor_line, frame):
        """
        Returns a horizontal line (list of colors) given hor_line [x1, y1, x2, y2] coordinates. If no frame given, it takes a screen.
        :param hor_line:
        :param frame:
        :return:
        """
        x1, y1, x2, y2 = hor_line[0] * self.width_, hor_line[1] * self.height_, hor_line[2] * self.width_, hor_line[
            3] * self.height_
        if frame is None:
            frame = self.getFrame()
        start = int(y1 * self.width_ + x1)
        size = int(x2 - x1)
        line = frame[start:start + size]
        return line

    def getLineExpBar(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        line = self._getHorLine(self.hor_lines["hor_exp_bar"], frame)
        masked_yellow = []
        for px in line:
            if self.pixel_equals(px, self.yellow_experience, 3):
                masked_yellow.append(px)
            else:
                masked_yellow.append([0, 0, 0, 0])
        return masked_yellow