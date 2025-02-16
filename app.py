from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interpret', methods=['POST'])
def interpret():
    file = request.files['file']
    content = file.read().decode('utf-8')
    interpreted_content = interpret_fidget_script(content)
    return interpreted_content

def interpret_fidget_script(script):
    lines = script.split('\n')
    output = []
    in_comment = False

    for line in lines:
        line = line.strip()

        # Handle comments
        if line.startswith('(') and line.endswith(')'):
            continue
        if line.startswith('('):
            in_comment = True
            continue
        if in_comment:
            if line.endswith(')'):
                in_comment = False
            continue

        # Handle DOCTYPE
        if line.startswith('<!DOCTYPE FIDGET>'):
            output.append('Fidget Script Detected')
            continue

        # Handle tags and attributes
        tag_match = re.match(r'<([a-z]+)([^>]*)>', line, re.IGNORECASE)
        if tag_match:
            tag = tag_match.group(1)
            attributes = parse_attributes(tag_match.group(2))

            if tag == 'display':
                output.append('Display Section:')
            elif tag == 'ren':
                output.append(f'Rendering Mode: {attributes.get("ren")}')
            elif tag == 'bg':
                output.append(f'Background: {attributes.get("colour")}')
            elif tag == 'console':
                output.append(f'Console Log: {attributes.get("log")}')
            elif tag == 'sprite':
                output.append(f'Sprite: {attributes}')
            elif tag == 'object':
                output.append(f'Object: {attributes}')
            elif tag == 'f':
                output.append(f'Function: {attributes}')
            elif tag == 'b':
                output.append(f'Button: {attributes}')
            elif tag == 'inter':
                output.append('Interaction Board:')
            elif tag == 'loop':
                output.append(f'Loop: {attributes}')
            elif tag == 'box':
                output.append(f'Box: {attributes.get("name")}')
            elif tag == 'exfile':
                output.append('External Files:')
            elif tag == 'link':
                output.append(f'Link: {attributes.get("name")} ({attributes.get("link")})')
            elif tag == 'walter':
                output.append('Walter Mode:')
            else:
                output.append(f'Unknown Tag: {tag}')
            continue

        # Handle plain text
        output.append(line)

    return '\n'.join(output)

def parse_attributes(attribute_string):
    attributes = {}
    attr_regex = re.compile(r'([a-z]+)=["\']?([^"\']+?)["\']?(?=\s|$)', re.IGNORECASE)
    matches = attr_regex.findall(attribute_string)
    for match in matches:
        attributes[match[0]] = match[1]
    return attributes

if __name__ == '__main__':
    app.run(debug=True)
