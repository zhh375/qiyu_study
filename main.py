from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from app.init_db import init_db
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.resources import resource_add_path
import os
import random
from app.cn_word import query_random_cn_word, update_cn_word, cal_cn_word, add_cn_word, qianfan_chat_cn
from app.en_word import query_random_en_word, update_en_word, cal_en_word, add_en_word, query_en_word, query_random_en_word_parent_id
from app.excel_data_syc import cn_word_syc, en_word_syc


init_db()


image_path = os.path.join(os.path.dirname(__file__), "data/image/")
en_word_image_path = os.path.join(os.path.dirname(__file__), "data/en_word_image/")
resource_add_path(os.path.join(os.path.dirname(__file__), "data/fonts/"))
LabelBase.register('Roboto', 'stkaiti.ttf')


display_value = {
    "cn_word": {
            "query_mode": 0,
            "list": [{"name": "开始", "id": "0", "category": 1, "user": "琦琦", "status": 0}]
        },
    "en_word": {
            "query_mode": 0,
            "list": [{"name": "start", "id": "0", "category": 1, "user": "琦琦", "type": 0, "status": 0, "parent_id": 0}]
    }
}
display_value_p = {
    "cn_word": 0,
    "en_word": 0
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

        button_layout = BoxLayout(size_hint_y=None, height=200)
        btn = Button(text='下一个', size_hint_x=1.5, font_size='40sp', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        btn.bind(on_press=self.on_button_next_one_press)
        button_layout.add_widget(btn)

        self.label = Label(text=display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"], font_size='160sp', color=(0, 0, 0, 1))

        bottom_button_layout = BoxLayout(size_hint_y=None, height=150)
        btn = Button(text='统计', font_size='20sp')
        btn.bind(on_press=self.on_button_cal_press)
        bottom_button_layout.add_widget(btn)
        self.query_mode_btn = Button(text='未学会', font_size='20sp')
        if display_value["cn_word"]["query_mode"] == 0:
            self.query_mode_btn.text = "未学会"
        elif display_value["cn_word"]["query_mode"] == 1:
            self.query_mode_btn.text = "所有"
        elif display_value["cn_word"]["query_mode"] == 2:
            self.query_mode_btn.text = "已学会"
        else:
            self.query_mode_btn.text = "拼音"
        self.query_mode_btn.bind(on_press=self.on_button_cn_word_change_press)
        bottom_button_layout.add_widget(self.query_mode_btn)
        btn = Button(text='中文', font_size='20sp')
        btn.bind(on_press=self.on_button_change_mode_press)
        bottom_button_layout.add_widget(btn)
        btn = Button(text='工具', font_size='20sp')
        btn.bind(on_press=self.on_button_tool_press)
        bottom_button_layout.add_widget(btn)

        bottom1_button_layout = BoxLayout(size_hint_y=None, height=150)
        btn = Button(text=f'上一个', font_size='20sp')
        btn.bind(on_press=self.on_button_up_press)
        bottom1_button_layout.add_widget(btn)
        btn = Button(text='组句', font_size='20sp')
        btn.bind(on_press=self.on_button_some_word)
        bottom1_button_layout.add_widget(btn)
        btn = Button(text='短故事', font_size='20sp')
        btn.bind(on_press=self.on_button_many_word)
        bottom1_button_layout.add_widget(btn)
        btn = Button(text=f'设置已学会', font_size='20sp')
        btn.bind(on_press=self.on_button_know_press)
        bottom1_button_layout.add_widget(btn)

        self.add_widget(bottom_button_layout)
        self.add_widget(bottom1_button_layout)
        self.add_widget(self.label)
        self.add_widget(button_layout)

    def on_button_next_one_press(self, instance):
        if display_value_p["cn_word"] < 9 and len(display_value["cn_word"]["list"]) > display_value_p["cn_word"] + 1:
            display_value_p["cn_word"] += 1
        else:
            result = query_random_cn_word(display_value["cn_word"]["query_mode"])
            if result:
                self.know_button_enable = True
                display_value["cn_word"]["list"].append(
                    {"name": result[0][1], "id": result[0][0], "category": result[0][2], "user": result[0][3],
                     "status": result[0][4]})
                if len(display_value["cn_word"]["list"]) > 10:
                    display_value["cn_word"]["list"].pop(0)
                if display_value_p["cn_word"] < 9:
                    display_value_p["cn_word"] += 1
            else:
                popup = Popup(title='提示', content=Label(text='查询为空'), size=(800, 400), size_hint=(None, None))
                popup.open()
                return

        if len(display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]) <= 2:
            self.label.font_size = '160sp'
            self.label.halign = 'center'
        elif len(display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]) <= 4:
            self.label.font_size = '100sp'
            self.label.halign = 'center'
        elif len(display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]) <= 6:
            self.label.font_size = '50sp'
            self.label.halign = 'center'
        elif len(display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]) <= 8:
            self.label.font_size = '50sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'left'
        else:
            self.label.font_size = '30sp'
            self.label.halign = 'center'

        self.label.text = display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]

    def on_button_up_press(self, instance):
        if display_value_p["cn_word"] > 0:
            display_value_p["cn_word"] -= 1
            self.label.text = display_value["cn_word"]["list"][display_value_p["cn_word"]]["name"]
        else:
            popup = Popup(title='提示', content=Label(text='已经是第一个了'), size=(800, 400), size_hint=(None, None))
            popup.open()

    def on_button_know_press(self, instance):
        if display_value["cn_word"]["query_mode"] != 3 and self.know_button_enable is True:
            result = update_cn_word(display_value["cn_word"]["list"][display_value_p["cn_word"]]["id"],
                                    display_value["cn_word"]["list"][display_value_p["cn_word"]]["category"], 1)
            if result is not False:
                display_value["cn_word"]["list"][display_value_p["cn_word"]]["status"] = 1
                self.on_button_next_one_press(instance)
            else:
                popup = Popup(title='提示', content=Label(text='设置失败'), size=(800, 400), size_hint=(None, None))
                popup.open()

    def on_button_some_word(self, instance):
        result = qianfan_chat_cn(0)
        self.label.font_size = '20sp'
        self.label.text_size = (self.label.width, None)
        self.label.halign = 'left'
        self.label.text = result

    def on_button_many_word(self, instance):
        result = qianfan_chat_cn(1)
        self.label.font_size = '20sp'
        self.label.text_size = (self.label.width, None)
        self.label.halign = 'left'
        self.label.text = result

    def on_button_cal_press(self, instance):
        all_count, known_count, unknown_count, today_count = cal_cn_word()
        if all_count is not False and known_count is not False:
            self.know_button_enable = False
            self.label.font_size = '30sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'left'
            self.label.text = ("所有汉字：{all_count}个\n"
                               "已学会汉字或词汇：{known_count}个\n"
                               "未学会汉字或词汇：{unknown_count}个\n"
                               "今天学会：{today_count}个"
                               .format(all_count=all_count[0][0], known_count=known_count[0][0],
                                unknown_count=unknown_count[0][0], today_count=today_count[0][0]))
        else:
            popup = Popup(title='提示', content=Label(text='统计失败'), size=(800, 400), size_hint=(None, None))
            popup.open()

    @staticmethod
    def on_button_tool_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())

    @staticmethod
    def on_button_change_mode_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(EnLayout())

    def on_button_cn_word_change_press(self, instance):
        if display_value["cn_word"]["query_mode"] == 0:
            display_value["cn_word"]["query_mode"] = 1     # 随机所有
            self.query_mode_btn.text = "所有"
            self.on_button_next_one_press(instance)
        elif display_value["cn_word"]["query_mode"] == 1:
            display_value["cn_word"]["query_mode"] = 2     # 随机已学会
            self.query_mode_btn.text = "已学会"
            self.on_button_next_one_press(instance)
        elif display_value["cn_word"]["query_mode"] == 2:
            display_value["cn_word"]["query_mode"] = 3     # 随机拼音
            self.query_mode_btn.text = "拼音"
            self.on_button_next_one_press(instance)
        else:
            display_value["cn_word"]["query_mode"] = 0     # 随机未学会
            self.query_mode_btn.text = "未学会"
            self.on_button_next_one_press(instance)


class EnLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(EnLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.know_button_enable = True
        self.query_mode_btn = None
        self.label = None
        self.gif_image = None

        Window.clearcolor = (1, 1, 1, 1)

        button_layout = BoxLayout(size_hint_y=None, height=200)
        btn = Button(text='下一个', size_hint_x=1.5, font_size='40sp', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        btn.bind(on_press=self.on_button_next_one_press)
        button_layout.add_widget(btn)

        bottom1_button_layout = BoxLayout(size_hint_y=None, height=150)
        btn = Button(text=f'上一个', font_size='20sp')
        btn.bind(on_press=self.on_button_up_press)
        bottom1_button_layout.add_widget(btn)
        btn = Button(text=f'换单词', font_size='20sp')
        btn.bind(on_press=self.on_button_change_word)
        bottom1_button_layout.add_widget(btn)
        btn = Button(text=f'设置已学会', font_size='20sp')
        btn.bind(on_press=self.on_button_know_press)
        bottom1_button_layout.add_widget(btn)

        layout = BoxLayout(orientation='vertical')
        self.gif_image = Image(source=os.path.join(en_word_image_path, 'start.jpg'))
        layout.add_widget(self.gif_image)

        self.label = Label(text=display_value["en_word"]["list"][display_value_p["en_word"]]["name"], font_size='50sp', color=(0, 0, 0, 1))

        bottom_button_layout = BoxLayout(size_hint_y=None, height=150)
        btn = Button(text='统计', font_size='20sp')
        btn.bind(on_press=self.on_button_cal_press)
        bottom_button_layout.add_widget(btn)
        self.query_mode_btn = Button(text='未学会单词', font_size='20sp')
        if display_value["en_word"]["query_mode"] == 1:
            self.query_mode_btn.text = "所有单词"
        elif display_value["en_word"]["query_mode"] == 2:
            self.query_mode_btn.text = "已学会单词"
        elif display_value["en_word"]["query_mode"] == 3:
            self.query_mode_btn.text = "未学会句子"
        elif display_value["en_word"]["query_mode"] == 4:
            self.query_mode_btn.text = "所有句子"
        elif display_value["en_word"]["query_mode"] == 5:
            self.query_mode_btn.text = "已学会句子"
        else:
            self.query_mode_btn.text = "字母"
        self.query_mode_btn.bind(on_press=self.on_button_en_word_change_press)
        bottom_button_layout.add_widget(self.query_mode_btn)
        btn = Button(text='英文', font_size='20sp')
        btn.bind(on_press=self.on_button_change_mode_press)
        bottom_button_layout.add_widget(btn)
        btn = Button(text='工具', font_size='20sp')
        btn.bind(on_press=self.on_button_tool_press)
        bottom_button_layout.add_widget(btn)

        self.add_widget(bottom_button_layout)
        self.add_widget(bottom1_button_layout)
        self.add_widget(layout)
        self.add_widget(self.label)
        self.add_widget(button_layout)

    @staticmethod
    def on_button_change_mode_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(MainLayout())

    def on_button_next_one_press(self, instance):
        if display_value_p["en_word"] < 9 and len(display_value["en_word"]["list"]) > display_value_p["en_word"] + 1:
            display_value_p["en_word"] += 1
        else:
            result = query_random_en_word(display_value["en_word"]["query_mode"])
            if result:
                self.know_button_enable = True
                display_value["en_word"]["list"].append(
                    {"name": result[0][1], "id": result[0][0], "category": result[0][2], "user": result[0][3],
                     "type": result[0][4], "status": result[0][5], "parent_id": result[0][6]})
                if len(display_value["en_word"]["list"]) > 10:
                    display_value["en_word"]["list"].pop(0)
                if display_value_p["en_word"] < 9:
                    display_value_p["en_word"] += 1
            else:
                popup = Popup(title='提示', content=Label(text='查询为空'), size=(800, 400), size_hint=(None, None))
                popup.open()

        if len(display_value["en_word"]["list"][display_value_p["en_word"]]["name"]) <= 4:
            self.label.font_size = '100sp'
            self.label.halign = 'center'
        elif len(display_value["en_word"]["list"][display_value_p["en_word"]]["name"]) <= 6:
            self.label.font_size = '50sp'
            self.label.halign = 'center'
        elif len(display_value["en_word"]["list"][display_value_p["en_word"]]["name"]) <= 8:
            self.label.font_size = '50sp'
            self.label.halign = 'center'
        elif len(display_value["en_word"]["list"][display_value_p["en_word"]]["name"]) <= 10:
            self.label.font_size = '30sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'center'
        else:
            self.label.font_size = '30sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'left'

        self.label.text = display_value["en_word"]["list"][display_value_p["en_word"]]["name"]

        en_word_image_path_now = os.path.join(en_word_image_path,
                                              display_value["en_word"]["list"][display_value_p["en_word"]]["name"] + '.jpg')
        if os.path.exists(en_word_image_path_now):
            self.gif_image.source = en_word_image_path_now
        else:
            en_word_image_path_now = os.path.join(en_word_image_path, 'no_picture.jpg')
            if display_value["en_word"]["query_mode"] in [3, 4, 5]:
                result = query_en_word(None, None, display_value["en_word"]["list"][display_value_p["en_word"]]["user"],
                                       '0', None, display_value["en_word"]["list"][display_value_p["en_word"]]["parent_id"])
                if result:
                    en_word_image_path_now = os.path.join(en_word_image_path, result[0][1] + '.jpg')
                    if os.path.exists(en_word_image_path_now) is False:
                        en_word_image_path_now = os.path.join(en_word_image_path, 'no_picture.jpg')
            self.gif_image.source = en_word_image_path_now

    def on_button_change_word(self, instance):
        if display_value["en_word"]["query_mode"] in [3, 4, 5]:
            result = query_random_en_word_parent_id(display_value["en_word"]["list"][display_value_p["en_word"]]["parent_id"])
            if result:
                en_word_image_path_now = os.path.join(en_word_image_path, result[0][1] + '.jpg')
                if os.path.exists(en_word_image_path_now):
                    self.gif_image.source = en_word_image_path_now
        else:
            popup = Popup(title='提示', content=Label(text='随机句子时按钮才生效'), size=(800, 400), size_hint=(None, None))
            popup.open()

    def on_button_up_press(self, instance):
        if display_value_p["en_word"] > 0:
            display_value_p["en_word"] -= 1
            self.label.text = display_value["en_word"]["list"][display_value_p["en_word"]]["name"]
        else:
            popup = Popup(title='提示', content=Label(text='已经是第一个了'), size=(800, 400), size_hint=(None, None))
            popup.open()

    def on_button_know_press(self, instance):
        if display_value["en_word"]["query_mode"] != 6 and self.know_button_enable is True:
            result = update_en_word(display_value["en_word"]["list"][display_value_p["en_word"]]["id"],
                                    display_value["en_word"]["list"][display_value_p["en_word"]]["category"], 1)
            if result is not False:
                display_value["en_word"]["list"][display_value_p["en_word"]]["status"] = 1
                self.on_button_next_one_press(instance)
            else:
                popup = Popup(title='提示', content=Label(text='设置失败'), size=(800, 400), size_hint=(None, None))
                popup.open()

    def on_button_cal_press(self, instance):
        (all_count_word, all_count_some_word, known_count_word, known_count_some_word,
         unknown_count, today_count) = cal_en_word()
        if all_count_word is not False and known_count_word is not False:
            self.know_button_enable = False
            self.label.font_size = '20sp'
            self.label.text_size = (self.label.width, None)
            self.label.halign = 'left'
            self.label.text = ("所有单词：{all_count_word}个\n"
                               "所有句子：{all_count_some_word}个\n"
                               "所有已学会单词：{known_count_word}个\n"
                               "所有已学会句子：{known_count_some_word}个\n"
                               "未学会单词或句子：{unknown_count}个\n"
                               "今天学会：{today_count}个"
                               .format(all_count_word=all_count_word[0][0], all_count_some_word=all_count_some_word[0][0],
                                       known_count_word=known_count_word[0][0],known_count_some_word=known_count_some_word[0][0],
                                unknown_count=unknown_count[0][0], today_count=today_count[0][0]))
            self.gif_image.source = os.path.join(en_word_image_path, 'come_on.jpg')
        else:
            popup = Popup(title='提示', content=Label(text='统计失败'), size=(800, 400), size_hint=(None, None))
            popup.open()

    @staticmethod
    def on_button_tool_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())

    def on_button_en_word_change_press(self, instance):
        if display_value["en_word"]["query_mode"] == 0:
            display_value["en_word"]["query_mode"] = 1
            self.query_mode_btn.text = "所有单词"
            self.on_button_next_one_press(instance)
        elif display_value["en_word"]["query_mode"] == 1:
            display_value["en_word"]["query_mode"] = 2
            self.query_mode_btn.text = "已学会单词"
            self.on_button_next_one_press(instance)
        elif display_value["en_word"]["query_mode"] == 2:
            display_value["en_word"]["query_mode"] = 3
            self.query_mode_btn.text = "未学会句子"
            self.on_button_next_one_press(instance)
        elif display_value["en_word"]["query_mode"] == 3:
            display_value["en_word"]["query_mode"] = 4
            self.query_mode_btn.text = "所有句子"
            self.on_button_next_one_press(instance)
        elif display_value["en_word"]["query_mode"] == 4:
            display_value["en_word"]["query_mode"] = 5
            self.query_mode_btn.text = "已学会句子"
            self.on_button_next_one_press(instance)
        elif display_value["en_word"]["query_mode"] == 5:
            display_value["en_word"]["query_mode"] = 6
            self.query_mode_btn.text = "字母"
            self.on_button_next_one_press(instance)
        else:
            display_value["en_word"]["query_mode"] = 0
            self.query_mode_btn.text = "未学会单词"
            self.on_button_next_one_press(instance)


class ToolLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolLayout, self).__init__(**kwargs)
        self.popup_cn = None
        self.popup_en = None
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        Window.clearcolor = (1, 1, 1, 1)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='同步汉字', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.show_file_chooser_cn)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='添加汉字', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.add_cn_word)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='同步英文', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.show_file_chooser_en)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='添加英文', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.add_en_word)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='骰子', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.dice_page)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='随机数', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.rand_page)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text=f'返回', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.on_button_back_press)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

    def show_file_chooser_cn(self, instance):
        file_chooser = FileChooserListView(path=os.path.dirname(__file__), filters=['*.xlsx', '*.xls'])

        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(file_chooser)

        button_layout = BoxLayout(size_hint=(1, None), height='50dp')

        ok_button = Button(text="确定", size_hint=(0.5, 1))
        ok_button.bind(on_press=lambda x: self.on_button_syc_cn_word_press(instance, file_chooser.path, file_chooser.selection))
        button_layout.add_widget(ok_button)

        cancel_button = Button(text="取消", size_hint=(0.5, 1))
        cancel_button.bind(on_press=self.dismiss_popup_cn)
        button_layout.add_widget(cancel_button)

        popup_content.add_widget(button_layout)

        # 显示弹出窗口
        self.popup_cn = Popup(title="选择 Excel 文件", content=popup_content, size=(800, 400), size_hint=(0.9, 0.9))
        self.popup_cn.open()

    @staticmethod
    def add_cn_word(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(AddCnWordLayout())

    @staticmethod
    def add_en_word(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(AddEnWordLayout())

    def on_button_syc_cn_word_press(self, instance, path, filename):
        if filename:
            filepath = os.path.join(path, filename[0])
            if cn_word_syc(filepath):
                popup = Popup(title='提示', content=Label(text='同步成功'), size=(800, 400), size_hint=(None, None))
            else:
                popup = Popup(title='提示', content=Label(text='同步失败'), size=(800, 400), size_hint=(None, None))
            self.dismiss_popup_cn(instance)
            popup.open()

    def show_file_chooser_en(self, instance):
        file_chooser = FileChooserListView(path=os.path.dirname(__file__), filters=['*.xlsx', '*.xls'])

        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(file_chooser)

        button_layout = BoxLayout(size_hint=(1, None), height='50dp')

        ok_button = Button(text="确定", size_hint=(0.5, 1))
        ok_button.bind(on_press=lambda x: self.on_button_syc_en_word_press(instance, file_chooser.path, file_chooser.selection))
        button_layout.add_widget(ok_button)

        cancel_button = Button(text="取消", size_hint=(0.5, 1))
        cancel_button.bind(on_press=self.dismiss_popup_en)
        button_layout.add_widget(cancel_button)

        popup_content.add_widget(button_layout)

        # 显示弹出窗口
        self.popup_en = Popup(title="选择 Excel 文件", size=(800, 400), content=popup_content, size_hint=(0.9, 0.9))
        self.popup_en.open()

    def on_button_syc_en_word_press(self, instance, path, filename):
        if filename:
            filepath = os.path.join(path, filename[0])
            if en_word_syc(filepath):
                popup = Popup(title='提示', content=Label(text='同步成功'), size=(800, 400), size_hint=(None, None))
            else:
                popup = Popup(title='提示', content=Label(text='同步失败'), size=(800, 400), size_hint=(None, None))
            self.dismiss_popup_en(instance)
            popup.open()

    def dismiss_popup_cn(self, instance):
        self.popup_cn.dismiss()

    def dismiss_popup_en(self, instance):
        self.popup_en.dismiss()

    @staticmethod
    def on_button_back_press(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(MainLayout())

    @staticmethod
    def rand_page(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(RandLayout())

    @staticmethod
    def dice_page(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(DiceLayout())

class DiceLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(DiceLayout, self).__init__(**kwargs)
        self.popup = None
        self.anim = None
        self.gif_image = None
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        Window.clearcolor = (1, 1, 1, 1)

        layout = BoxLayout(orientation='vertical')
        self.gif_image = Image(source=os.path.join(image_path, 'dice.jpg'))
        layout.add_widget(self.gif_image)
        self.add_widget(layout)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='转一次', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.dice_press)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='返回', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.back)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

    @staticmethod
    def back(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())

    def dice_press(self, instance):
        self.gif_image.source = os.path.join(image_path, 'dice_'+str(random.randint(1, 6))+'.jpg')

class AddCnWordLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AddCnWordLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.text_input_1 = TextInput(hint_text='请输入name', height=40, input_type='text', multiline=True, input_filter=None)
        self.text_input_2 = TextInput(hint_text='请输入category/等级/级别', height=40, input_type='text', input_filter=None)
        self.text_input_3 = TextInput(hint_text='请输入user/用户', height=40, input_type='text', input_filter=None)
        self.text_input_4 = TextInput(hint_text='请输入status/0-未学会/1-已学会', height=40, input_type='text', input_filter=None)
        self.text_input_2.text = "1"
        self.text_input_3.text = "琦琦"
        self.text_input_4.text = "0"

        add_button = Button(text='添加', on_press=self.add)
        return_button = Button(text='返回', on_press=self.back)

        self.add_widget(self.text_input_1)
        self.add_widget(self.text_input_2)
        self.add_widget(self.text_input_3)
        self.add_widget(self.text_input_4)
        self.add_widget(add_button)
        self.add_widget(return_button)

    def add(self, instance):
        if add_cn_word(self.text_input_1.text, self.text_input_2.text, self.text_input_3.text, self.text_input_4.text) == True:
            popup = Popup(title='提示', content=Label(text='添加成功'), size=(800, 400), size_hint=(None, None))
        else:
            popup = Popup(title='提示', content=Label(text='添加失败'), size=(800, 400), size_hint=(None, None))
        popup.open()

    @staticmethod
    def back(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())


class AddEnWordLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AddEnWordLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.text_input_1 = TextInput(hint_text='请输入name', height=40, input_type='text', multiline=True, input_filter=None)
        self.text_input_2 = TextInput(hint_text='请输入category/等级/级别', height=40, input_type='text', input_filter=None)
        self.text_input_3 = TextInput(hint_text='请输入user/用户', height=40, input_type='text', input_filter=None)
        self.text_input_4 = TextInput(hint_text='请输入type/单词/句子', height=40, input_type='text', input_filter=None)
        self.text_input_5 = TextInput(hint_text='请输入status/0-未学会/1-已学会', height=40, input_type='text', input_filter=None)
        self.text_input_2.text = "1"
        self.text_input_3.text = "琦琦"
        self.text_input_4.text = "0"
        self.text_input_5.text = "0"

        add_button = Button(text='添加', on_press=self.add)
        return_button = Button(text='返回', on_press=self.back)

        self.add_widget(self.text_input_1)
        self.add_widget(self.text_input_2)
        self.add_widget(self.text_input_3)
        self.add_widget(self.text_input_4)
        self.add_widget(self.text_input_5)
        self.add_widget(add_button)
        self.add_widget(return_button)

    def add(self, instance):
        if add_en_word(self.text_input_1.text, self.text_input_2.text, self.text_input_3.text, self.text_input_4.text,
                       self.text_input_4.text):
            popup = Popup(title='提示', content=Label(text='添加成功'), size=(800, 400), size_hint=(None, None))
        else:
            popup = Popup(title='提示', content=Label(text='添加失败'), size=(800, 400), size_hint=(None, None))
        popup.open()

    @staticmethod
    def back(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())


class RandLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RandLayout, self).__init__(**kwargs)
        self.popup = None
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        Window.clearcolor = (1, 1, 1, 1)

        self.label = Label(text="Go", font_size='200sp', color=(0, 0, 0, 1))
        self.add_widget(self.label)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='随机', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.rand_press)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = Button(text='返回', size_hint=(None, None), size=(600, 150), font_size='30sp')
        btn.bind(on_press=self.back)
        anchor_layout.add_widget(btn)
        self.add_widget(anchor_layout)

    def rand_press(self, instance):
        self.label.text = str(random.randint(1, 10))

    @staticmethod
    def back(instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(ToolLayout())

class QiyuApp(App):
    def build(self):
        return MainLayout()


QiyuApp().run()
