from rag_assisted_bot.rag_assisted_chatbot import GithubScrapper
from dotenv import load_dotenv
load_dotenv()

scrapper = GithubScrapper(
    username='vijaytakbhate2002', save_folder='./github_data/readme_files', metadata_save_folder='./github_data/metadata.json'
)
scrapper.scrap()
