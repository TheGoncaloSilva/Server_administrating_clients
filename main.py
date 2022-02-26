import platform, kivy, os, sys, json
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout # Import GridLayout design
from kivy.uix.button import Button # import buttons
from kivy.uix.label import Label # Import the simbols and widgets
from kivy.uix.popup import Popup # Import Popups
from kivy.uix.boxlayout import BoxLayout # Box layout for Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.lang.parser import global_idmap
from kivy.graphics import Rectangle, Color
from kivy import utils
from src.pages.python.classes import Room
from src.pages.python.modals import OptionsModal
from kivy.modules import inspector
import time, threading, socket, functools
import src.network.serverTCP as Server

class Home(Screen):
    pass

class Start(Screen):
    room_name = ObjectProperty(None)
    room_ip = ObjectProperty(None)
    room_port = ObjectProperty(None)
    room_hosts = ObjectProperty(None)
    room_password = ObjectProperty(None)
    room_encryption = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

        #if os.path.isfile("src/Cached_Room.txt"):
            #with open("src/Cached_Room.txt", "r") as f:
                #info = f.read().split(";")
                #self.room_name.text = info[0]
                #self.room_ip.text = info[1]
                #self.room_port.text = info[2]
                #self.room_hosts.text = info[3]

    # Function to reset the password field if the encryption button is pressed
    def check_press(self):
        if not self.room_encryption.active:
            self.room_password.text = ""

    # Function to get the Inputs size and cut the excessive
    def insert_text(self, input, size):
        if len(input.text) > size:
            input.text = input.text[:size]
    
    # Function to not let introduce characters in number inputs
    def insert_number(self, input, size):
        try:
            if int(input.text) > size:
                input.text = size
            elif int(input.text) <= 0:
                input.text = "1"
        except:
            input.text = input.text[:len(input.text)-1]

