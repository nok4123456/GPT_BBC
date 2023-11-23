# %%
from transform import main as transform_main
from scraping_BBC import main as scraping_main


def scraping_and_transform():
    scraping_main()
    transform_main()
    return


scraping_and_transform()

# %%
