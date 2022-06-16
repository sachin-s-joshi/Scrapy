# Scrapy
Scrapy to scrape/crawl website and get data to store and analyze

# Command for run
    Setup virtual environment with – pyhton3 -e venv nameofenv , a folder is created with name in root directory example (bot)

    Activate virtual environment with – source /virtual_environment_folder/bin/activate

    After activation, install all required packages using python install -r requirements.txt

    And , now under subdirectory demo, run – scrapy crawl me
### Running with Custom URLs:

After the project is set setup create .env file at root level.

Following variable are set now:
- site - for website url

This .env file is served as environment variable to specify urls you want to crawl 

### Command to run:

- Setup virtual environment with – pyhton3 -e venv nameofenv , a folder is created with name in root directory example (bot)
- Activate virtual environment with – source /virtual_environment_folder/bin/activate
- After activation, install all required packages using python install -r requirements.txt
- And , now under subdirectory demo, run – scrapy crawl me

### Running with Docker images:

* Run docker build -t <image_name> .
* docker run crawler:custom crawl me
