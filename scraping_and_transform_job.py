# %%
from transform.transform import main as transform_main
from scraping.scraping_BBC import main as scraping_main
from dotenv import load_dotenv


def main():
    load_dotenv()
    scraping_main()
    transform_main()
    return


if __name__ == "__main__":
    main()
# %%
