import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition, NoTransition
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.config import Config
# from kivy.uix.textinput import TextInput

from blank_checker.checker import getting_data, verification_works


Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '600')


class CheckPicture:
    picture = ''

    def __int__(self, picture, source):
        self.picture = picture


class DataInput:
    count_variants = 0
    count_answer_options = 0
    count_question = 36
    orders_answers = dict()
    checking_pictures = []

    @staticmethod
    def print_all_data_input():
        print(f'Выбранное количество вариантов: {DataInput.count_variants}')
        print(f'Выбранное количество вриантов ответа: {DataInput.count_answer_options}')
        print(f'Выбранное количество вопросов: {DataInput.count_question}')
        print(f'Порядок ответов: {DataInput.orders_answers}')
        print(f'Изображения: {DataInput.checking_pictures}')


class PreviewPage(Screen):
    pass


# ///////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////// TUTORIAL ////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////

class TutorialPageOne(Screen):

    @staticmethod
    def switch_next_screen():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_2'

    @staticmethod
    def skip_tutorial():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'constructor_page_1'


class TutorialPageTwo(Screen):

    @staticmethod
    def switch_next_screen():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_3'

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_1'

    @staticmethod
    def skip_tutorial():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'constructor_page_1'


class TutorialPageThree(Screen):

    @staticmethod
    def switch_next_screen():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_4'

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_2'

    @staticmethod
    def skip_tutorial():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'constructor_page_1'


class TutorialPageFour(Screen):

    @staticmethod
    def switch_next_screen():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_5'

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_3'

    @staticmethod
    def skip_tutorial():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'constructor_page_1'


class TutorialPageFive(Screen):

    @staticmethod
    def switch_to_constructor():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'constructor_page_1'

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_4'

# ///////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////// CONSTRUCTOR //////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////


class ConstructorPageOne(Screen):

    def switch_next_screen(self):
        TestApp.screen_manager.transition = SlideTransition(direction='left')
        TestApp.screen_manager.current = 'constructor_page_2'
        DataInput.count_question = self.ids.count_question_input.text

    @staticmethod
    def switch_back_to_tutorial():
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'tutorial_page_1'

    @staticmethod
    def on_click_checkbox_answers(instance, value):
        if instance:
            DataInput.count_answer_options = value

    @staticmethod
    def on_click_checkbox_variants(instance, value):
        if instance:
            DataInput.count_variants = value


class ConstructorPageTwo(Screen):
    textInputs = []
    labels = []

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.transition = SlideTransition(direction='right')
        TestApp.screen_manager.current = 'constructor_page_1'

    def switch_to_check_data_page(self):
        TestApp.screen_manager.transition = FadeTransition()
        TestApp.screen_manager.current = 'download_picture_page'

    def get_textinput(self):
        current_y = 0.75
        fl = self.ids.constructor_two_layout
        for i in range(int(DataInput.count_variants)):
            label = Label(text=f'Вариант {i+1}', pos_hint={'center_x': 0.17, 'center_y': current_y},
                                color=[0, 0, 0, 0.5])
            textinput = kivy.uix.textinput.TextInput(size_hint=[0.6, 0.05], font_size=12,
                                                       pos_hint={'center_x': 0.64, 'center_y': current_y})
            self.textInputs.append(textinput)
            self.labels.append(label)
            fl.add_widget(label)
            fl.add_widget(textinput)
            current_y -= 0.08

    def clean_input(self):
        DataInput.orders_answers = {'count_questions': int(DataInput.count_question)}
        fl = self.ids.constructor_two_layout
        index = 1
        for tinput in self.textInputs:
            fl.remove_widget(tinput)
            DataInput.orders_answers[str(index)] = tinput.text
            index += 1
        for label in self.labels:
            fl.remove_widget(label)
        DataInput.print_all_data_input()


# ///////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// GALLERY //////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////

class DownloadPicturePage(Screen):

    @staticmethod
    def get_picture():
        TestApp.screen_manager.transition = NoTransition()
        TestApp.screen_manager.current = 'gallery_pictures'


class GalleryPictures(Screen):
    preview_picture = Image()
    loading_picture = ''
    types = ['.jpg', '.img', '.svg', '.png', '.jpeg']

    def selected(self, file_name):
        try:
            self.ids.gallery_layout.remove_widget(self.preview_picture)
            self.ids.load_button.disabled = True
            self.ids.gallery_buttons.size_hint = [1, 0.1]
            if file_name[0][file_name[0].find('.'):] in self.types:
                self.preview_picture.source = file_name[0]
                self.ids.load_button.disabled = False
                self.ids.gallery_buttons.size_hint = [1, 0.2]
                self.ids.gallery_layout.add_widget(self.preview_picture, 1)
                self.loading_picture = file_name[0]
        except:
            pass

    def load_picture(self):
        DataInput.checking_pictures.append(self.loading_picture)
        self.ids.done_button.disabled = False
        DataInput.print_all_data_input()

    @staticmethod
    def close_gallery():
        TestApp.screen_manager.current = 'results_page'


class ResultsPage(Screen):
    current_picture = 0

    def set_picture(self):
        carousel = self.ids.pictures_result
        for image in DataInput.checking_pictures:
            bl = BoxLayout(orientation='vertical')
            label = Label(text=self.get_result(image), color=[0, 0, 0, 0.5], size_hint=[1, 0.25], font_size=17)
            image = AsyncImage(source=image, allow_stretch=True, size_hint=[1, 0.6], pos_hint={'center_x': 0.5, 'center_y': 0.7})
            bl.add_widget(image)
            bl.add_widget(label)
            carousel.add_widget(bl)

    def get_result(self, image):
        result = verification_works(getting_data(image), DataInput.orders_answers)
        return(f'Выполнение работы - {result["per_complition"]}\n'
               f'Правильные ответы - {result["result"]}')

    @staticmethod
    def switch_screen_back():
        TestApp.screen_manager.current = 'gallery_pictures'
        DataInput.checking_pictures = []


# ///////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////// MANAGER //////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////

class WindowManager(ScreenManager):
    pass


class TestApp(App):
    screen_manager = ScreenManager()

    def build(self):
        Builder.load_file('ScrManager.kv')
        self.screen_manager.add_widget(PreviewPage(name='preview_page'))
        self.screen_manager.add_widget(TutorialPageOne(name='tutorial_page_1'))
        self.screen_manager.add_widget(TutorialPageTwo(name='tutorial_page_2'))
        self.screen_manager.add_widget(TutorialPageThree(name='tutorial_page_3'))
        self.screen_manager.add_widget(TutorialPageFour(name='tutorial_page_4'))
        self.screen_manager.add_widget(TutorialPageFive(name='tutorial_page_5'))
        self.screen_manager.add_widget(ConstructorPageOne(name='constructor_page_1'))
        self.screen_manager.add_widget((DownloadPicturePage(name='download_picture_page')))
        self.screen_manager.add_widget(ConstructorPageTwo(name='constructor_page_2'))
        self.screen_manager.add_widget(GalleryPictures(name='gallery_pictures'))
        self.screen_manager.add_widget(ResultsPage(name='results_page'))
        return self.screen_manager

    def on_start(self):
        Clock.schedule_once(self.set_next_page, 5)

    def set_next_page(self, dt):
        self.screen_manager.transition = FadeTransition()
        self.screen_manager.current = 'tutorial_page_1'


if __name__ == '__main__':
    TestApp().run()
