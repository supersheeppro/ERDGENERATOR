import json
import math
import xml.sax.saxutils as saxutils
from typing import List, Dict, Any, Tuple


class DrawioClassDiagramGenerator:
    """
    Genereert een Draw.io XML-bestand voor een klassendiagram vanuit een JSON-input.
    Deze versie is gecorrigeerd voor de TypeError en gebruikt een robuustere methode
    voor het doortellen van cell IDs.
    """

    def __init__(self, padding: int = 150, class_width: int = 240):
        self.padding = padding
        self.class_width = class_width
        self.classes_input: List[Dict[str, Any]] = []
        self.colors = ["#FF0000", "#00AA00", "#0000FF", "#FFAA00", "#00AAAA", "#AA00AA", "#000000"]
        self.container_style = "swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentCheck=0;collapsible=0;marginBottom=0;html=1;"
        self.title_style = "text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontStyle=1"
        self.member_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;"
        self.relationship_styles = {
            "inheritance": {"startArrow": "none", "startFill": "0", "endArrow": "block", "endFill": "0"},
            "composition": {"startArrow": "diamond", "startFill": "1", "endArrow": "none", "endFill": "0"},
            "aggregation": {"startArrow": "diamond", "startFill": "0", "endArrow": "none", "endFill": "0"},
            "association": {"startArrow": "none", "startFill": "0", "endArrow": "open", "endFill": "0"},
            "default": {"startArrow": "none", "startFill": "0", "endArrow": "none", "endFill": "0"},
        }

    def _escape(self, text: str) -> str:
        return saxutils.escape(text, {"\"": "&quot;", "'": "&apos;"})

    def _create_cell(self, id_: int, x: int, y: int, w: int, h: int, text: str, style: str) -> str:
        return f'\n    <mxCell id="{id_}" value="{self._escape(text)}" style="{style}" vertex="1" parent="1">\n      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n    </mxCell>'

    def _make_class_cell(self, json_data: Dict[str, Any], x: int, y: int, start_id: int) -> Tuple[
        str, int, int, int, Dict]:
        def format_members(members: List[Dict], is_method: bool = False) -> str:
            lines = []
            for member in members:
                access_map = {"public": "+", "private": "-", "protected": "#"}
                access = access_map.get(member.get("access", "private"), "-")
                if is_method:
                    params = ", ".join(member.get("parameters", []))
                    ret_type = member.get("return_type", "void")
                    line = f'{access} {member["name"]}({params}): {ret_type}'
                else:
                    line = f'{access} {member["name"]}: {member["type"]}'
                lines.append(self._escape(line))
            return "<br>".join(lines)

        attributes_str = format_members(json_data.get("attributes", []))
        methods_str = format_members(json_data.get("methods", []), is_method=True)
        line_h, min_comp_h, title_h, line_separator_h = 20, 25, 30, 1

        # Voeg een extra hoogte toe voor de scheidingslijn
        attr_h = max(min_comp_h, len(json_data.get("attributes", [])) * line_h)
        meth_h = max(min_comp_h, len(json_data.get("methods", [])) * line_h)
        total_h = title_h + attr_h + line_separator_h + meth_h

        cells, cell_id = [], start_id
        cells.append(self._create_cell(cell_id, x, y, self.class_width, total_h, "", self.container_style))
        cell_id += 1
        cells.append(self._create_cell(cell_id, x, y, self.class_width, title_h, json_data['name'], self.title_style))
        cell_id += 1
        cells.append(
            self._create_cell(cell_id, x, y + title_h, self.class_width, attr_h, attributes_str, self.member_style))
        cell_id += 1

        # Nieuwe cel voor de horizontale lijn
        separator_style = "line;strokeWidth=1;html=1;fontStyle=1;align=center;verticalAlign=middle;"
        cells.append(self._create_cell(cell_id, x, y + title_h + attr_h, self.class_width, line_separator_h, "",
                                       separator_style))
        cell_id += 1

        cells.append(self._create_cell(cell_id, x, y + title_h + attr_h + line_separator_h, self.class_width, meth_h,
                                       methods_str,
                                       self.member_style))
        cell_id += 1

        class_data = {"name": json_data['name'], "pos": (x, y), "width": self.class_width, "height": total_h,
                      "json": json_data}
        return "\n".join(cells), cell_id, self.class_width, total_h, class_data

    def _generate_diagram_layout(self) -> Tuple[List[Dict[str, Any]], int]:  # GEWIJZIGD
        """Berekent de layout en genereert de cellen voor alle klassen."""
        if not self.classes_input: return [], 2

        total_classes = len(self.classes_input)
        columns = math.ceil(math.sqrt(total_classes))

        temp_heights = [max(25, len(c.get("attributes", [])) * 20) + max(25, len(c.get("methods", [])) * 20) + 30 for c
                        in self.classes_input]

        y_positions, current_y = [], 0
        for row in range(math.ceil(total_classes / columns)):
            row_indices = range(row * columns, min((row + 1) * columns, total_classes))
            if not row_indices: continue
            max_h = max(temp_heights[i] for i in row_indices)
            y_positions.append(current_y)
            current_y += max_h + self.padding

        cell_id, classes_info = 2, []
        for i, class_json in enumerate(self.classes_input):
            col, row = i % columns, i // columns
            x = col * (self.class_width + self.padding)
            y = y_positions[row]

            xml, next_id, w, h, data = self._make_class_cell(class_json, x, y, cell_id)
            data['xml'] = xml
            classes_info.append(data)
            cell_id = next_id

        return classes_info, cell_id  # GEWIJZIGD: geef de laatst gebruikte cell_id terug

    def _generate_relationship_cells(self, classes_info: List[Dict[str, Any]], start_cell_id: int) -> str:  # GEWIJZIGD
        """Genereert de XML voor alle relatielijnen tussen de klassen."""
        class_map = {c["name"]: c for c in classes_info}

        # GEWIJZIGD: Verwijder de foute berekening en gebruik de doorgegeven startwaarde
        cell_id = start_cell_id

        relation_cells, rel_idx, used_waypoints = [], 0, set()

        def get_unique_waypoint_x(x: float) -> Tuple[float, float]:
            offset, original_x = 0, x
            while x in used_waypoints:
                offset += 10
                x = original_x - offset
            used_waypoints.add(x)
            return x, offset

        for source_info in classes_info:
            for rel in source_info["json"].get("relationships", []):
                target_name = rel.get("target")
                if not target_name or target_name not in class_map: continue

                target_info = class_map[target_name]
                style_props = self.relationship_styles.get(rel.get("type"), self.relationship_styles["default"])

                source_x_edge, source_y_mid = source_info["pos"][0] + source_info["width"], source_info["pos"][1] + \
                                              source_info["height"] / 2
                target_x_edge, target_y_mid = target_info["pos"][0], target_info["pos"][1] + target_info["height"] / 2

                half_pad = self.padding / 2
                wp1_x, _ = get_unique_waypoint_x(source_x_edge + half_pad)
                wp4_x, _ = get_unique_waypoint_x(target_x_edge - half_pad)

                points_arr = []
                if source_info["pos"][0] != target_info["pos"][0]:
                    shared_y = min(source_info["pos"][1], target_info["pos"][1]) - half_pad
                    points_arr.extend(
                        [f'<mxPoint x="{wp1_x}" y="{source_y_mid}" />', f'<mxPoint x="{wp1_x}" y="{shared_y}" />',
                         f'<mxPoint x="{wp4_x}" y="{shared_y}" />', f'<mxPoint x="{wp4_x}" y="{target_y_mid}" />'])
                else:
                    points_arr.extend(
                        [f'<mxPoint x="{wp1_x}" y="{source_y_mid}" />', f'<mxPoint x="{wp4_x}" y="{target_y_mid}" />'])

                points = f'\n<Array as="points">\n{"".join(p for p in points_arr)}\n</Array>'

                color = self.colors[rel_idx % len(self.colors)]
                line_style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={color};strokeWidth=2;" + "".join(
                    f"{k}={v};" for k, v in
                    style_props.items()) + f"sourceLabel={self._escape(rel.get('source_multiplicity', ''))};targetLabel={self._escape(rel.get('target_multiplicity', ''))};"

                relation_cells.append(f'''
                <mxCell id="{cell_id}" style="{line_style}" edge="1" parent="1">
                  <mxGeometry relative="1" as="geometry">
                    <mxPoint x="{source_x_edge}" y="{source_y_mid}" as="sourcePoint" />
                    <mxPoint x="{target_x_edge}" y="{target_y_mid}" as="targetPoint" />{points}
                  </mxGeometry>
                </mxCell>''')
                cell_id += 1
                rel_idx += 1

        return "\n".join(relation_cells)

    def run(self, json_data: List[Dict[str, Any]]) -> str:
        """Hoofdfunctie om de volledige Draw.io XML te genereren."""
        self.classes_input = json_data

        # GEWIJZIGD: Vang de laatst gebruikte cell_id op
        layout_info, last_class_cell_id = self._generate_diagram_layout()
        class_cells_xml = "\n".join(c['xml'] for c in layout_info)

        # GEWIJZIGD: Geef de cell_id door aan de volgende functie
        relationship_cells_xml = self._generate_relationship_cells(layout_info, last_class_cell_id)

        header = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="python-script-v3" version="24.0.0" type="device">
