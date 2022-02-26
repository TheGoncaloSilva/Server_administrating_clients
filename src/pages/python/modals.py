from ctypes import util
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy import utils

class OptionsModal(Popup):
    def __init__(self, type, app, **kwargs):
        super(OptionsModal, self).__init__(**kwargs)
        self.app = app
        self.size_hint = [None, None]
        self.pos_hint = {'center_x': 0.5, "top": .7}
        self.height = 250
        self.width = 310
        self.auto_dismiss = False
        if type == 'error':
            # title
            self.title = "critical".upper()
            self.background_color = [255, 0, 0, 1]
            self.title_size = '16sp'
            self.title_color = [1, 1, 1, 1]
            # separator
            self.separator_color = [1, 1, 1, 1]
            self.separator_height: 10
            # content
            self.box = BoxLayout(size_hint_y = .3,
                                padding = 10, 
                                spacing = 10, 
                                pos_hint = {'top': .99, 'center_x': .5}, 
                                orientation = 'horizontal', 
                                height = 40)

            self.l_info = Label(text = "An error occurred, please check your Inputs or try again later", 
                                color = [1, 1, 1, 1],
                                font_size = "15sp", 
                                bold = True,
                                markup = True,
                                size_hint_y = None,
                                max_lines = 20,
    			                text_size = [self.width, None],
    			                height = 40,
                                valign = 'top')

            self.save_btn = Button(text = "Close", 
                                background_normal = '', 
                                background_color = [1, 1, 1, 1], 
                                color = [0, 0, 0, 1], 
                                font_size = "18sp", 
                                bold = True, 
                                pos_hint = {'center_x': .5, "y": .03}, 
                                size_hint = [.9, .15])
            # callbacks
            self.save_btn.bind(on_release=lambda x: self.dismiss())
            self.l_info.bind(size=self.l_info.setter('text_size'))# limits the text area to a specific size, that's a size of the widget itself
            # positioning widgets on the popup
            self.box.add_widget(self.l_info)
            self.float = FloatLayout()
            self.float.add_widget(self.box)
            self.float.add_widget(self.save_btn)
            self.add_widget(self.float)
        
        if type == 'warning':
            # title
            self.title = "warning".upper()
            #self.background_color = utils.get_color_from_hex('##ff0000')
            self.background_color = [255, 255, 0, 1]
            self.title_size = '16sp'
            self.title_color = [0, 0, 0, 1]
            # separator
            self.separator_color = [1, 1, 1, 1]
            self.separator_height: 10
            # content
            self.box = BoxLayout(size_hint_y = .3,
                                padding = 10, 
                                spacing = 10, 
                                pos_hint = {'top': .99, 'center_x': .5}, 
                                orientation = 'horizontal', 
                                height = 40)

            self.l_info = Label(text = "The inputs Name, IP and Max_hosts are required inputs, please check", 
                                color = [0, 0, 0, 1],
                                font_size = "15sp", 
                                bold = True,
                                markup = True,
                                size_hint_y = None,
                                max_lines = 20,
    			                text_size = [self.width, None],
    			                height = 40,
                                valign = 'top')

            self.save_btn = Button(text = "Close", 
                                background_normal = '', 
                                background_color = [1, 1, 1, 1], 
                                color = [0, 0, 0, 1], 
                                font_size = "18sp", 
                                bold = True, 
                                pos_hint = {'center_x': .5, "y": .03}, 
                                size_hint = [.9, .15])
            # callbacks
            self.save_btn.bind(on_release=lambda x: self.dismiss())
            self.l_info.bind(size=self.l_info.setter('text_size'))# limits the text area to a specific size, that's a size of the widget itself
            # positioning widgets on the popup
            self.box.add_widget(self.l_info)
            self.float = FloatLayout()
            self.float.add_widget(self.box)
            self.float.add_widget(self.save_btn)
            self.add_widget(self.float)

        if type == 'success_s': 
                     # title
            self.title = "Success".upper()
            #self.background_color = utils.get_color_from_hex('##ff0000')
            self.background_color = [0, 255, 0, 1]
            self.title_size = '16sp'
            self.title_color = [0, 0, 0, 1]
            # separator
            self.separator_color = [1, 1, 1, 1]
            self.separator_height: 10
            # content
            self.box = BoxLayout(size_hint_y = .3,
                                padding = 10, 
                                spacing = 10, 
                                pos_hint = {'top': .99, 'center_x': .5}, 
                                orientation = 'horizontal', 
                                height = 40)

            self.l_info = Label(text = "The requested Operation was successfully executed", 
                                color = [0, 0, 0, 1],
                                font_size = "15sp", 
                                bold = True,
                                markup = True,
                                size_hint_y = None,
                                max_lines = 20,
    			                text_size = [self.width, None],
    			                height = 40,
                                valign = 'top')

            self.save_btn = Button(text = "Close", 
                                background_normal = '', 
                                background_color = [1, 1, 1, 1], 
                                color = [0, 0, 0, 1], 
                                font_size = "18sp", 
                                bold = True, 
                                pos_hint = {'center_x': .5, "y": .03}, 
                                size_hint = [.9, .15])
            # callbacks
            self.save_btn.bind(on_release=lambda x: self.fade())
            self.l_info.bind(size=self.l_info.setter('text_size'))# limits the text area to a specific size, that's a size of the widget itself
            # positioning widgets on the popup
            self.box.add_widget(self.l_info)
            self.float = FloatLayout()
            self.float.add_widget(self.box)
            self.float.add_widget(self.save_btn)
            self.add_widget(self.float)

    def fade(self):
        self.app.change_screen('dash', 'up')
        self.dismiss()
