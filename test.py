import csv
import json

def extractDir(crew):
  # Assuming 'crew_data' contains the string data you provided
  #crew_data = "[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]"

  # Remove square brackets and curly braces from the string
  crew_data = crew.replace("[", "").replace("]", "").replace("{", "").replace("}", "")

  # Split the string into a list of key-value pairs
  key_value_pairs = [pair.strip() for pair in crew_data.split(",")]
  #print(key_value_pairs)
  # Extract the 'name' values from each pair and remove single quotes
  crew_names = []
  director = False

  for pair in key_value_pairs:
    if "name" in pair:
        crew_names.append(pair.split(":")[1].strip().replace("'", ""))

  # Join the crew names with commas
  crew_names_string = ', '.join(crew_names)

  # Print the crew names without any extra characters
  print(crew_names_string)
  #cast_data = json.loads(cast_data)
  #names = [actor['name'] for actor in cast_data] 
  #print(names) 


def display_csv_column(file_path, column_index, limit):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        row_count = 0
        for row in csv_reader:
            if len(row) > column_index:
                extractDir(row[column_index])
                #print(row[column_index])
                row_count += 1
                if row_count >= limit:
                    break



file_path = 'movies_metadata.csv'
column_index = 13
limit = 10  

display_csv_column(file_path, column_index, limit)
