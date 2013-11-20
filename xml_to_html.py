import sys
import xml.etree.ElementTree as ET

LINE_THRESHOLD = 10
TEXT_MATCHES = [".//HedLine_hl1/*/*", ".//Content/*/*"]
TEXT_NODES = ['W','Q']

def parse_text_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    lines_list = []
    temp_line = []
    last_y = None
    
    
    for match in TEXT_MATCHES:
        for node in root.findall(match):
            if node.tag in TEXT_NODES:
                left_x , top_y , right_x , bottom_y = [int(s) for s in node.attrib['BOX'].split()]
                if (last_y is not None) and (top_y - LINE_THRESHOLD > last_y):
                    lines_list.append(temp_line)
                    temp_line = []
                temp_line.append(node.text)
                last_y = top_y
        
    lines_list.append(temp_line)
    
    result = "<html><head></head><meta charset=\"utf-8\"><body><div align=right>"
    result += "<br>".join([" ".join(line).encode("utf8") for line in lines_list])
    result += "</div></body></html>"
    return result
    



def main(argv):
    print parse_text_xml(argv[1])
    


if __name__ == "__main__":
    main(sys.argv)