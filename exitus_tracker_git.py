import customtkinter
import time as t
from threading import Thread
from ahk import AHK
from PIL import Image, ImageGrab
import keyboard
import pyautogui
import pydirectinput
import pygetwindow as gw
import win32api
import win32con
import pywintypes
import queue



class CeleExitusRoot(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.resolution_pixel_mapping = {
            (2560, 1440): {
                "Cele_Client_Off": (-3, -2),
                "Exitus_Tracker_Off": -8},  # Root Window is off on x for 8 pixel
            (1920, 1080): {
                "Cele_Client_Off": (-0, -0),  # need to be figured out for full HD
                "Exitus_Tracker_Off": -0},  # need to be figured out for full HD
            (2560, 1600): {
                "Cele_Client_Off": (-3, -2),
                "Exitus_Tracker_Off": -8}
        }
        self.main_monitor_resolution = get_main_monitor_resolution()
        self.minsize(300, 80)
        self.maxsize(300, 560)
        self.geometry(f"300x80+{self.resolution_pixel_mapping[self.main_monitor_resolution]['Exitus_Tracker_Off']}+800")
        self.title("Exitus Tracker")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        self.attributes('-topmost', 'true')  # Window is always in foreground
        self.attributes("-alpha", 0.7)  # Changing transparency to 0.7
        self.ahk = AHK()  # Initializing a working process for AHK
        #self.setup_adjust_cele_client()  # Adjusting the Cele Client in the beginning for one time
        self.setup_global_hotkeys()
        self.pipeline = queue.Queue(maxsize=1)
        self.setup_keyboard_listener()
        self.setup_evaluation_recorded_key_inputs()
        self.cele_client_window_handle = None
        self.resize_image_factor = 1.15
        self.frames = []  # Frames saved here in order to be able to access them later for destroying

    def get_win_cele_client(self):
        """
        Getting the Cele client window as described below by pid
        :return:
        """
        CELE_CLIENT_TITLE = "Celestial World 2.0"
        GET_BY_PID = "ahk_pid"

        for window in self.ahk.list_windows():
            if window.title == CELE_CLIENT_TITLE and len(window.text) == 0:
                """The actually cele client got a window.text len of 0. The Celestial World 2.0 folder has the same 
                title(window.title) as the cele client. So you can't win_get() by title, in case the user has also the 
                folder open. So you go for the pid of the cele client"""
                cele_client_pid = window.pid
                win = self.ahk.win_get(title=GET_BY_PID + str(cele_client_pid))
                return win
        else:
            return False

    def adjust_cele_client(self):
        """
        Adjusting the left and upper gab between Cele client and end of screen
        Adjust Cele client after getting with .get_win_cele_client()
        :return: Callable[adjust_cele_client]
        """
        if win_cele_client := self.get_win_cele_client():
            x, y = self.resolution_pixel_mapping[self.main_monitor_resolution]["Cele_Client_Off"]
            win_cele_client.move(x=x, y=y)
            return
        else:
            print("Windows of Cele Client is not opened or couldn't be found to move the window")
            t.sleep(0.1)
            return self.adjust_cele_client()

    def setup_adjust_cele_client(self):
        """
        Initializes Thread
        """
        adjustment_thread = Thread(target=self.adjust_cele_client, daemon=True)
        adjustment_thread.start()

    def global_hotkeys(self):
        """
        Defines hotkeys
        """
        keyboard.add_hotkey('shift+q', self.setup_adjust_cele_client)
        keyboard.add_hotkey('shift+c', self.get_cele_client_window_handle)
        keyboard.wait()

    def setup_global_hotkeys(self):
        """
        Setups the global hotkeys in separate thread
        """
        hotkey_thread = Thread(target=self.global_hotkeys, daemon=True)
        hotkey_thread.start()

    def keyboard_listener(self):
        """
        REWORKED
        Constantly capturing all keyboard inputs for 0.3 seconds as small "pieces" (as long as there's a user input)
        and saving into self.recent_recorded_key_inputs
        """
        while True:
            key_input = keyboard.read_event()
            if key_input.event_type == keyboard.KEY_UP:
                self.pipeline.put(key_input.name)
                print(f"Put {key_input.name} into pipeline")

    def setup_keyboard_listener(self):
        """
        setup keyboard_listener in separate thread
        """
        keyboard_listener_thread = Thread(target=self.keyboard_listener, daemon=True)
        keyboard_listener_thread.start()

    def evaluate_recorded_key_inputs(self):
        """
        Creating a new frame based on the user input
        """
        while True:
            current_key_inputs = self.pipeline.get()
            print(f"Get {current_key_inputs} from pipeline")

            if current_key_inputs == 'f11':
                create_frame_thread = Thread(target=self.create_frame, args=("portal", self.resize_image_factor))
                create_frame_thread.start()


            elif current_key_inputs =='f12':
                destroy_all_frames_thread = Thread(target=self.destroy_all_frames)
                destroy_all_frames_thread.start()

            elif current_key_inputs == 'f9':
                create_frame_thread = Thread(target=self.create_frame, args=("waypoint", self.resize_image_factor))
                create_frame_thread.start()

    def setup_evaluation_recorded_key_inputs(self):
        """
         setup evaluate_recorded_key_inputs in separate thread
        """
        evaluation_recorded_key_inputs_thread = Thread(target=self.evaluate_recorded_key_inputs, daemon=True)
        evaluation_recorded_key_inputs_thread.start()

    def get_cele_client_window_handle(self):
        """
        getting window handle of current activ window, used later to activate cele_client when sending key_inputs to it.
        Saving it to self.cele_client_window_handle
        """
        self.cele_client_window_handle = gw.getActiveWindow()
        print(f"Getting the handle of the current active window:\nTitle: {self.cele_client_window_handle.title}\n"
              f"Handle: {self.cele_client_window_handle._hWnd}")

    def send_keyboard_input_client(self, keyboard_input):
        """
        sending keyboard inputs to cele client
        uses the self.cele_client_window_handle to interact with window
        :param keyboard_input:
        """
        cele_client = self.cele_client_window_handle
        try:
            cele_client.activate()
            t.sleep(0.1)
            pydirectinput.press(keyboard_input)
        except AttributeError:
            print("Window handle of cele client was not found, but is needed to send keyboard inputs to it! Press shift+c")

    def adjust_root_height(self):
        """
        checks if the current height of the root window must be adjusted
        the current height must match the amount of saved frames * base height
        if otherwise, it must be adjusted by just adding to the current height, the base height
        """
        BASE_HEIGHT_FRAME = 80
        current_height = self._current_height

        if not current_height == (len(self.frames) * BASE_HEIGHT_FRAME):
            geometry = "300x" + (str(self._current_height + BASE_HEIGHT_FRAME))
            self.geometry(geometry)
        else:
            return

    def create_frame(self, frame_type: str, resize_image_factor: float|None):
        """
        creating a new frame, checking the flag must_be_destroyed. Flag gets set to True if pyautogui isn't able to
        take screenshots of map name or bonus.
        If flag is false the frame can be appended to self.frames[] the root height can be adjusted and the frame can
        be gridded. Additionally, it will be sent a key to the client to save the coordinates in order to the
        teleporting system

        :param frame_type: str
        :param resize_image_factor: float|None
        """
        frame = CeleExitusFrame(master=self, frame_type=frame_type, resize_image_factor=resize_image_factor)
        if frame.must_be_destroyed:
            frame.destroy()
            print("Frame was destroyed")
        else:
            self.frames.append(frame)
            self.adjust_root_height()
            frame.grid()
            #self.send_keyboard_input_client('r')
            print("New frame was created \n current frames:", self.frames)

    def destroy_all_frames(self):
        """
        destroying all frames, clearing self.frames[], setting geometry back to default and sending key to client to
        delete all saved coordinates in cele client
        """
        for frame in self.frames:
            frame.destroy()
            #del frame
        self.frames.clear()
        self.geometry("300x80")
        self.send_keyboard_input_client('numpad9')
        CeleExitusButton.created_buttons = 0
        print("Setting CeleExitusButton.created_buttons back to 0")
        print("Destroying all frames and setting geometry back to 300x80", self.frames)


class CeleExitusFrame(customtkinter.CTkFrame):
    def __init__(self, master, frame_type: str, resize_image_factor: float|None):
        super().__init__(master)
        self.frame_type = frame_type
        self.resize_image_factor = resize_image_factor
        self.must_be_destroyed = False
        self.screenshot_map_name = None
        self.screenshot_boni_window = None
        self.headline_coordinates = None

        if self.frame_type == "portal":
            self.take_screenshot_map_name()
            self.take_screenshot_boni_window()
            master.send_keyboard_input_client("esc")
            master.send_keyboard_input_client("numpad0")

            if not self.must_be_destroyed:
                self.configure(width=300)
                self.configure(height=80)
                self.teleport_button = CeleExitusButton(self, screenshot_map_name=self.screenshot_map_name,
                                                        screenshot_boni_window=self.screenshot_boni_window)
                self.teleport_button.grid()

        else:
            self.configure(width=300)
            self.configure(height=80)
            waypoint_image = Image.open("Waypoint.PNG")
            #print(waypoint_image.size)
            if self.resize_image_factor:
                waypoint_image = self.resize_image(waypoint_image)

            waypoint_image = customtkinter.CTkImage(light_image=waypoint_image,
                                            dark_image=waypoint_image,
                                            size=waypoint_image.size)
            self.teleport_button = CeleExitusButton(self, waypoint_image=waypoint_image)
            self.teleport_button.grid()


    def take_screenshot(self, coordinates, resize: bool = False):
        """
        taking a screenshot of a given box at the monitor
        :param coordinates:
        :param resize:
        :return: screenshot
        """
        screenshot = ImageGrab.grab(coordinates)
        if resize and self.resize_image_factor:
            screenshot = self.resize_image(screenshot)

        screenshot = customtkinter.CTkImage(light_image=screenshot,
                                            dark_image=screenshot,
                                            size=screenshot.size)
        return screenshot

    def locate_fields_onscreen(self, image_filename, recursion_depth=0, confidence=0.9):
        """

        :param image_filename: str
        :param recursion_depth: int
        :param confidence: float
        :return: coordinates_field
        """
        try:
            coordinates_field = pyautogui.locateCenterOnScreen(image_filename, confidence=confidence)
            #print(coordinates_field)
        except pyautogui.ImageNotFoundException:
            if recursion_depth == 3:
                print("Abort function locate_fields_onscreen")
                self.must_be_destroyed = True
                return False
            else:
                recursion_depth += 1
                confidence -= 0.1
                print("Celestial_Portal Headline or Confirm Button couldn't be fetched on first attempt\n now doing",
                      recursion_depth+1, "attempt, with confidence", confidence)
                t.sleep(0.1)
                return self.locate_fields_onscreen(image_filename, recursion_depth, confidence)
        else:
            return coordinates_field

    def take_screenshot_map_name(self):
        """
        Take the screenshot of the mapname
                """
        try:
            x, y = self.locate_fields_onscreen('Celestial_Portal_Headline_2k.PNG')
            self.headline_coordinates = x,y
        except TypeError:
            print("Couldn't take screenshot of map name due to error in ImageNotFound")
        else:
            border_box = (x - 64, y + 22, x + 64, y + 40)  # calc for 2k border box: left, top, right, bottom for 2k
            print(border_box)
            screenshot_map_name = self.take_screenshot(border_box, resize=True)
            self.screenshot_map_name = screenshot_map_name

    def take_screenshot_boni_window(self):
        """
        Take the screenshot of the boni_window
        """
        try:
            x2, y2 = self.locate_fields_onscreen('Confirm_Button_2k.PNG')
            x1, y1 = self.headline_coordinates
        except TypeError:
            print("Couldn't take screenshot of boni window due to error in ImageNotFound")
        else:
            border_box = (x1 - 91, y1 + 10, x2 + 91, y2 - 15)  # calc for 2k | different on other resolution?
            print(border_box)
            screenshot_boni_window = self.take_screenshot(border_box)
            self.screenshot_boni_window = screenshot_boni_window

    def resize_image(self, image):
        """
        :param image:
        :return: image_resized
        """
        new_image_size = tuple(int(x * self.resize_image_factor) for x in image.size)
        image_resized = image.resize(size=new_image_size, resample=Image.Resampling.LANCZOS)
        return image_resized


class CeleExitusButton(customtkinter.CTkButton):
    created_buttons = 0
    def __init__(self, master, screenshot_map_name=None, screenshot_boni_window=None, waypoint_image=None):
        super().__init__(master)
        CeleExitusButton.created_buttons+=1
        self.button_id = CeleExitusButton.created_buttons
        self.master = master
        self.configure(width=300)
        self.configure(height=80)
        self.configure(text="")
        self.configure(command=self.teleport)
        self.configure(corner_radius=5)
        self.configure(border_width=2)
        self.configure(fg_color="transparent")
        self.waypoint_image = waypoint_image
        if self.waypoint_image:
            self.configure(image=self.waypoint_image)
        else:
            self.screenshot_map_name = screenshot_map_name
            self.screenshot_boni_window = screenshot_boni_window
            self.toplevel = None
            self.configure(image=self.screenshot_map_name)
            self.bind_event()

    def teleport(self):
        """
        teleport to the saved position
        :return:
        """
        self.master.master.send_keyboard_input_client(f"numpad{self.button_id}")

    def bind_event(self):
        """
        binging entering and leaving event to button
        :return:
        """
        event_list = ["<Enter>", "<Leave>"]
        for event in event_list:
            self.bind(event, self.event_handler)

    def event_handler(self, event):
        """
        reacting to given event
        :param event:
        :return:
        """
        event_type = event.type

        if event_type == "7":
            self.toplevel = self.create_toplevel()
            print("Enter")

        elif event_type == "8":
            self.toplevel.destroy()
            print("Leave")

    def create_toplevel(self):
        """
        creating a toplevel hold the screenshots
        :return:
        """
        toplevel = CeleExitusToplevel(self, self.screenshot_boni_window.cget("size"), self.screenshot_boni_window)
        return toplevel


class CeleExitusToplevel(customtkinter.CTkToplevel):
    def __init__(self, master, screenshot_size, screenshot_boni_window):
        super().__init__(master)
        self.overrideredirect(True)
        self.screenshot_size = screenshot_size
        self.screenshot_boni_window = screenshot_boni_window
        self.geometry(f"{self.screenshot_size[0]}x{self.screenshot_size[1]}+300+600")
        self.attributes('-topmost', 'true')
        self.label = customtkinter.CTkLabel(self, width=self.screenshot_size[0], height=self.screenshot_size[1],
                                            image=self.screenshot_boni_window, text="")
        self.label.grid()


################ Helper Functions #####################################


def get_main_monitor_resolution():
    """
    Function to calculate the main monitor resolution under windows
    :return: (width, height) : Tuple = The width and height of the main monitor resolution
    """
    i = 0
    while True:
        try:
            device = win32api.EnumDisplayDevices(None, i)
        except pywintypes.error as exc:
            print(exc)
            break
        else:
            if device.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE:
                settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
                width = settings.PelsWidth
                height = settings.PelsHeight
                return width, height
        i += 1
