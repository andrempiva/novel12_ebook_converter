
# novel12_ebook_converter
This Python script will download a novel availaible on [Novel12](https://novel12.com/) and save it into the .epub format.
Based on [wuxiaworld_export_ebook](https://github.com/LordKBX/wuxiaworld_export_ebook), a Fork of [Wuxiaworld-2-eBook](https://github.com/MakeYourLifeEasier/Wuxiaworld-2-eBook).

## Getting Started

To run this script you'll need to have Python >=3.4.x installed which you can find [here](https://www.python.org/downloads/ "Python Download Link").

### Features

- Download and save you favorite Novels from novel12.com into a .epub file

### Installation

As mentioned before this script was written for Python >=3.4.x.

Additionally the packages lxml and Beautifulsoup4 are required.

To install all dependencies just use the console to navigate into the project folder and write

```
pip install -r requirements.txt
```

### Usage

Edit the my_novel variable in main.py file with the parameters you want, found on the page of the novel in the novel12 website.

Run the script using
```
python main.py
```
Keep in mind that it will take some time for the script to finish, so don't close the window or the console if the program doesn't respond.

When done, your ebook will be in the export folder.

## Keep in mind!

If you come across bug's or suggestion's for future updates don't hesitate to open up a "new Issue" in the issue tab

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
