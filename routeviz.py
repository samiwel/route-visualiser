import tkinter as tk
import graphviz as gv
from PIL import Image, ImageTk
import json

class Block:

    def __init__(self, name):
        self.name = name
        self.routing_rules = None

def main():

    schema_json = None
    with open(file='data.json', mode='r') as f:
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

    graph = gv.Graph(format='png')
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

    filename = graph.render(cleanup=True)
    print('Generated file', filename)
    root = tk.Tk()
    root.wm_title = filename
    img = ImageTk.PhotoImage(Image.open(filename))
    panel = tk.Label(root, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    root.mainloop()

if __name__ == '__main__':
    main()
