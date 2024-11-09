from ..modules import *

def signal_handler(sig, frame):
    from ..pm_behaviours import pm_on_stop
    
    threading.Thread(target = pm_on_stop, args = ()).start()

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')