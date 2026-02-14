import pandas as pd
import pathlib


def to_html_table(df: pd.DataFrame):
    html_table = df.to_html(classes="table table-hover", index=False, border=0)

    # Add custom classes to the table structure
    html_table = html_table.replace("<thead>", '<thead class="table-secondary">')

    # Wrap the table in a div with class "table-responsive"
    html_table = f'<div class="table-responsive">{html_table}</div>'
    html_table = html_table.replace("\n", "")
    html_table = html_table.replace("right", "left")
    return html_table


if __name__ == "__main__":
    # go over each html file: 
    DIR = pathlib.Path(__file__).parent
    html_files = list(DIR.glob('*.html'))
    print(*html_files, sep='\n')

    output_file = DIR / "uitslag.html"

    with open(output_file, mode='w+') as f:
        for file in html_files:
            if 'uitslag' in file.name:
                continue
            f.writelines(f"<h4>{file.stem}</h4>\n")
            df = pd.read_html(file)
            assert len(df) == 1
            df = df[0]
            

            df = df.rename({"No": "Nr", "Saino":"Zeilnr", "Boatname": "Bootnaam", "Points": "Punten"}, axis=1)
            df.Punten /= 10
            df = df.drop("Name", axis=1)
            # df = df.set_index("Nr")

            f.writelines(to_html_table(df))
            f.writelines("\n")



