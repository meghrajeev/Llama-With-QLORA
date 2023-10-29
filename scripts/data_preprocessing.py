import re
import os

def clean_conversations(filename, output_dir):

    date_pattern = re.compile(r'\[\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[APMapm]{2}\]')

    with open(filename, 'r', encoding='utf-8') as file:
        contents = file.read()
    
    cleaned_contents = date_pattern.sub('', contents)
    
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.basename(filename)
    cleaned_base_name = 'cleaned' + base_name
    output_filename = os.path.join(output_dir, cleaned_base_name)
    
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(cleaned_contents)

def main():
    input_dir = 'data/raw_data'
    output_dir = 'data/preprocessed_data'
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            full_path = os.path.join(input_dir, filename)

            clean_conversations(full_path, output_dir)

if __name__ == "__main__":
    main()


