from config.index import INPUT_PATH, OUTPUT_PATH

class FileHandler:
    @staticmethod
    def process_files(process_line_function):
        with open(INPUT_PATH, 'r', encoding='utf-8') as f_in, \
            open(OUTPUT_PATH, 'w', encoding='utf-8') as f_out:

            for line in f_in:
                processed_line = process_line_function(line.rstrip('\n'))
                f_out.write(f"{processed_line}\n")