import os
import json
import platform
import pandas as pd


def get_extensions_dir():
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home, ".vscode", "extensions")
    else:
        # Works for both macOS and Linux
        return os.path.join(home, ".vscode", "extensions")


def main():
    pd.set_option("display.width", 100)  # Set pandas print width to 100 characters

    extensions_dir = get_extensions_dir()
    if not os.path.isdir(extensions_dir):
        print("VS Code extensions directory not found.")
        return

    extensions_data = []  # List to store extracted data

    for ext_folder in os.listdir(extensions_dir):
        ext_path = os.path.join(extensions_dir, ext_folder)
        package_json = os.path.join(ext_path, "package.json")
        if os.path.isfile(package_json):
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    name = data.get("name", "Unknown")
                    version = data.get("version", "Unknown")
                    display_name = data.get("displayName", "Unknown")
                    publisher = data.get("publisher", "Unknown")
                    author = data.get("author", "Unknown")
                    author = (
                        author
                        if isinstance(author, str)
                        else author.get("name", "Unknown")
                    )
                    extensions_data.append(
                        {
                            "Display Name": display_name,
                            "Author": author,
                            "Publisher": publisher,
                            "Version": version,
                            "Name": name,
                        }
                    )
            except Exception as e:
                print(f"Failed to read {package_json}: {e}")

    # Create a pandas DataFrame from the extracted data
    if extensions_data:
        df = pd.DataFrame(extensions_data)
        df = df.sort_values(by=["Publisher", "Display Name"])

        # dedup the DataFrame
        df = df.drop_duplicates(subset=["Display Name", "Publisher"])
        df = df.reset_index(drop=True)

        print("\nExtensions DataFrame:")
        print(df)

        # Save the DataFrame to a CSV file
        df.to_csv("vsc_extensions.csv", index=False)
    else:
        print("No extensions data found.")


if __name__ == "__main__":
    main()
