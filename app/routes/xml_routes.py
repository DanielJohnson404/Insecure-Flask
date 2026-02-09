from flask import Blueprint, request
import xml.etree.ElementTree as ET
import lxml.etree

xml_bp = Blueprint('xml_bp', __name__)

@xml_bp.route('/process_xml_unsafe', methods=['POST'])
def process_xml_unsafe():
    try:
        xml_data = request.data
        parser = lxml.etree.XMLParser(resolve_entities=True) 
        root = lxml.etree.fromstring(xml_data, parser=parser)
        username = root.findtext('username')
        return f"Processed user: {username}"
    except Exception as e:
        return str(e)

@xml_bp.route('/process_xml_safe', methods=['POST'])
def process_xml_safe():
    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)
        username = root.find('username').text
        return f"Processed user safely: {username}"
    except Exception as e:
        return str(e)
