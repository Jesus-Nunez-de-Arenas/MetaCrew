from datetime import datetime
import os
import sys

class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()  # Ensure immediate writing

    def flush(self):
        for stream in self.streams:
            stream.flush()


def create_log_folder():
    """
    Create a log folder with the current date and time.
    """
    now = datetime.now()
    
    log_dir = os.path.join('logs', now.strftime('%Y-%m-%d'), now.strftime('%H'))
    
    os.makedirs(log_dir, exist_ok=True)
    
    return log_dir


def create_log_file(log_dir):
    """
    Create a log file with a timestamp.
    """
    log_file_path = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    log_file = open(log_file_path, 'w')
    
    return log_file, log_file_path


def setup_logging():
    """
    Set up logging by creating a log folder, log file, and redirecting stdout and stderr.
    Returns the log file and its path.
    """
    log_dir = create_log_folder()
    log_file, log_file_path = create_log_file(log_dir)
    redirect_stdout_stderr(log_file)
    return log_file, log_file_path


def redirect_stdout_stderr(log_file):
    """
    Redirect stdout and stderr to the log file.
    """
    sys.stdout = Tee(sys.stdout, log_file)
    sys.stderr = Tee(sys.stderr, log_file)
    
    log_file.write(f"Log started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.flush()  # Ensure immediate writing


def close_log_file(log_file):
    """
    Close the log file and restore stdout and stderr.
    """
    if log_file and not log_file.closed:
        log_file.write(f"Log ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
