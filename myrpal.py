import argparse 
import re

class FileParser:

    def __init__(self) -> None:
        self.file = None
        self.file_name = None

    def get_filename(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="Enter the filename")
        args = parser.parse_args()
        return args.filename.strip()
    
    def open_file(self):
        self.file =  open(self.file_name, "r")

    def get_file_content(self):
        return self.file.read()
    

    
    def run(self):
        self.file_name = self.get_filename()
        self.open_file()
        content = self.get_file_content()
        print(content)
        self.file.close()
    


def main():
    fileParser = FileParser()

    fileParser.run()

if __name__ == "__main__":
    main()