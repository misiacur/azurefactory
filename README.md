# Azure Roadies Backstage support repo
This is set of scripts that should help with Azure Factory to backstage migration 

## Folders structurue
- **catalog-templates**
Contains templates used by Python script to generate `catalog-info.yml` files that will have to be register by Backstage 
  - `azurefactory-domain.yml` (has to be modified manualy) defines Azure Factory **project** as Domain 
  - `azurefactory-groups.yml` (has to be modified manualy) defines **groups** responsible for specific colections
  - `azurefactory-users.yml` (has to be modified manualy) defines list of **users** assigned to the groups
  - `role-catalog.j2` (template) defines catalog-info file for **roles**
  - `system-catalog.j2` (template) defines catalog-info file for **collections**
- **test** 
Test folder mimiking Azure Factory repository structure, used to test script `catalog-creator.py`
- **`catalog-creator.py`** main script responsible to generate catalog-info files that will be register in Backstage

## How script works?
Script `catalog-creator.py` uses (defined in the script) list of COLLECTIONS to loop over. And generates all files under `/target` folder. Script also use (by default) `/test` folder to recognize roles and generate for each role `catalog-info.yml` file definig this role.

When running script make sure you have python install and jinja2 lib 
```shell
python3.10 -m pip install --upgrade pip   
pip3 install Jinja2
```

To run script just execute:
```shell
python3 catalog-creator.py   
```

## TODO
- roles currently have fixed dependency 
- groups have to be setup manually
- users have to be setup manually 