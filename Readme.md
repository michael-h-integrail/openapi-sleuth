# OpenAPI Sleuth

This project contains a Python script named `openapi-sleuth.py` that generates OpenAPI files for a given 'reflective' openapi API. Hubspot provides such a reflective API [here](https://api.hubspot.com/public/api/spec/v1/specs).  This type of API endpoint returns a list of other endpoints that provide openapi json content.  It's useful for discovering the available APIs (and their openapi descriptions) in an automated way, which is what this script does.

This script creates a folder for the base API name provided (default: "hubspot") and generates multiple OpenAPI files within that folder named 'BaseAPIname-endpointname.json' (for example, 'hubspot-tasks.json' for the tasks endpoint). 

When the script finishes, it prints out how many OpenAPI files it created in the subfolder.

## Prerequisites

- **Python 3.8+**
- **Conda** (or Miniconda/Anaconda)

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/michael-h-integrail/openapi-sleuth.git
cd openapi-sleuth
```

### 2. Create and Activate a Conda Environment

Create a new Conda environment named openapi-sleuth and activate it:

```bash
conda create -n openapi-sleuth python=3.8 -y
conda activate openapi-sleuth
```
### 3. Install Dependencies
Install the required dependencies using pip with the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

## Running the Script
Once the environment is set up and dependencies are installed, run the script with:

```bash
python openapi-sleuth.py
```

## Optional Arguments
- **--base-url**: Specify the base URL for the reflective API that can be used to find openapi endpoints and their openapi json descriptions (Default is 'https://api.hubspot.com/public/api/spec/v1/specs')
- **--prefix**: Specify a prefix for the openapifiles. The script will also create all your prefix-endpointname.json files in folder with the prefix name. (Default is 'hubspot')


For example, if you wanted to generate the hubspot openapi files use:

```bash
python openapi-sleuth.py --base-url https://api.hubspot.com/public/api/spec/v1/specs --api-name hubspot
```
After running, the script will output the number of OpenAPI files created in the specified prefix folder.