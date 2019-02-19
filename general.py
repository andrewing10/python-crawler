import os
import json

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

# Read querylinks.html to generate all html links to crawl
def generate_urls(project_name, base_url, file_name):
    results = []
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name , 'crawled.txt')
    data_file = os.path.join(project_name , 'toto.txt')
    delete_file_contents(queue)
    delete_file_contents(crawled)
    delete_file_contents(data_file)

    with open(file_name, 'r') as f:
        lines = f.readlines()
        html_mark = 'option'
        for line in lines:
            if html_mark in line:
                # The other way I will use is to split by 'sppl', will have more than one line. pending
                new_url = base_url + line[25: 50]
                results.append(new_url)
                append_to_file(queue, new_url)
    return results

# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Add data onto an existing file
def append_json_to_file(path, data):
    with open(path, 'a') as file:
        file.write(json.dumps(data) + ',\n')

# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")