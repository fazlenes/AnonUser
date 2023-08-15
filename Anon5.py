import kivy
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.storage.jsonstore import JsonStore
import mysql.connector



kivy.require("1.11.1")


MYSQL_HOST = 'localhost'
MYSQL_USER = 'username'
MYSQL_PASSWORD = 'pass:)'
MYSQL_DATABASE = 'databasename'


connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = connection.cursor()

class ScrollableBoxLayout(BoxLayout, FocusBehavior):
    pass

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        self.email = ""
        self.background_color = (1, 1, 0, 1)

        image = Image(source="resim.png", size_hint=(1, 1))
        self.add_widget(image)

        self.sign_up_button = Button(text="Sign Up", background_color=[1, 0, 2, 1], on_release=self.sign_up)
        self.add_widget(self.sign_up_button)

        self.login_button = Button(text="Login", background_color=[1, 1, -2, 1], on_release=self.login)
        self.add_widget(self.login_button)

    def sign_up(self, instance):
        self.clear_widgets()
        self.add_widget(UyeScreen(login_screen=self))

    def login(self, instance):
        self.clear_widgets()
        self.add_widget(GirisScreen(login_screen=self))

    def show_menu(self, email):
        self.clear_widgets()
        self.add_widget(MenuScreen(login_screen=self, email=email))

