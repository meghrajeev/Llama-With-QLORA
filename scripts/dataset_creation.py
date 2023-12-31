import json
import csv
import argparse
import os
def process_conversation(folder_path, json_path, user_name):
    csv_file_name = f"{json_path}/AllChats.csv"
    json_file_name = f"{json_path}/AllChats.json"
    dataset = []

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            json_file_path = os.path.join(folder_path, file)
            friend_name = file.replace("Chat.json", "")
            
            # Construct the formatted name string for the friend
            formatted_friend_name = f'Friend ({friend_name})'
            
            # Load the conversation from the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                conversation = json.load(json_file)

            for i in range(len(conversation)):
                response_dict = conversation[i]
                if list(response_dict.keys())[0] != user_name:  # Skip if the message is not from the user
                    continue
                # Skip if the message only contains white characters
                if not list(response_dict.values())[0].strip():
                    continue
                context_start = max(0, i - 5)
                context = conversation[context_start:i]
                context_text = '\n'.join([f"{list(item.keys())[0]}: {list(item.values())[0]}" for item in context])
                instruction_text = f"{list(context[-1].keys())[0]}: {list(context[-1].values())[0]}"
                response_text = f"{list(response_dict.values())[0]}"
                dataset.append({
                    'instruction': instruction_text,
                    'context': context_text,
                    'response': response_text
                })
    with open(json_file_name, 'w', encoding='utf-8') as jsonfile:
      json.dump(dataset, jsonfile, ensure_ascii=False, indent=4)

    def format_row(row):
      formatted_str = f"### Instruction:\n{row['instruction']}\n### Context:\n{row['context']}\n### Response:\n{row['response']}"
      return formatted_str

    # Update each row in the dataset with the formatted string
    for row in dataset:
      row['formatted'] = format_row(row)

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as f:
      # Include 'formatted' in the list of fieldnames
      fieldnames = ['instruction', 'context', 'response', 'formatted']
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for row in dataset:
          writer.writerow(row)
    

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process a conversation and write to a CSV file.')
    parser.add_argument('folder_path', help='The folder that contains the JSON file containing the conversation.')
    parser.add_argument('csv_path', help='The name of the CSV file to write the dataset to.')
    parser.add_argument('user_name', help="The name of the user in the conversation.")
    
    args = parser.parse_args()
    
    # Call the function with the arguments
    process_conversation(args.folder_path, args.csv_path, args.user_name)
