from bs4 import BeautifulSoup 
import csv
import urllib2
from lxml import etree 
import os

script_dir = os.path.dirname(__file__) 
vra_xpath = os.path.join(script_dir, 'vra_xpath.txt')
next_gen_pred = os.path.join(script_dir, 'dc_term_map.txt')
next_gen_fields = os.path.join(script_dir, 'next_gen_field.txt')

def parse_pid(pid):
    """ parse throught the vra and get the necessary data"""
    images_xpath = get_list(vra_xpath)  
    url = "%s%s%s" %("http://images.northwestern.edu/technical_metadata/", pid, "/VRA")
    namespaces = {"vra":"http://www.vraweb.org/vracore4.htm"}
    print 'working on ... %s' %url
    tree = etree.parse(url)
    tree.getroot()
    items = [url]
    for field in images_xpath:
        items.append(tree.xpath(field, namespaces=namespaces))
    return items

def iterate_pids(pids):
    """ Iterate through pidlist return a list of lists"""
    return [parse_pid(pid) for pid in pids]

def save_csv(name_of_file, list_of_data):
    """ put headers in and save it"""
    import csv
    output = open(name_of_file, 'wb')
    writer = csv.writer(output)
    writer.writerow(["url"]+get_list(next_gen_fields))
    writer.writerow(["url"]+get_list(vra_xpath))
    writer.writerow(["url"]+get_list(next_gen_pred))

    for row in list_of_data:
        writer.writerow(row)

def get_list(csv_file):
    """turn a list of items into a, well list. Used for PIDs, vra fields, and headers"""
    f = open(csv_file, 'r').read()
    # Note, pop the last one to ensure no errors. 
    return f.split('\n')[:-1]

test_pids = get_list('/Users/dsc712/Desktop/casas.csv')
save_csv('test.csv', iterate_pids(test_pids))