class UyeScreen(BoxLayout):
    def __init__(self, login_screen, **kwargs):
        super(UyeScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.login_screen = login_screen
        self.padding = 20
        self.spacing = 10
        self.background_color = (1, 1, 0, 1)

        image = Image(source="resim5.png", size_hint=(1, 1))
        self.add_widget(image)

        self.scrollview = ScrollView()
        self.add_widget(self.scrollview)

        self.layout = ScrollableBoxLayout(orientation="vertical", spacing=10)
        self.scrollview.add_widget(self.layout)

        self.name_input = TextInput(hint_text="Nick", background_color=(1, 1, 1, 1))
        self.layout.add_widget(self.name_input)

        self.email_input = TextInput(hint_text="Email", background_color=(1, 1, 1, 1))
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text="Password", password=True, background_color=(1, 1, 1, 1))
        self.layout.add_widget(self.password_input)

        self.sign_up_button = Button(text="Sign Up", on_release=self.sign_up)
        self.layout.add_widget(self.sign_up_button)

        self.back_button = Button(text="Back", on_release=self.back_to_login)
        self.layout.add_widget(self.back_button)

    def sign_up(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not self.is_valid_email(email):
            self.show_message("Please enter a valid email address.")
        elif not self.has_valid_email_domain(email):
            self.show_message("Enter a valid email domain.")
        elif self.check_existing_email(email) and self.check_existing_name(name):
            self.show_message("This email and nickname are already used.")
        elif self.check_existing_email(email):
            self.show_message("This email is already in use.")
        elif self.check_existing_name(name):
            self.show_message("This nickname has been taken before.")
        elif not self.is_valid_password(password):
            self.show_message("Password must be at least 8 characters and contain at least 1 capital letter.")
        else:
            user_data = {
                "nick": name,
                "email": email,
                "password": password,
                "friends": []
            }
            self.save_user_data(user_data)
            self.show_message("Successfully signed up.")
            self.clear_fields()

    def back_to_login(self, instance):
        self.login_screen.clear_widgets()
        self.login_screen.add_widget(LoginScreen())

    def is_valid_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email)

    def has_valid_email_domain(self, email):
        valid_domains = ["gmail.com", "hotmail.com", "yahoo.com"]
        domain = email.split("@")[-1]
        return domain in valid_domains

    def check_existing_email(self, email):
        query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result is not None

    def check_existing_name(self, name):
        query = "SELECT nick FROM users WHERE nick = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result is not None

    def is_valid_password(self, password):
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        return True

    def save_user_data(self, user_data):
        query = "INSERT INTO users (nick, email, password) VALUES (%s, %s, %s)"
        values = (user_data['nick'], user_data['email'], user_data['password'])
        cursor.execute(query, values)
        connection.commit()

    def clear_fields(self):
        self.name_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""

    def show_message(self, message):
        popup = Popup(title="Information", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class GirisScreen(BoxLayout):
    def __init__(self, login_screen, **kwargs):
        super(GirisScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.login_screen = login_screen
        self.padding = 20
        self.spacing = 10
        self.background_color = [1, 1, 1, 1]
        image = Image(source="resim4.png", size_hint=(1, 1))
        self.add_widget(image)

        self.scrollview = ScrollView()
        self.add_widget(self.scrollview)

        self.layout = ScrollableBoxLayout(orientation="vertical", spacing=10)
        self.scrollview.add_widget(self.layout)

        self.username_input = TextInput(hint_text="Email")
        self.layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Password", password=True, background_color=(1, 1, 1, 1))
        self.layout.add_widget(self.password_input)

        self.remember_me_layout = BoxLayout(orientation='horizontal', spacing=5)
        self.remember_me_label = Label(text="Remember Me", font_size="15sp", color=[0, .3, .9, 1], line_height=2)
        self.remember_me_layout.add_widget(self.remember_me_label)
        self.remember_me_checkbox = CheckBox(active=False)
        self.remember_me_layout.add_widget(self.remember_me_checkbox)
        self.layout.add_widget(self.remember_me_layout)

        self.login_button = Button(text="Login", background_color=[1, 1, 0, 1], on_release=self.login)
        self.layout.add_widget(self.login_button)

        self.back_button = Button(text="Back", background_color=[1, 1, 0, 1], on_release=self.back)
        self.layout.add_widget(self.back_button)

        self.store = JsonStore('user_data.json')
        if 'email' in self.store:
            self.username_input.text = self.store.get('email')['value']
            if 'password' in self.store:
                self.password_input.text = self.store.get('password')['value']

    def on_remember_me_checkbox(self, checkbox, value):
        if value:
            self.store.put('email', value=self.username_input.text)
            self.store.put('password', value=self.password_input.text)
        else:
            self.store.delete('email')
            self.store.delete('password')

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if self.check_credentials(username, password):
            self.show_message("Login successful.")
            self.clear_fields()
            self.show_menu(password)
        else:
            self.show_message("Invalid username or password.")

    def check_credentials(self, username, password):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        return result is not None

    def show_menu(self, email):
        self.login_screen.clear_widgets()
        self.login_screen.show_menu(MenuScreen)

    def back(self, instance):
        self.login_screen.clear_widgets()
        self.login_screen.add_widget(LoginScreen())
    def clear_fields(self):
        self.username_input.text = ""
        self.password_input.text = ""

    def show_message(self, message):
        popup = Popup(title="Information", content=Label(text=message), auto_dismiss=self.check_credentials, size_hint=(None, None), size=(400, 200))
        popup.open()

class MenuScreen(BoxLayout):
    def __init__(self, login_screen, email, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.login_screen = login_screen
        self.email = email
        self.padding = 20
        self.spacing = 10
        self.background_color = (1, 1, 0, 1)

        image = Image(source="resim3.png", size_hint=(1, 1))
        self.add_widget(image)

        self.label = Label(text="Anonymous World")
        self.add_widget(self.label)

        self.application_button = Button(text="Applications", background_color=[1, 0, -3, 1], on_release=self.application)
        self.add_widget(self.application_button)

        self.chat_button = Button(text="Chat", background_color=[1, 0, 2, 1], on_release=self.show_chat)
        self.add_widget(self.chat_button)

        change_bg_button = Button(text='Change Background Color', background_color=[1, 0, -3, 1], on_release=self.change_background_color)
        self.add_widget(change_bg_button)

        self.logout_button = Button(text="Logout", background_color=[1, 0, 2, 1], on_release=self.logout)
        self.add_widget(self.logout_button)

        self.exit_button = Button(text="Exit", background_color=[1, 0, -3, 1], on_release=self.exit)
        self.add_widget(self.exit_button)

        self.colors = [
            (1, 0, 0, 1),  # Kırmızı
            (0, 1, 0, 1),  # Yeşil
            (0, 0, 1, 1),  # Mavi
            (1, 1, 0, 1),  # Sarı
            (0, 1, 1, 1),  # Camgöbeği
        ]
        self.current_color_index = 0

    def application(self, instance):
        self.clear_widgets()
        self.add_widget(ApplicationScreen(login_screen=self.login_screen))

    def show_chat(self, email):
        self.clear_widgets()
        self.add_widget(ChatScreen(login_screen=self.login_screen, email=self.email))

    def logout(self, instance):
        self.clear_widgets()
        self.login_screen.clear_widgets()
        self.login_screen.add_widget(LoginScreen())  # LoginScreen'e dön

    def change_background_color(self, instance):
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        App.get_running_app().root_window.clearcolor = self.colors[self.current_color_index]

    def exit(self, instance):
        App.get_running_app().stop()

    def clear_fields(self):
        pass


class ApplicationScreen(BoxLayout):
    def __init__(self, login_screen, **kwargs):
        super(ApplicationScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.login_screen = login_screen
        self.padding = 20
        self.spacing = 10
        self.background_color = (1, 0, -3, 1)  # Açık Mavi arka plan

        image = Image(source="resim7.png", size_hint=(1, 1))
        self.add_widget(image)

        self.label = Label(text="Applications")
        self.add_widget(self.label)

        self.back_button = Button(text="Back", background_color=[1, 0, 2, 1], on_release=self.back)
        self.add_widget(self.back_button)

    def back(self, instance):
        self.clear_widgets()
        self.login_screen.clear_widgets()
        self.login_screen.show_menu(MenuScreen)
class ChatScreen(BoxLayout):
    def __init__(self, login_screen, email, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.login_screen = login_screen
        self.email = email  # Giriş yapan kullanıcının email adresini burada tutuyoruz
        self.padding = 20
        self.spacing = 10
        self.background_color = [1, 0, 2, 1]  # Mor arka plan

        image = Image(source="resim6.png", size_hint=(1, 0.5))
        self.add_widget(image)

        self.scrollview = ScrollView()
        self.add_widget(self.scrollview)

        self.layout = ScrollableBoxLayout(orientation="vertical", spacing=10)
        self.scrollview.add_widget(self.layout)

        menu_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.add_widget(menu_layout)

        self.chat_history = Label(text="", font_size="16sp", halign='left', size_hint=(1, None),
                                  text_size=(self.width - 20, None))
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.layout.add_widget(self.chat_history)

        self.message_input = TextInput(hint_text="Type your message...", multiline=False, size_hint=(1, None),
                                       height=50)
        self.layout.add_widget(self.message_input)

        self.send_button = Button(text="Send", on_release=self.send_message)
        self.layout.add_widget(self.send_button)

        self.direct_message_input = TextInput(hint_text="Kullanıcı adını girin", multiline=False, size_hint=(1, None),
                                              height=50)
        self.layout.add_widget(self.direct_message_input)

        self.send_direct_message_button = Button(text="Mesaj Gönder", on_release=self.send_direct_message_to_user)
        self.layout.add_widget(self.send_direct_message_button)

        friends_button = Button(text="Friends", on_release=self.show_friends)
        menu_layout.add_widget(friends_button)

        add_friends_button = Button(text="Add Friends", on_release=self.show_add_friends)
        menu_layout.add_widget(add_friends_button)

        friends_invites_button = Button(text="Friends Invites", on_release=self.show_friends_invites)
        menu_layout.add_widget(friends_invites_button)

        self.back_button = Button(text="Back", on_release=self.backm)
        self.layout.add_widget(self.back_button)

    def send_direct_message_to_user(self, instance):
        friend_nick = self.direct_message_input.text
        if friend_nick:
            self.send_direct_message(friend_nick)
        else:
            self.show_message("Lütfen mesaj göndermek istediğiniz kullanıcı adını girin.")
    def backm(self, instance):
        self.clear_widgets()
        self.login_screen.clear_widgets()
        self.login_screen.show_menu(MenuScreen)

    def clear_messages(self):
        self.chat_history.text = ""

    def get_email_by_username(self, username):
        query = "SELECT email FROM users WHERE nick = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    def send_direct_message(self, friend_nick):
        friend_email = self.get_email_by_username(friend_nick)
        if friend_email:
            message = self.message_input.text
            if message:
                self.chat_history.text += f"\nSiz {friend_nick} adlı arkadaşınıza: {message}"
                self.save_message_to_database(self.email, friend_email, message)
                self.message_input.text = ""
            else:
                self.show_message("Lütfen bir mesaj girin.")
        else:
            self.show_message(f"{friend_nick} adlı bir kullanıcı bulunamadı.")
    def get_username_by_email(self, email):
        query = "SELECT nick FROM users WHERE email = %s"
        cursor.execute = query, (email,)
        result = cursor.fetchone()
        return result[0] if result else "Anon"

    # noinspection PyArgumentList
    def send_message(self, instance):
        message = self.message_input.text
        if message:
            self.chat_history.text += f"\nSiz: {message}"
            self.save_message_to_database(self.login_screen.email, receiver_email=message)
            self.message_input.text = ""
        else:
            self.show_message("Lütfen bir mesaj girin.")

    def save_message_to_database(self, sender_email, receiver_email, message):
        if not message:
            return

        sender_nick = self.get_username_by_email(sender_email)
        receiver_nick = self.get_username_by_email(receiver_email)

        query = "INSERT INTO messages (sender_nick, receiver_nick, message) VALUES (%s, %s, %s)"
        values = (sender_nick, receiver_nick, message)
        cursor.execute(query, values)
        connection.commit()

    def show_friends(self, instance):
        query = "SELECT friends FROM users WHERE email = %s"
        cursor.execute = query, (self.email,)
        result = cursor.fetchone()

        if result:
            friends_list = result[0].split(',')
            self.clear_widgets()
            layout = BoxLayout(orientation='vertical')
            for friend in friends_list:
                friend_label = Label(text=friend)
                layout.add_widget(friend_label)

            back_button = Button(text="Back", on_release=self.back)
            layout.add_widget(back_button)
            self.add_widget(layout)
        else:
            self.clear_widgets()
            no_friends_label = Label(text="You don't have any friends.")
            back_button = Button(text="Back", on_release=self.back)
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(no_friends_label)
            layout.add_widget(back_button)
            self.add_widget(layout)

    def show_add_friends(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(None, None),
                                 size=(450, 250))

        label = Label(text="")
        popup_layout.add_widget(label)

        friend_nick_input = TextInput(hint_text="Friend's Nickname")
        popup_layout.add_widget(friend_nick_input)

        add_button = Button(text="Add Friend", size_hint=(1, 0.3), size=(1, 50),
                            on_release=lambda x: self.add_friend(friend_nick_input.text))
        popup_layout.add_widget(add_button)

        cancel_button = Button(text="Cancel", size_hint=(1, 0.3), size=(1, 50), on_release=self.dismiss_popup)
        popup_layout.add_widget(cancel_button)

        self._popup = Popup(title="Add Friend", content=popup_layout, size_hint=(None, None), size=(450, 250),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self._popup.open()

    def add_friend(self, friend_nick):
        query = "SELECT email FROM users WHERE nick = %s"
        cursor.execute(query, (friend_nick,))
        result = cursor.fetchone()

        if result:
            friend_email = str(result[0])
            cursor.execute("UPDATE users SET friend_invites = CONCAT(friend_invites, %s) WHERE email = %s",
                           ("," + friend_email,
                            str(self.email)))
            connection.commit()
            popup = Popup(title="Success", content=Label(text="Friend added successfully!"), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
        else:
            popup = Popup(title="Error", content=Label(text="Friend not found. Please enter a valid nickname."),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def show_friends_invites(self, instance):
        query = "SELECT friend_invites FROM users WHERE email = %s"
        cursor.execute(query, (str(self.email),))
        result = cursor.fetchone()

        if result:
            friend_invites = result[0].split(',')
            self.clear_widgets()
            layout = BoxLayout(orientation='vertical')
            for invite in friend_invites:
                invite_label = Label(text=invite)
                layout.add_widget(invite_label)

            back_button = Button(text="Back", on_release=self.back)
            layout.add_widget(back_button)
            self.add_widget(layout)
        else:
            self.clear_widgets()
            no_invites_label = Label(text="You don't have any friend invites.")
            back_button = Button(text="Back", on_release=self.back)
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(no_invites_label)
            layout.add_widget(back_button)
            self.add_widget(layout)

    def back(self, instance):
        self.clear_widgets()
        self.login_screen.clear_widgets()
        self.login_screen.show_menu(self.email)

    def dismiss_popup(self, instance=None):
        self._popup.dismiss()

    def show_message(self, message):
        popup = Popup(title="Information", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()



class MainApp(App):
    def build(self):
        login_screen = LoginScreen()
        return login_screen


if __name__ == "__main__":
    app = MainApp()
    app.run()
