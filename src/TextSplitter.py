import os

class TextSplitter:
    def __init__(self, semantic_text_splitter, output_folder):
        self.semantic_text_splitter = semantic_text_splitter
        self.output_folder = output_folder

    def split_text(self, text, file_name):
        chunks = self.semantic_text_splitter.split_text(text)

        for chunk in chunks:
            file_path = os.path.join(self.output_folder, f"{file_name}_{chunks.index(chunk)}.txt")

            with open(file_path, "w") as f:
                f.write(chunk)

    def split_text_from_folder(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith('.txt'):
                with open(file_path, "r") as f:
                    text = f.read()
                    self.split_text(text, file_name)
            else:
                print(f"Skipping non-text file: {file_name}")
