"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""
import re
from threading import Thread
from ui.run_action import RunActionDialog
try:
    import scripts # @UnresolvedImport
except ModuleNotFoundError:
    scripts = None

class RunContext():
    """ Object contains everything that an action script can use to interact with the rest of
        the program
    """

    def __init__(self, parent, list_widget_item):
        self.serial = parent.serial
        self.terminal = parent.com_traffic
        self.script = None
        self.parent = parent

        replacement = {"<cr>":"\r", "<lf>":"\n"}

        self.action = list_widget_item.action
        for r in replacement:
            self.action = re.sub(r, replacement[r], self.action, re.IGNORECASE)

        # check for "run script" directive
        mrun = re.match("<run\s*\((.*)\)>", self.action, re.IGNORECASE)
        if mrun:
            if scripts == None:
                self.terminal.append_blue_text(f"Scripts.py not found to {mrun.group(0)}\n")
                return
            self.script = mrun.group(1)
        self.name = list_widget_item.text()

    def perform_action(self):
        ''' Perform the action in the action list item '''
        if self.script != None:
            self.run_action_in_background()
            return

        # basic operation writes text to the UART
        self.serial.write(self.action)
        self.terminal.write(self.action)

    def run_action_in_background(self):

        self.dialog = RunActionDialog(self.parent, self.name)
        self.dialog.start()
        run_thread = Thread(target = self.update_mode_thread)
        run_thread.daemon = True
        run_thread.start()

        # this will block until the dialog closes
        self.dialog.exec()

    def update_mode_thread(self):
        """ Thread which runs the action script. """
        getattr(scripts, self.script)(self.serial, self.terminal, self.dialog)
        self.dialog.percent_complete = 100

