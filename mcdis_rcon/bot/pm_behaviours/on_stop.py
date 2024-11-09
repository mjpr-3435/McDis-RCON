from ..pm_functions import *
from ..pm_classes import *
from ..modules import *

from ..loader import _, panel, config
from ..pm_loader import networks, servers, processes

def pm_on_stop():
    any_process_open = lambda: any([process.state() in ['Open', 'Initializing'] for process in processes])
    
    if any_process_open():
        print(_('Closing processes...'))

        for process in processes:
            process.stop(omit_tasks=True)
        
        i = 60
        while i > 0 and any_process_open():
            print(_('Processes will be forcibly closed in {} seconds...').format(i))
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
            i -= 1
            time.sleep(1)
            
        if any_process_open():
            for process in processes:
                process.kill()
            
            print(_('Processes forcibly closed.'))
        else:
            print(_('Processes closed.'))
    os._exit(0)