class Dash(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_widget(Label(text = "Clients will appear in this menu"))


class MyApp(App):

    room = Room()
    all_clients_ids = []
    server_handler = ''
    client_handler = ''
    active_clients = []
    def_button = ''

    def build(self): # Create the UI
        self.title = 'Network Manager' # Change the the name of the application window
        size_x = 960
        #size_y = 540
        size_y = 480
        Window.size = (size_x, size_y)
        Window.minimum_width, Window.minimum_height = (size_x, size_y)
        #inspector.create_inspector(Window, self) Debug
        return Builder.load_file('main.kv')

    def change_screen(self, sc, way):
        #if sc == 'home': ACTIVATE IF NEEDED
        #    self.close_server()
        manager = self.root.ids.screen_manager
        manager.transition.duration = 0.5
        manager.transition.direction = way
        manager.current = sc

    def default_clients(self):
        net = self.root.ids['dash'].ids
        ##### Default button
        btn = Button(text='Clients will appear here',
                    bold=True,
                    background_normal='',
				    color=[0, 0, 0, 1],
            		background_down='',
				    background_color=[255, 215, 0, 1])
        self.def_button = btn
        net.box.add_widget(btn)

        #for i in range(15): DEBUG
        #self.add_client_view('192.168.50.1', 30, 'Linux', 36.6, 15.4, 8) DEBUG

    def add_client_view(self, ip, port, platform, cpu_usage, ram_usage, total_ram):
        # remove this 
        #ip = '192.168.50.1'
        #platform = 'Linux'
        #cpu_usage = 36.6
        #ram_usage = 15.4
        #total_ram = 8
        ######
        ip = ip + ':' + str(port)
        net = self.root.ids['dash'].ids
        grid = GridLayout(cols=2,rows=4)
        l1 = Label(text='Add: ',
                color=[0,0,0,1], bold= True)
        l1_info = Label(text=ip,
                color=[0,0,0,1], bold= True)
        l2 = Label(text='Platform: ',
                color=[0,0,0,1], bold= True)
        l2_info = Label(text=platform,
                color=[0,0,0,1], bold= True)
        l3 = Label(text='CPU: ',
                color=[0,0,0,1], bold= True)
        l3_info = Label(text=f'{cpu_usage} %',
                color=[0,0,0,1], bold= True)
        l4 = Label(text='RAM: ',
                color=[0,0,0,1], bold= True)
        l4_info = Label(text=f'{ram_usage} % / {total_ram} gb',
                color=[0,0,0,1], bold= True)
        # Positioning widgets
        grid.add_widget(l1)
        grid.add_widget(l1_info)
        grid.add_widget(l2)
        grid.add_widget(l2_info)
        grid.add_widget(l3)
        grid.add_widget(l3_info)
        grid.add_widget(l4)
        grid.add_widget(l4_info)
        # Setting background on the grid
        with grid.canvas.before:
            Color(255, 215, 0, 1, mode='rgba')
            grid.rect = Rectangle(size=(grid.width/2,grid.height/2),
                            pos=grid.pos)
            Clock.schedule_interval(functools.partial(self.update_rect,grid),0.5)# Update the canvas as the screen size change
        self.all_clients_ids.append(grid) # update the dictionary
        net.box.add_widget(grid)
        return {'add': l1_info, 'platform': l2_info, 'cpu': l3_info, 'ram': l4_info, 'grid': grid}

    # update function which makes the canvas adjustable.
    def update_rect(self, grid, *kwargs):
        grid.rect.pos = grid.pos
        grid.rect.size = grid.size


    # Example of self.active_clients = [ip, port, {'add': l1_info, 'platform': l2_info, 'cpu': l3_info, 'ram': l4_info, 'grid': grid}]
    def client_view_update(self, client, ip, port, platform, cpu_usage, ram_usage, total_ram):
        
        ip = ip + ':' + str(port)
        self.active_clients[client][3]['add'].text = ip
        self.active_clients[client][3]['platform'].text = platform
        self.active_clients[client][3]['cpu'].text = f'{cpu_usage} %'
        self.active_clients[client][3]['ram'].text = f'{ram_usage} % / {total_ram} gb'
    
    def client_view_remove(self, client):
        net = self.root.ids['dash'].ids
        self.active_clients[client][3]['grid'].remove_widget(self.active_clients[client][3]['add'])
        self.active_clients[client][3]['grid'].remove_widget(self.active_clients[client][3]['platform'])
        self.active_clients[client][3]['grid'].remove_widget(self.active_clients[client][3]['cpu'])
        self.active_clients[client][3]['grid'].remove_widget(self.active_clients[client][3]['ram'])
        net.box.remove_widget(self.active_clients[client][3]['grid'])
    
    def create_server(self, name, ip, port, max_hosts, password, encryption):
        if self.check_inputs(name, ip, port, max_hosts) == False:
            return print(False)

        self.room.room_name = name.text
        self.room.room_ip = ip.text
        self.room.room_port = port.text
        self.room.room_maxhosts = max_hosts.text
        if encryption.active:
            self.room.room_encryption = os.urandom(16)
        else:
            self.room.room_encryption = ''
        self.room.room_password = password.text
        print(f"Trying to create server {name.text} with ip {ip.text}:{port.text}")
        if self.connect_server():
            self.execute_show_options('success_s')
            #self.add_client_view() DEBUG
            self.cache_data()
            self.default_clients()
            Clock.schedule_interval(functools.partial(self.manage_clients), 0.1) # ADJUST REFRESH VALUE
        else:
            self.execute_show_options('error')

    # Function to create the Socket Server
    def connect_server(self):
        if Server.test_connection(self.room.room_ip, int(self.room.room_port)):
            self.server_handler = threading.Thread(
                                target=Server.initiate_server,args=(self.room.room_ip,
                                                                    int(self.room.room_port),
                                                                    int(self.room.room_maxhosts),
                                                                    self.room.room_name,
                                                                    self.room.room_encryption,
                                                                    self.room.room_password),
                                                                    daemon=True)
            self.server_handler.start()
            return True
        return False
    
    # Posso usar outro thread invés de um clock
    def manage_clients(self, *kwargs):
        # example entry = {'ip': '127.0.0.1', 'port': 35376, 'sys_info': {'platform': 'Linux', 'cpu': 'x86_64', 'cpu_usage': 2.7, 'ram': 31.7, 'total_ram': 15}}
        entry = Server.get_queue_client_data() # Get the oldest data to be processed from the socket server
        if entry != None:
            # TTL for the client to be disconnected because the function is called every 0.5 seconds = 15 seconds => TTL 30
            compare = [entry['ip'], entry['port'], 150, '']
            found = False
            for i, line in enumerate(self.active_clients):
                if compare[0] in line[0] and str(compare[1]) in str(line[1]):
                    found = True
                    self.active_clients[i][2] = 150 # reset TTL
                    self.client_view_update(i, entry['ip'], entry['port'],
                                    entry['sys_info']['platform'],
                                    entry['sys_info']['cpu_usage'],
                                    entry['sys_info']['ram'],
                                    entry['sys_info']['total_ram']) # Update widget

            if not found: # Client not found
                objects = self.add_client_view(entry['ip'], entry['port'],
                                    entry['sys_info']['platform'],
                                    entry['sys_info']['cpu_usage'],
                                    entry['sys_info']['ram'],
                                    entry['sys_info']['total_ram'])
                compare[3] = objects # add objects to the list
                self.active_clients.append(compare)

            Server.remove_last_queue_client_data()
        
        for i, line in enumerate(self.active_clients):
            if line[2] == 0: # If TTL expired
                self.client_view_remove(i)
                self.active_clients.pop(i) # Disconnect Client
                print('CLIENT REMOVED')
            else:
                self.active_clients[i][2] = self.active_clients[i][2] - 1        

    # Function to remove the widgets from the dashboard screen
    # and close the socket server    
    def close_server(self):
        if len(self.active_clients) > 0: # remove default button
            net = self.root.ids['dash'].ids
            net.box.remove_widget(self.def_button)
            self.server_handler.join() # kill the server thread, thus the server
            # KILL CLOCK
            if not self.server_handler.isAlive():
                print('thread killed')
            Server.quit_server()
        for i, line in enumerate(self.active_clients):
            self.client_view_remove(i)
        self.active_clients = []
        

    def check_inputs(self, name, ip, port, max_hosts):
        # when create_server clicked, check if the inputs have data
        # if not popup warning
        if name.text == '':
            self.execute_show_options('warning')
            return False
        elif ip.text == '':
            self.execute_show_options('warning')
            return False
        elif port.text == '':
            self.execute_show_options('warning')
            return False
        elif max_hosts.text == '':
            self.execute_show_options('warning')
            return False
        return True

    def cache_data(self):
        # if a server is successfully created, save those inputs in a file, so that it will be easier next
        # time to create another server
        with open("src/Cached_Room.txt", "w") as f:
            f.write(f"{self.room.room_name}; {self.room.room_ip}; {self.room.room_port}; {self.room.room_maxhosts}")

    def show_options(self, type):
        pop = OptionsModal(type, app)
        pop.open()

    def execute_show_options(self, type):
        Clock.schedule_once(lambda x: self.show_options(type), 0.5)

if __name__ == "__main__":
    app = MyApp()
    app.run()