import warnings
from tkinter import messagebox



class errorHandler:
    """
    the methods cliErrorDisplay and visualErrorDisplay take the error print from an exception, aswell as a custom message, personally written by me to specify what triggered 
    the error, without overloading the user with documention.
    """



    def cliErrorDisplay(customMessage, error):
        warnings.warn(customMessage,error)



    def visualErrorDisplay(customMessage, error)
        messagebox.showerror("Error", customMessage, detail=error)

