from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from app.init_db import init_db
from kivy.core.text import LabelBase
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.resources import resource_add_path
import os
from app.cn_word import query_random_cn_word, update_cn_word, cal_cn_word
from app.excel_data_syc import cn_word_syc


init_db()


resource_add_path(os.path.join(os.path.dirname(__file__), "data/fonts/"))
LabelBase.register('Roboto', 'stkaiti.ttf')


display_value = {
    "cn_word": {"name": "开始", "id": "0", "category": 1, "user": "琦琦", "status": 0, "query_mode": 0}
}


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.know_button_enable = True
        self.query_mode_btn = None
        self.label = None

        Window.clearcolor = (1, 1, 1, 1)

        button_layout = BoxLayout(size_hint_y=None, height=100)
        btn = Button(text='下一个', size_hint_x=1.5, font_size='30sp', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        btn.bind(on_press=self.on_button_next_one_press)
        button_layout.add_widget(btn)
        btn = Button(text=f'已学会', font_size='30sp')
        btn.bind(on_press=self.on_button_know_press)
        button_layout.add_widget(btn)

        self.label = Label(text=display_value["cn_word"]["name"], font_size='200sp', color=(0, 0, 0, 1))

        bottom_button_layout = BoxLayout(size_hint_y=None, height=30)
        btn = Button(text='统计', font_size='10sp')
        btn.bind(on_press=self.on_button_cal_press)
        bottom_button_layout.add_widget(btn)
        self.query_mode_btn = Button(text='随机所有', font_size='10sp')
        self.query_mode_btn.bind(on_press=self.on_button_cn_word_change_press)
        bottom_button_layout.add_widget(self.query_mode_btn)
        btn = Button(text='英文', font_size='10sp')
        btn.bind(on_press=self.on_button_change_mode_press)
        bottom_button_layout.add_widget(btn)
        btn = Button(text='工具', font_size='10sp')
        btn.bind(on_press=self.on_button_tool_press)
        bottom_button_layout.add_widget(btn)

        self.add_widget(button_layout)
        self.add_widget(self.label)
        self.add_widget(bottom_button_layout)

    def on_button_next_one_press(self, instance):
        if display_value["cn_word"]["query_mode"] != 3:
            result = query_random_cn_word(display_value["cn_word"]["query_mode"])
            if result is not False:
                self.know_button_enable = True
                display_value["cn_word"]["id"] = result[0][0]
                display_value["cn_word"]["name"] = result[0][1]
                display_value["cn_word"]["category"] = result[0][2]
                display_value["cn_word"]["user"] = result[0][3]
                display_value["cn_word"]["status"] = result[0][4]
                if len(display_value["cn_word"]["name"]) > 2:
                    self.label.font_size = '150sp'
                    self.label.halign = 'center'
                elif len(display_value["cn_word"]["name"]) > 4:
                    self.label.font_size = '100sp'
                    self.label.halign = 'center'
                elif len(display_value["cn_word"]["name"]) > 6:
                    self.label.font_size = '50sp'
                    self.label.halign = 'center'
                elif len(display_value["cn_word"]["name"]) > 8:
                    self.label.font_size = '50sp'
                    self.label.text_size = (self.label.width, None)
                    self.label.halign = 'left'
                else:
                    self.label.font_size = '200sp'
                    self.label.halign = 'center'

                self.label.text = display_value["cn_word"]["name"]
            else:
                popup = Popup(title='提示', content=Label(text='查询为空'), size_hint=(None, None))
                popup.open()

    def on_button_know_press(self, instance):
        if display_value["cn_word"]["query_mode"] != 3 and self.know_button_enable is True:
            result = update_cn_word(display_value["cn_word"]["id"], display_value["cn_word"]["category"], 1)
            if result is not False:
                display_value["cn_word"]["status"] = 1
                self.on_button_next_one_press(instance)
            else:
                popup = Popup(title='提示', content=Label(text='设置失败'), size_hint=(None, None))
                popup.open()

    def on_button_cal_press(self, instance):
        all_count, known_count, unknown_count = cal_cn_word()
        if all_count is not False and known_count is not False:
            self.know_button_enable = False
            self.label.font_size = '30sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'left'
            self.label.text = ("所有汉字：{all_count}个\n已学会汉字或词汇：{known_count}个\n未学会汉字或词汇：{unknown_count}个"
                               .format(all_count=all_count[0][0], known_count=known_count[0][0], unknown_count=unknown_count[0][0]))
        else:
            popup = Popup(title='提示', content=Label(text='统计失败'), size_hint=(None, None))
            popup.open()

    @staticmethod
    def on_button_change_mode_press(instance):
        popup = Popup(title='提示', content=Label(text='暂未实现'), size_hint=(None, None))
        popup.open()

    @staticmethod
    def on_button_tool_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())

    def on_button_cn_word_change_press(self, instance):
        if display_value["cn_word"]["query_mode"] == 0:
            display_value["cn_word"]["query_mode"] = 1     # 随机所有
            self.query_mode_btn.text = "随机已学会"
            self.on_button_next_one_press(instance)
        elif display_value["cn_word"]["query_mode"] == 1:
            display_value["cn_word"]["query_mode"] = 2     # 随机已学会
            self.query_mode_btn.text = "随机未学会"
            self.on_button_next_one_press(instance)
        else:
            display_value["cn_word"]["query_mode"] = 0     # 随机未学会
            self.query_mode_btn.text = "随机所有"
            self.on_button_next_one_press(instance)


class ToolLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolLayout, self).__init__(**kwargs)
        self.popup = None
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        Window.clearcolor = (1, 1, 1, 1)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='同步汉字', size_hint=(None, None), size=(200, 50), font_size='30sp')
        btn.bind(on_press=self.show_file_chooser)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text=f'返回', size_hint=(None, None), size=(200, 50), font_size='30sp')
        btn.bind(on_press=self.on_button_back_press)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

    def show_file_chooser(self, instance):
        file_chooser = FileChooserListView(path=os.path.dirname(__file__), filters=['*.xlsx', '*.xls'])

        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(file_chooser)

        button_layout = BoxLayout(size_hint=(1, None), height='50dp')

        ok_button = Button(text="确定", size_hint=(0.5, 1))
        ok_button.bind(on_press=lambda x: self.on_button_syc_cn_word_press(instance, file_chooser.path, file_chooser.selection))
        button_layout.add_widget(ok_button)

        cancel_button = Button(text="取消", size_hint=(0.5, 1))
        cancel_button.bind(on_press=self.dismiss_popup)
        button_layout.add_widget(cancel_button)

        popup_content.add_widget(button_layout)

        # 显示弹出窗口
        self.popup = Popup(title="选择 Excel 文件", content=popup_content, size_hint=(0.9, 0.9))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()

    def on_button_syc_cn_word_press(self, instance, path, filename):
        if filename:
            filepath = os.path.join(path, filename[0])
            if cn_word_syc(filepath):
                popup = Popup(title='提示', content=Label(text='同步成功'), size_hint=(None, None))
            else:
                popup = Popup(title='提示', content=Label(text='同步失败'), size_hint=(None, None))
            self.dismiss_popup(instance)
            popup.open()

    @staticmethod
    def on_button_back_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(MainLayout())


class QiyuApp(App):
    def build(self):
        return MainLayout()


QiyuApp().run()
