import time
path_log_txt = r"/src/run/others/log.txt"

def write_log(text_log):
        with open(path_log_txt, 'a') as f:
            f.write(str(text_log)+"\n")
