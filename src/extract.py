#!/usr/bin/env python3

import requests, os, json
from bs4 import BeautifulSoup

target_domain = 'https://www.fao.org/3/AC854T/'
output_dir = '/opt/app/mnt/data/site/'

def pull_file(uri:str, filepath:str):
    r = requests.get(uri,filepath)
    r.status_code
    with open(filepath,'w') as tw:
        tw.write(r.text)

def str_to_int(input_str:str):
    try:
        return int(input_str)
    except ValueError:
        if input_str == '-':
            return None

def transform_html_to_dict(filepath,food):
    html = ""
    with open(filepath) as tw:
        html = tw.read()
    soup = BeautifulSoup(html,'html.parser')
    row_index = 0
    item_number = 0
    food_name = ""
    look_for_cc = False
    look_for_B = False
    for tr in soup.body.table.findAll('tr'):
        division_index = 0
        tds = tr.findAll('td')
        ref_cell_contents = tds[0].getText()
        #print("\n\n-------\n{}".format(ref_cell_contents))
        #if ref_cell_contents == 'Item No.':
        #    print("-- {}".format(ref_cell_contents == 'Item No.'))
        if ref_cell_contents.isdigit():
            item_number = int(ref_cell_contents)
            food_name = tds[1].getText()
            look_for_cc = True
            look_for_B = True
            #print("--- {}".format(ref_cell_contents))
        elif ref_cell_contents == '(CC)':
            look_for_cc = False
        
        if look_for_cc == False and look_for_B ==True:
            if tds[6].getText() == 'B':
                look_for_B = False
                food[food_name] = {
                    "Isoleucine":str_to_int(tds[7].getText()),
                    "Leucine":str_to_int(tds[8].getText()),
                    "Lysine":str_to_int(tds[9].getText()),
                    "Methionine":str_to_int(tds[10].getText()),
                    "Cystine":str_to_int(tds[11].getText()),
                }
        #for td in tds:
        #    print("{}...{} --- {}".format(row_index, division_index, td.getText().strip()))
        #    division_index += 1
        row_index += 1
    #return food

def get_next_page_uri(filepath):
    with open(filepath) as tw:
        html = tw.read()
    soup = BeautifulSoup(html,'html.parser')
    for a in soup.body.p.findAll('a'):
        if a.img['alt'] == "Next Page":
            return a['href']


def derive_food():
    start_file = 'AC854T03.htm'
    next_file = start_file
    food = dict()

    while next_file != None:
        if not os.path.isfile(output_dir + next_file):
            pull_file(target_domain + next_file, output_dir + next_file)
        #print(next_file)
        transform_html_to_dict(output_dir + next_file, food)
        next_file = get_next_page_uri(output_dir + next_file)
    return food

def pull_food_cache(file_path):
    if not os.path.exists(file_path):
        food = derive_food()
        json_data = json.dumps(food,indent=4)
        del food
        with open(file_path, 'w') as file:
            file.write(json_data)

    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == '__main__':

    file_path = "/opt/app/mnt/data/temp.json"
    food2 = pull_food_cache(file_path)
    print(json.dumps(food2,indent=4))