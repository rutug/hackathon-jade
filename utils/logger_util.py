import os
import sys
from pathlib import Path
import traceback
from loguru import logger

# First, remove the default handler
logger.remove()

# Add a basic console handler that will always work
try:
    logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
except Exception as e:
    print(f"Error adding stderr logger: {e}")


def get_executable_directory():
    """
    Get the directory where the executable (or script) is located.
    """
    try:
        if getattr(sys, 'frozen', False):
            # Running as executable
            # sys.executable points to the .exe file
            executable_dir = Path(sys.executable).parent
        else:
            # Running in development mode
            # Use the parent directory of the directory containing this file
            executable_dir = Path(__file__).parent.parent
            
        return executable_dir
    except Exception:
        # In case of any errors, print the traceback to stdout for debugging
        print(f"Error determining executable directory: {traceback.format_exc()}")
        # Fall back to current working directory
        return Path(os.getcwd())

try:
    # Get executable directory and create logs subdirectory
    exe_dir = get_executable_directory()
    logs_dir = exe_dir / "logs"
    
    # Create the logs directory - with explicit error checking
    try:
        if not logs_dir.exists():
            print(f"Creating logs directory at: {logs_dir}")
            logs_dir.mkdir(exist_ok=True)
        
        # Verify we can write to the directory by creating a test file
        test_file = logs_dir / "test_write.tmp"
        test_file.write_text("Test")
        test_file.unlink()  # Remove the test file
        
        print(f"Successfully verified write access to: {logs_dir}")
    except Exception as e:
        print(f"Error creating or writing to logs directory: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise
    
    # Now add the file handlers
    logger.add(
        logs_dir / "debug.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        enqueue=True,  # Use a queue for thread safety
        diagnose=True,  # Include variables in traceback
        backtrace=True,  # Extend traceback
        catch=True,     # Catch exceptions
    )
    
    logger.add(
        logs_dir / "info.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        enqueue=True,
        diagnose=True,
        backtrace=True,
        catch=True,
    )
    
    logger.add(
        logs_dir / "error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="3 months",
        compression="zip",
        enqueue=True,
        diagnose=True,
        backtrace=True,
        catch=True,
    )
    
    # Log success information
    print(f"Logger initialized with logs directory: {logs_dir}")
    logger.info("Logger initialized")
    logger.info(f"Executable directory: {exe_dir}")
    logger.info(f"Logs directory: {logs_dir}")

except Exception as e:
    # Last resort error handling
    print(f"CRITICAL ERROR in logger initialization: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    print("Continuing with console logging only")