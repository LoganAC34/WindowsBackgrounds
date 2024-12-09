from wxglade.wxRenameDialog import *


class RenameDialog(wxRenameDialog):
    def __init__(self, parent, existing_name, *args, **kwds):
        wxRenameDialog.__init__(self,  parent, *args, **kwds)

        self.parent = parent
        self.existing_name = existing_name
        self.text_ctrl_1.SetLabelText(self.existing_name)

    def on_text(self, event):
        self.label_warning.SetLabelText("")

    def on_cancel(self, event):
        #print("Event handler 'on_cancel' not implemented!")
        self.on_close(event)

    def on_apply(self, event):
        #print("Event handler 'on_apply' not implemented!")
        new_name = self.text_ctrl_1.GetValue().strip()

        tabCount = self.parent.notebook_1.GetPageCount()
        used_profile_names = []
        for x in range(0, tabCount):
            tab_name = self.parent.notebook_1.GetPageText(x)
            used_profile_names.append(tab_name)

        if new_name not in used_profile_names or new_name == self.existing_name:
            self.parent.profile_rename(new_name)
            self.on_close(event)
        else:
            self.label_warning.SetLabel("Profile name already taken!")

    def on_close(self, event):
        self.parent.Enable()
        self.Destroy()
        event.Skip()
