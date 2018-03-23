#!/usr/bin/env python
import graphviz as gv
import json
import sys

class Block:

    def __init__(self, name=''):
        self.name = name
        self.routing_rules = None

def read_json(filename=None):
    if not filename:
        raise NameError('JSON input file name not supplied.')

    json_content = None
    with open(file=filename, mode='r') as f:
        json_content = json.load(f)
        f.close()

    return json_content

def parse_schema_for_blocks(schema_json):
    blocks = []
    for section in schema_json['sections']:
        for group in section['groups']:
            for block in group['blocks']:
                b = Block()
                for question in block['questions']:
                    b.name = question['title']
                if 'routing_rules' in block:
                    b.routing_rules = block['routing_rules']
                blocks.append(b)
    return blocks

def construct_graph(output_format, blocks):
    graph = gv.Digraph(format=output_format)
    for index, block in enumerate(blocks):
        graph.node(block.name)
        if block.routing_rules:
            for routing_rule in block.routing_rules:
                label = None
                if 'when' in routing_rule['goto']:
                    when = routing_rule['goto']['when'][0]
                    label_parts = []
                    if 'id' in when:
                        label_parts.append(when['id'])
                    if 'meta' in when:
                        label_parts.append(when['meta'])
                    if 'condition' in when:
                        label_parts.append(when['condition'])
                    if 'value' in when:
                        label_parts.append('&quot;' + when['value'] + '&quot;')
                    text = ' '.join(label_parts)
                    if len(text.strip()) > 0:
                        label = text
                graph.edge(block.name, routing_rule['goto']['id'], label=label)
        elif index < len(blocks) - 1:
            graph.edge(blocks[index].name, blocks[index+1].name, label='Implicit')

    return graph

def main(args):
    input_filename = args[1] if len(args) > 1 else 'data.json'
    output_filename = args[2] if len(args) > 2 else 'output'
    output_format = 'svg'

    schema_json = read_json(input_filename)
    if not schema_json:
        print('Could not read JSON from', input_filename)
        sys.exit(1)

    blocks = parse_schema_for_blocks(schema_json)
    graph = construct_graph(output_format, blocks)
    filename = graph.render(filename=output_filename, cleanup=True)
    print('Generated file', filename)

if __name__ == '__main__':
    main(sys.argv)
