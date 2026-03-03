import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from vitax import Vitax
from systemUI.home import HomeActivity

def main():
    vitax = Vitax()
    vitax.setActivity(HomeActivity())
    try:
        while 1:
            try:
                vitax.loop()
            except KeyboardInterrupt as e: # Close the program if we force it to stop.
                raise # Rethrow the same KeyboardInterrupt exception
            except Exception as e: # Vitax was unable to catch an exception. From this point on it is considered a critical system exception.
                print(e)
                status = vitax.handleCriticalException(e)
                if status == False: # Vitax couldn't deal with this exception.
                    print("CRITICAL EXCEPTION")
                    print("Better call support, not even I can handle this one!")
                    raise
                
    except KeyboardInterrupt:
        exit(-1)

if __name__ == "__main__":
    os.system('cls')
    main()
