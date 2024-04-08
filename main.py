from Code.MINOR_PROJECT_GUI import gui_maker
import traceback


try:
    gui_maker.main()
except Exception as ex:
    traceback.print_exc()