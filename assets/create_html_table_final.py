"""
Create HTML table from final subscriptions
"""

import pandas as pd
import pathlib


def to_html_table(df: pd.DataFrame):
    html_table = df.to_html(classes="table table-hover", index=False, border=0)

    # Add custom classes to the table structure
    html_table = html_table.replace(
        "<thead>", '<thead class="table-secondary">'
    )

    # Wrap the table in a div with class "table-responsive"
    html_table = f'<div class="table-responsive">{html_table}</div>'
    html_table = html_table.replace("\n", "")
    html_table = html_table.replace("right","center")
    return html_table


if __name__ == "__main__":
    file = "./startlijst_wolderwijdcup_2025.xlsx"
    df = pd.read_excel(file)
    df = df.drop("Unnamed: 7", axis=1)

    df = df.rename(
        {
            "sailno": "Zeilnummer",
            "boatname": "Bootnaam",
            "boattype": "Scheepstype",
            "name": "Schipper",
        },
        axis=1,
    )

    output_folder = pathlib.Path("./tables")
    output_folder.mkdir(exist_ok=True)
    # group by class:
    for key, group in df.groupby("class"):
        fname = output_folder / f"{key}_zaterdag.html"
        cols = ["Zeilnummer", "Bootnaam", "Schipper", "Scheepstype", "sw"]
        if key == "FF65":
            cols = cols[:-1]
            with open(fname, "w+") as f:
                f.writelines(to_html_table(group[cols]))
                continue
        with open(fname, "w+") as f:
            f.writelines(to_html_table(group[cols].sort_values("sw")))
        if key in ["SW-A", "SW-B"]:
            fname = output_folder / f"{key}_wwc.html"
            with open(fname, "w+") as f:
                f.writelines(
                    to_html_table(
                        group[group.info1.str.contains("zondag")][
                            cols
                        ].sort_values("sw")
                    )
                )