<diagram name="Class Diagram" id="diagram1">
<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#FFFFFF" math="0" shadow="0">
<root><mxCell id="0"/><mxCell id="1" parent="0"/>'''
        footer = '''</root></mxGraphModel></diagram></mxfile>'''
        return header + class_cells_xml + "\n" + relationship_cells_xml + footer


if __name__ == "__main__":
    json_string = """
    [
      { "name": "Person", "attributes": [{"name": "name", "type": "String", "access": "protected"}]},
      { "name": "Customer", "attributes": [{"name": "customerId", "type": "int", "access": "private"}], "methods": [{"name": "placeOrder", "return_type": "Order", "access": "public"}], "relationships": [{"type": "inheritance", "target": "Person"}]},
      { "name": "Order", "attributes": [{"name": "orderId", "type": "int", "access": "private"}], "relationships": [{"type": "association", "target": "Customer", "source_multiplicity": "*", "target_multiplicity": "1"}, {"type": "composition", "target": "OrderLine", "source_multiplicity": "1", "target_multiplicity": "1..*"}]},
      { "name": "OrderLine", "attributes": [{"name": "quantity", "type": "int", "access": "private"}], "relationships": [{"type": "aggregation", "target": "Product", "source_multiplicity": "*", "target_multiplicity": "1"}]},
      { "name": "Product", "attributes": [{"name": "productId", "type": "int", "access": "private"}]}
    ]
    """
    class_diagram_json = json.loads(json_string)

    generator = DrawioClassDiagramGenerator()
    drawio_xml = generator.run(class_diagram_json)

    output_filename = "class_diagram_v3_fixed.drawio"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(drawio_xml)
        print(f"✅ Succesvol '{output_filename}' gegenereerd.")
    except IOError as e:
        print(f"❌ Fout bij het schrijven naar het bestand: {e}")