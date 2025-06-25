from icrawler.builtin import GoogleImageCrawler
import os

def download_images(keyword, folder, max_num=50):
    save_dir = os.path.join("dataset", folder)
    os.makedirs(save_dir, exist_ok=True)

    crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    crawler.crawl(keyword=keyword, max_num=max_num)
    print(f"✅ Скачано {max_num} фото в папку {save_dir}")

if __name__ == "__main__":
    categories = {
        "fixie": "fixed gear bike",
        "mtb": "mountain bike",
        "bmx": "bmx bicycle",
        "road": "road bike",
        "keirin": "keirin bike"
    }

    for name, query in categories.items():
        download_images(query, name, max_num=50)
