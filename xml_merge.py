import sys
import re


from property_ql.utils.file_utils import *
from property_ql.utils.xml_utils import *


def validate_input_params(_params_):
    if len(_params_) < 2:
        print("Wrong input parameters")
        print("Expected parameters: {xml_file_1}, {xml_file_2}")
        print(_params_)
        sys.exit(1)
    else:
        print("xml file 1: " + _params_[1])
        print("xml file 2: " + _params_[2])


def has_childs(_elem_):
    if len(_elem_):
        return True
    else:
        return False


def replace_idx(_string_):
    return re.sub(r'\[\d+\]', '', _string_)


def contains_array_elem(_xpath_):
    regexp = re.compile(r'\[\d+\]')
    return  regexp.search(_xpath_)


def print_xml(_element_):
    return etree.tostring(_element_, encoding='unicode')


def print_xml_array(_array_):
    return ','.join(map(print_xml, _array_))


def copy_xml_element(_elem_):
    new_element = etree.Element(_elem_.tag, _elem_.attrib)
    for child in _elem_:
        new_element.append(copy_xml_element(child))
    new_element.text = _elem_.text
    new_element.tail = _elem_.tail
    return new_element


def update_element(xpath, new_value):
    element.text


def insert_element(parent_element, new_element):
    parent_element.append(new_element)



if __name__ == '__main__':

    validate_input_params(sys.argv)

    file_path_1= sys.argv[1]
    file_path_2 = sys.argv[2]

    xml_tree1 = read_xml_file(file_path_1)
    xml_tree2 = read_xml_file(file_path_2)

# 1. ==================Go trough xml tree approach===================================
#     for elem in xml_tree2.getroot():
#
#         elem_xpath = xml_tree2.getpath(elem)
#         if contains_array_elem(elem_xpath):
#             elem_xpath = replace_idx(elem_xpath)
#
#         print(f"Checking element: {elem_xpath}")
#
#         #source_elem = xml_tree1.xpath(elem_xpath)
#
#         found_elements = xml_tree1.findall(elem.tag)
#         for source_elem in found_elements:
#
#             for i in elem:
#                 i.tag
#
#             print(print_xml(source_elem))


        # if source_elem:
        #     print(f"Element found: {elem_xpath}")


# 2.  ============== Use xpath list======================================

    tree2_elements = xml_tree2.xpath('//*')

    xpath_list = []
    to_merge_map = {}

    # Collect map of merged values
    for elem in tree2_elements:

        xpath = xml_tree2.getpath(elem)
        value = elem.text.strip() if elem.text else ""

        # Collect element tags with values ===================
        if value:
            val = {'xpath': xpath, 'value': value}
            xpath_list.append(val)

            #----- Group By block todo move to functions
            parent_xpath = xml_tree2.getpath(elem.getparent())
            if to_merge_map.get(parent_xpath):
                vals = to_merge_map.get(parent_xpath)
                vals.append(val)
                to_merge_map[xml_tree2.getpath(elem.getparent())] = vals
            else:
                to_merge_map[xml_tree2.getpath(elem.getparent())] = [val]
            #-----

        # Collect element attributes ===================
        for attrib in elem.attrib:
            xpath = xml_tree2.getpath(elem) + "/@" + attrib
            value = elem.get(attrib)
            val = {'xpath': xpath, 'value': value}
            xpath_list.append(val)

            #----- Group By block todo move to functions
            parent_xpath = xml_tree2.getpath(elem.getparent())
            if to_merge_map.get(parent_xpath):
                vals = to_merge_map.get(parent_xpath)
                vals.append(val)
                to_merge_map[xml_tree2.getpath(elem.getparent())] = vals
            else:
                to_merge_map[xml_tree2.getpath(elem.getparent())] = [val]
            #-----

    # Processing values to merge
    for entry in to_merge_map:
        search_elem = entry.replace('/Properties','') #todo re-do .replace('/Properties','')

        if contains_array_elem(search_elem):
            search_elem = replace_idx(search_elem)

        target_elements = xml_tree1.findall(search_elem)
        entry_values = to_merge_map.get(entry)

        matching_elements = []

        for te in target_elements:

            # print("checking elem:")
            # print(print_xml(te))

            found = False
            missing_elements = []

            for merge_elem in entry_values:
                cv = xml_tree2.xpath(merge_elem.get('xpath'))[0]
                child = te.find(cv.tag)
                if child.text == merge_elem.get('value'):
                    matching_elements.append(te)
                # else:
                #     missing_elements.append(cv)


        if len(matching_elements) == 1 : # Update
            element = matching_elements[0]

            for merge_elem in entry_values:
                cv = xml_tree2.xpath(merge_elem.get('xpath'))[0]
                child = element.find(cv.tag)
                if child is not None:
                    if child.text != merge_elem.get('value'):
                        child.text = merge_elem.get('value')
                else:
                    new_element = copy_xml_element(cv)
                    element.append(new_element)

        else:  # Insert?
            parent_element = target_elements[0].getparent()
            new_element = xml_tree2.xpath(entry)[0]
            parent_element.append(copy_xml_element(new_element))



        # print("missing elements:")
        # print(print_xml_array(missing_elements))
















    # for elem_xpath in xpath_list:
    #
    #     #todo group by
    #     search_elem = elem_xpath.get('xpath').replace('/Properties','') #todo re-do .replace('/Properties','')
    #     if contains_array_elem(search_elem):
    #         search_elem = replace_idx(search_elem)
    #
    #     source_elements = xml_tree1.findall(search_elem)
    #
    #     found_elem = None
    #     print(f"Processing {elem_xpath}")
    #     for e in source_elements:
    #         if e.text == elem_xpath.get('value'):
    #             found_elem = e
    #             print(f"Found element to merge")
    #             print_xml(found_elem)
    #             break
    #
    #
    #     if found_elem:
    #         #print(f"Processing {elem_xpath.get('xpath')}")
    #         merge_elem = copy_xml_element(xml_tree2.xpath(elem_xpath.get('xpath'))[0].getparent())
    #         tobe_removed = e.getparent()
    #         parent_elem = tobe_removed.getparent()
    #         parent_elem.remove(tobe_removed)
    #         parent_elem.append(merge_elem)
    #         break






    print(print_xml(xml_tree1))

    xml_tree1.write('merged.xml')


    #     xpath_array = elem.get('xpath').split("/")
    #     found = xml_tree1.xpath("/"+elem)









        # for elem in xpath_array:
        #     found = xml_tree1.xpath("/"+elem)

        #print(f"{ elem.get('xpath') } : { elem.get('value') }")