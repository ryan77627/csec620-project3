import json
import csv
import ipaddress

# File paths
input_file = 'out.json'  # Input JSON file
output_file = 'revised_labeled_flows.csv'  # Output CSV file

# Define the internal subnet and specific IP mappings
internal_subnet = ipaddress.ip_network('192.168.105.0/24')
specific_labels = {
    '192.168.105.54': 'Realm',
    '192.168.105.55': 'Sliver',
    '192.168.105.56': 'HeadHunter'
}

# Read the JSON file
with open(input_file, 'r') as f:
    data = [json.loads(line) for line in f]

# Define relevant keys and relabel the flows
keys = ['sa', 'da', 'pr', 'sp', 'dp', 'bytes_out', 'num_pkts_out', 'time_start', 'time_end', 'label']
labeled_data = []

for entry in data:
    # Ensure the necessary fields are present in the entry
    if 'sa' in entry and 'da' in entry:
        sa, da = entry['sa'], entry['da']
        sa_in_subnet = ipaddress.ip_address(sa) in internal_subnet
        da_in_subnet = ipaddress.ip_address(da) in internal_subnet

        # Determine the label based on criteria
        if sa in specific_labels and da_in_subnet:
            entry['label'] = specific_labels[sa]
        elif da in specific_labels and sa_in_subnet:
            entry['label'] = specific_labels[da]
        else:
            entry['label'] = 'benign'  # Default label for other traffic

        # Add the labeled entry with selected fields to the list
        labeled_entry = {key: entry.get(key, None) for key in keys}
        labeled_data.append(labeled_entry)

# Write the labeled data to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(labeled_data)

print(f"Revised labeled CSV file written to {output_file}")

