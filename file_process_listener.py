import os
import time
import shutil
import argparse
from pathlib import Path
import schedule
import sys

class FileProcessorSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, directory):
        if not hasattr(self, 'initialized'):
            self.directory = Path(directory)
            self.initialized = True

            # Create subdirectories if they don't exist
            (self.directory / '_processing').mkdir(exist_ok=True)
            (self.directory / 'processed').mkdir(exist_ok=True)

    def check_for_files(self):
        for file in self.directory.glob('*.csv'):
            self.process_file(file)

    def process_file(self, file):
        # Move the file to _processing directory
        processing_path = self.directory / '_processing' / file.name
        shutil.move(str(file), processing_path)
        print(f"Processing file {processing_path.name}...")

        # Simulate processing (you can replace this with actual processing logic)
        time.sleep(1)

        print(f"Done processing file {processing_path.name}...")

        # Move the file to processed directory
        processed_path = self.directory / 'processed' / processing_path.name
        shutil.move(str(processing_path), processed_path)

    def start(self):
        self.check_for_files()

def main():
    parser = argparse.ArgumentParser(description="Monitor a directory for CSV files and process them.")
    parser.add_argument('directory', type=str, help="Directory to monitor")
    parser.add_argument('interval', type=int, help="File check interval in minutes")

    args = parser.parse_args()

    processor = FileProcessorSingleton(args.directory)

    # Schedule the task using the schedule package
    schedule.every(args.interval).minutes.do(processor.start)

    print(f"Monitoring directory: {args.directory} every {args.interval} minutes.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
