import argparse
import nbformat
import os

def add_state_to_widgets(nb):
    # Process widget metadata in notebook metadata if present
    widgets = nb.get('metadata', {}).get('widgets', {})
    if isinstance(widgets, dict):
        for widget_id, widget_data in widgets.items():
            if 'state' not in widget_data:
                widget_data['state'] = {}
        nb['metadata']['widgets'] = widgets

    # Process widget metadata in each cell, if present
    for cell in nb.get('cells', []):
        if 'metadata' in cell and isinstance(cell['metadata'], dict):
            cell_widgets = cell['metadata'].get('widgets', {})
            if isinstance(cell_widgets, dict):
                for widget_id, widget_data in cell_widgets.items():
                    if 'state' not in widget_data:
                        widget_data['state'] = {}
                cell['metadata']['widgets'] = cell_widgets
    return nb

def main():
    parser = argparse.ArgumentParser(
        description="Fix widget metadata in a Jupyter Notebook by adding a dummy 'state' key where missing."
    )
    parser.add_argument("notebook_path", help="Path to the Jupyter Notebook file (ipynb)")

    args = parser.parse_args()
    notebook_path = args.notebook_path

    # Construct output path: original name with _clean appended before file extension
    base, ext = os.path.splitext(notebook_path)
    output_path = f"{base}_clean{ext if ext else '.ipynb'}"

    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    except Exception as e:
        print(f"Error reading notebook {notebook_path}: {e}")
        return

    nb = add_state_to_widgets(nb)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Fixed notebook saved as {output_path}")
    except Exception as e:
        print(f"Error writing fixed notebook to {output_path}: {e}")

if __name__ == "__main__":
    main()
