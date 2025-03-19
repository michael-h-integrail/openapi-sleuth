#!/usr/bin/env python3
import argparse
import os
import re
import requests

def sanitize_filename(name):
    """
    Sanitize the API name so it can be used as part of a filename.
    Lowercases the name and replaces non-alphanumeric characters with hyphens.
    """
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def get_latest_version(versions):
    """
    Select the version with stage 'LATEST' if available,
    otherwise return the first available version.
    """
    latest = [v for v in versions if v.get("stage") == "LATEST"]
    if latest:
        # If more than one, choose the one with the highest version number
        latest.sort(key=lambda x: x.get("version", 0), reverse=True)
        return latest[0]
    elif versions:
        return versions[0]
    return None

def download_openapi_files(base_url, prefix):
    """
    Fetches the enumeration endpoint, iterates over each API definition,
    downloads the OpenAPI spec from the provided URL,
    and saves it in the base folder with filenames using the format:
    basename-apiname.json.
    """
    try:
        resp = requests.get(base_url)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching enumeration endpoint: {e}")
        return

    data = resp.json()
    results = data.get("results", [])
    if not results:
        print("No API definitions found at the enumeration endpoint.")
        return

    print(f"Found {len(results)} API definitions.")

    # Create base folder using the prefix
    base_folder = prefix
    os.makedirs(base_folder, exist_ok=True)
    total_files = 0

    for api_def in results:
        api_name = api_def.get("name")
        versions = api_def.get("versions", [])
        if not versions:
            print(f"No versions for API '{api_name}', skipping.")
            continue

        version_info = get_latest_version(versions)
        if not version_info:
            print(f"No valid version info for API '{api_name}', skipping.")
            continue

        openapi_url = version_info.get("openApi")
        if not openapi_url:
            print(f"No openApi URL for API '{api_name}', skipping.")
            continue

        print(f"Downloading OpenAPI for '{api_name}' from {openapi_url}...")
        try:
            openapi_resp = requests.get(openapi_url)
            openapi_resp.raise_for_status()
        except Exception as e:
            print(f"Error fetching OpenAPI spec for '{api_name}': {e}")
            continue

        sanitized_name = sanitize_filename(api_name)
        filename = os.path.join(base_folder, f"{prefix}-{sanitized_name}.json")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(openapi_resp.text)
            print(f"Saved OpenAPI spec for '{api_name}' to {filename}")
            total_files += 1
        except Exception as e:
            print(f"Error saving file for '{api_name}': {e}")

    print(f"\nTotal {total_files} OpenAPI file(s) created in '{base_folder}' folder.")

def main():
    parser = argparse.ArgumentParser(
        description="Enumerate and download OpenAPI specs from a vendor's enumeration endpoint, storing them in a base folder.",
        epilog="Example usage:\n  python openapi-sleuth.py --base-url https://api.hubspot.com/public/api/spec/v1/specs --prefix hubspot"
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://api.hubspot.com/public/api/spec/v1/specs",
        help="Base URL for the vendor's API enumeration endpoint (default: HubSpot specs endpoint)"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="hubspot",
        help="Prefix for the output file names; a base folder will be created with this name (default: hubspot)"
    )
    args = parser.parse_args()
    download_openapi_files(args.base_url, args.prefix)

if __name__ == "__main__":
    main()
