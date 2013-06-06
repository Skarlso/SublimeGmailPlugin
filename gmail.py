import sublime, sublime_plugin, smtplib

class GmailCommand(sublime_plugin.TextCommand):
    to = "example@gmail.com"
    text = "selected text"

    def on_done(self, user_input):
        self.send_gmail(user_input, text)

    def send_gmail(self, to, text):
        gmail_user = "your@gmail.com"
        gmail_pwd = "yourpassword"
        FROM = 'your@gmail.com'
        TO = ['%s' % to] # from input
        SUBJECT = "Sent from sublime text"
        TEXT = text

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        try:
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            #server.quit()
            server.close()
            sublime.status_message("Email sent successfully to: %s" % to)
        except:
            sublime.status_message("There was an error sending the email to: %s " % to)


    def run(self, edit):
        global text
        global to
        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                text = self.view.substr(region)
                self.view.window().show_input_panel("To:", 'email@gmail.com', self.on_done, None, None)
