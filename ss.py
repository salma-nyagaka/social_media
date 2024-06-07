

import re

def extract_table_creation_statements(sql_content):
    statements = []
    in_statement = False
    current_statement = []

    for line in sql_content.splitlines():
        if line.strip().startswith("CREATE TABLE"):
            in_statement = True

        if in_statement:
            current_statement.append(line)

        if in_statement and line.strip().endswith(";"):
            statements.append("\n".join(current_statement))
            current_statement = []
            in_statement = False

    return statements

def parse_table_creation_statement(statement):
    table_name_match = re.search(r'CREATE TABLE [\w.]+\.([\w_]+) \(', statement)
    if not table_name_match:
        return None, []

    table_name = table_name_match.group(1)
    columns = re.findall(r'(\w+)\s+(\w+.*?)(?:,|\))', statement)
    return table_name, columns

def extract_foreign_keys(sql_content):
    fk_statements = re.findall(r'ALTER TABLE ONLY ([\w.]+)\n\s+ADD CONSTRAINT (\w+) FOREIGN KEY \((\w+)\) REFERENCES ([\w.]+)\((\w+)\)', sql_content)
    foreign_keys = []
    for fk in fk_statements:
        source_table = fk[0].split('.')[-1]
        target_table = fk[3].split('.')[-1]
        foreign_keys.append((source_table, target_table, fk[2], fk[4]))
    return foreign_keys

def generate_drawio_xml(tables, foreign_keys):
    xml_content = [
        '<mxfile host="app.diagrams.net">',
        '  <diagram name="ERD" id="some-id">',
        '    <mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]

    cell_id = 2
    table_cells = {}

    for table_name, columns in tables.items():
        xml_content.append(f'        <mxCell id="{cell_id}" value="{table_name}" style="shape=table;startSize=30;" vertex="1" parent="1">')
        xml_content.append(f'          <mxGeometry x="20" y="{20 + 100 * (cell_id - 2)}" width="160" height="{30 + 30 * len(columns)}" as="geometry" />')
        xml_content.append(f'        </mxCell>')
        table_cells[table_name] = cell_id
        parent_cell_id = cell_id
        cell_id += 1
        for column_name, column_type in columns:
            xml_content.append(f'        <mxCell id="{cell_id}" value="{column_name}: {column_type}" style="text;html=1;" vertex="1" parent="{parent_cell_id}">')
            xml_content.append(f'          <mxGeometry x="0" y="{30 * (cell_id - parent_cell_id)}" width="160" height="30" as="geometry" />')
            xml_content.append(f'        </mxCell>')
            cell_id += 1

    for fk in foreign_keys:
        source_table_id = table_cells[fk[0]]
        target_table_id = table_cells[fk[1]]
        xml_content.append(f'        <mxCell id="{cell_id}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;" edge="1" parent="1" source="{source_table_id}" target="{target_table_id}">')
        xml_content.append(f'          <mxGeometry relative="1" as="geometry" />')
        xml_content.append(f'        </mxCell>')
        cell_id += 1

    xml_content.append('      </root>')
    xml_content.append('    </mxGraphModel>')
    xml_content.append('  </diagram>')
    xml_content.append('</mxfile>')

    return "\n".join(xml_content)

# Read the SQL dump file
sql_dump_path = '/Users/salmanyagaka/Documents/social_media_project.sql'
with open(sql_dump_path, 'r') as file:
    sql_dump_content = file.read()

# Extract and parse table creation statements
table_creation_statements = extract_table_creation_statements(sql_dump_content)
tables = {}
for statement in table_creation_statements:
    table_name, columns = parse_table_creation_statement(statement)
    if table_name:
        tables[table_name] = columns

# Extract foreign key constraints
foreign_keys = extract_foreign_keys(sql_dump_content)

# Generate draw.io XML
drawio_xml = generate_drawio_xml(tables, foreign_keys)

# Save the XML to a file
xml_output_path = '/Users/salmanyagaka/Documents/social_media_project.xml'
with open(xml_output_path, 'w') as file:
    file.write(drawio_xml)

print(f"XML output saved to {xml_output_path}")
