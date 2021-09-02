from kivymd.uix import screen
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (350, 600)
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
import smtplib
import re
#########################################
class EmailApp(MDApp):
    def new_email(self):
        self.input_email.text = ''
        self.input_body.text = ''
        self.label1.text = ''
        self.label2.text = ''

    def check_before_send(self, args):
        self.label1.text = ''
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex_email, self.input_email.text) and self.input_body.text != '':
            self.send()
        elif re.match(regex_email, self.input_email.text) and self.input_body.text == '':
            self.label1.theme_text_color = 'Error'
            self.label1.text = 'Please enter a message'
        else:
            self.label1.theme_text_color = 'Error'
            self.label1.text = 'Invalid email address'

    def send(self):
        self.label1.text = ''
        smtp_object = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_object.ehlo()
        email = 'ADD EMAIL HERE'
        password = 'ADD PASSWORD HERE'
        smtp_object.login(email,password)
        from_address = email
        subject = "Jerry's Email App"
        msg = "Subject: "+subject+'\n'+self.input_body.text+'\n\n\n\n\n\n'+"This message was sent from Jerry's Email App, created using Python. \n\nDeveloper email address: ***"
        smtp_object.sendmail(from_address,self.input_email.text,msg)
        self.label2.text = 'Message sent!'

    def build(self):
        self.theme_cls.primary_palette = 'DeepOrange'
        screen = MDScreen()
        self.toolbar = MDToolbar(title="Send an email")
        self.toolbar.pos_hint = {'top': 1}
        self.toolbar.right_action_items = [['email-edit-outline', lambda x: self.new_email()]] #DOUBLE LIST BRACKETS - check again
        screen.add_widget(self.toolbar)

        #logo
        screen.add_widget(Image(
            source='jerry.png',
            pos_hint = {'center_x':0.5, 'center_y':0.75}
            ))

        #collect recipient email address
        self.input_email = MDTextField(
            hint_text = 'email address',
            halign = 'center',
            size_hint = (0.8,1),
            pos_hint = {'center_x':0.5, 'center_y':0.55},
            font_size = 18,
            write_tab = False,
            on_text_validate = self.check_before_send # this was hard to find! on_text_validate is when the user hits ‘enter’ :-)
        )
        screen.add_widget(self.input_email)

        #collect email message body
        self.input_body = MDTextField(
            hint_text = 'message',
            halign = 'center',
            size_hint = (0.8,1),
            pos_hint = {'center_x':0.5, 'center_y':0.4},
            font_size = 18,
            write_tab = False,
            on_text_validate = self.check_before_send
        )
        screen.add_widget(self.input_body)

        #label to inform user of sent or error
        self.label1 = MDLabel(
            # text = 'Please check and try again', #(place holder text for testing)
            halign = 'center',
            size_hint = (0.8,1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.32},
            theme_text_color = 'Error'
        )

        self.label2 = MDLabel(
            # text = 'message sent!', #(place holder text for testing)
            halign = 'center',
            pos_hint = {'center_x': 0.5, 'center_y': 0.25},
            theme_text_color = 'Primary',
            font_style = 'H5'
        )
        screen.add_widget(self.label1)
        screen.add_widget(self.label2)

        #send button
        screen.add_widget(MDFillRoundFlatButton(
            text = 'Send',
            font_size =17,
            pos_hint = {'center_x': 0.5, 'center_y': 0.15},
            on_press = self.check_before_send
        ))

        return screen

if __name__ == '__main__':
    EmailApp().run()