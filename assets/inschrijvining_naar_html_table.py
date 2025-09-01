import pandas as pd
import pathlib
import sys

PATH = pathlib.Path(__file__).parent


def main():
    csv_file = pathlib.Path(
        PATH
        / "./Wolderwijdcup (Antwoorden) - Formulierreacties 1 2024-09-03.csv"
    )
    if len(sys.argv) == 1:
        print("Give input file")
        return None
    file = sys.argv[1]
    csv_file = pathlib.Path(PATH / file)
    if not csv_file.exists():
        print(f"{csv_file.resolve()} does not exist")
        return None
    df = pd.read_csv(csv_file)
    df.dropna(how="all", inplace=True)
    html_table = df[["Wedstrijdnummer", "Bootnaam", "Scheepstype"]]

    # Convert the DataFrame to HTML with the desired table structure
    html_table = html_table.to_html(
        classes="table table-hover", index=False, border=0
    )

    # Add custom classes to the table structure
    html_table = html_table.replace(
        "<thead>", '<thead class="table-secondary">'
    )

    # Wrap the table in a div with class "table-responsive"
    html_table = f'<div class="table-responsive">{html_table}</div>'
    html_table = html_table.replace("\n", "")

    # Print the HTML
    output_file = PATH / "../deelnemers_table.html"
    with open(output_file, "w") as f:
        f.writelines(html_table)
    print(f"New file written in: {output_file.resolve()}")


if __name__ == "__main__":
    main()
