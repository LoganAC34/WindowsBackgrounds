from Project.bin.wxglade.wxWarningDialog import *


class WarningDialog(wxWarningDialog):
    def __init__(self, parent, message_type: int, title: str, message: str, function_yesok=None, *args, **kwds):
        """
        Class for displaying warning message and a return function if the user clicks "Yes" or "OK".
        :param parent: self
        :param message_type: 1 - "OK" button | 2 - "Yes" & "No" buttons
        :param title: Warning title
        :param message: Warning body text
        :param function_yesok: Function for warning message to run on "Yes" or "OK" buttons.
        :param args:
        :param kwds:
        """
        wxWarningDialog.__init__(self,  parent, *args, **kwds)

        self.parent = parent
        self.message_type = message_type
        self.label_title.SetLabelText(title)
        self.label_message.SetLabelText(message)
        self.function_yesOk = function_yesok

        if message_type == 1:
            self.button_OK.Show()
        elif message_type == 2:
            self.button_YES.Show()
            self.button_NO.Show()

        self.Fit()


    def on_yesOk(self, event):
        #print("Event handler 'on_yesOk' not implemented!")
        self.function_yesOk()
        self.Destroy()
        event.Skip()

    def on_noCancel(self, event):
        #print("Event handler 'on_noCancel' not implemented!")
        self.parent.Enable()
        self.Destroy()
        event.Skip()
