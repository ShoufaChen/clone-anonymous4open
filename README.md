# Clone codes from anonymous.4open.science 

**Can NOT work now** :pensive:


Only supports Python3.

## Prerequisites
```
pip install beautifulsoup4
pip install lxml
```


## Quick Start
```
git clone https://github.com/ShoufaChen/clone-anonymous4open
cd clone-anonymous4open
python clone.py --clone-dir /path/to/save  --target anonymous-url
```
Example:
```
python clone.py --clone-dir ../examples --target https://anonymous.4open.science/r/840c8c57-3c32-451e-bf12-0e20be300389/
```


## TODO
- [ ] support files that do not have `<code>` element.
- [ ] support *.md files

## Acknowledgement

Thanks to excellent [Luyuan](https://github.com/BeBeBerr) for helpful instructions. :poultry_leg::poultry_leg::poultry_leg:
