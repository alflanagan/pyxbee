from functools import wraps
import inspect

def print_call(f):
    sig = inspect.signature(f)
    called_name = f.__name__
    called_params = sig.parameters
    #oh, this is beautiful
    @wraps(f)
    def wrapper(*args, **kwargs):
        #Prints the function name of its caller, with args
        #arg to stack() is # of lines of context to include (not well documented)
        s = inspect.stack(0)
        #print(s[1])
        caller_name = s[1][3]
        caller_frame = s[1][0]
        #print([x for x, y in inspect.getmembers(caller_frame)])
        params = [str(x) for x in args]
        kwdparams = []
        for key in kwargs:
            kwdparams.append("{}={}".format(str(key), str(kwargs[key])))
        kwd_string = ', '.join(kwdparams)
        outstr = caller_name + " called " + called_name + "(" + ', '.join(params)
        if kwdparams:
            if params:
                outstr += ", " + kwd_string
            else:
                outstr += kwd_string
        outstr += ")"
        print(outstr)
        return f(*args, **kwargs)
    return wrapper
