#!/usr/bin/env python
import graphviz as gv
import json
import sys

class Block:

    def __init__(self, name):
        self.name = name
        self.routing_rules = None

def main(args):

    input_filename = args[1] if len(args) > 1 else 'data.json'
    output_filename = args[2] if len(args) > 2 else 'output'
    output_format = 'svg' # This might change later

    schema_json = None
    with open(file=input_filename, mode='r') as f:
        schema_json = json.load(f)
        f.close()

    if not schema_json:
        print('ERROR could not read file')

    blocks = []
    for group in schema_json['groups']:
        for block in group['blocks']:
            b = Block(block['id'])
            if 'routing_rules' in block:
                b.routing_rules = block['routing_rules']
            blocks.append(b)

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
                        label_parts.append(when['value'])
                    text = ' '.join(label_parts)
                    if len(text.strip()) > 0:
                        label = text

                graph.edge(block.name, routing_rule['goto']['id'], label=label)

        elif index < len(blocks) - 1:
            graph.edge(blocks[index].name, blocks[index+1].name, label='Implicit')

    filename = graph.render(filename=output_filename, cleanup=True)
    print('Generated file', filename)

if __name__ == '__main__':
    main(sys.argv)
