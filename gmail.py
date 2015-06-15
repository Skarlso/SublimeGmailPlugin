import sublime
import sublime_plugin
import smtplib
import sys


class GmailCommand(sublime_plugin.TextCommand):
    to = "example@gmail.com"
    text = "selected text"

    def on_done(self, user_input):
        self.send_gmail(user_input, text)

    def send_gmail(self, to, text):
        gmail_user = "gmail_user"
        gmail_pwd = "gmail_pwd"
        g_from = 'g_from'
        g_to = ['%s' % to]  # from input
        g_sign = "Sent from sublime text"
        g_text = text

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (g_from, ", ".join(g_to), g_sign, g_text)

        try:
            # server = smtplib.SMTP(SERVER)
            # or port 465 doesn't seem to work!
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(g_from, g_to, message.encode('utf8'))
            # server.quit()
            server.close()
            sublime.status_message("Email sent successfully to: %s" % to)

        except:
            sublime.status_message(
                "There was an error sending the email to: %s " %
                sys.exc_info()[0])

    def run(self, edit):
        global text
        global to
        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                text = self.view.substr(region)
                self.view.window().show_input_panel(
                    "To:", 'email@gmail.com', self.on_done, None, None)
