# AI Demo

## Project List

### Bert

- Description: This repository contains a demo for fining tune BERT model, a popular transformer-based model proposed in 2018.
- Target: Fine-tuning using BERT allows the model to learn Eason's linguistic style and expression habits. When tested, the model generates a continuation of Eason's style based on input prompts.
- Steps to run:
  1. Clone the repository and go to `Bert` folder.
  2. Install the required dependencies using `pip install -r requirements.txt`.
  3. Install `torch` version based on your environment, you can find the command [here](https://pytorch.org/get-started/locally/).
     1. You can use the `demo.py` to check if the torch is installed correctly. If it print `cuda` it means the torch is installed with GPU support, otherwise it is installed with CPU support.
  4. Prepare the dataset for fine-tuning in `eason_comments.txt`.
  5. Run the fine-tuning script using `python train_eason_bert.py`. It will fine-tune the BERT model on the provided dataset and test it.
     1. Ground Truth: `Looks like playing football, if you can't shoot, pass it to your teammates.`
     2. Before train: `Looks like playing football, if you can't shoot, pass it to your friends.`
     3. After train: `Looks like playing football, if you can't shoot, pass it to your opponent.`
- Hint:
  - If you network cannot download the pretrained model from huggingface, try this [method](https://blog.csdn.net/qq_60074111/article/details/138977479)
    1. Config in powershell `$env:HF_ENDPOINT = "https://hf-mirror.com"`.
    2. Install two pakages using `pip install -U huggingface_hub hf_transfer`.
  - If your pip install is slow, using `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` to speed up the download process.  

### WIReview
- Description: This repository contains a demo of CW work item details page using AI to collect information and generate a summary review report. Most code is written by DeepSeek (backend) and v0 (frontend).
 
https://github.com/user-attachments/assets/e6d8ccb1-6db1-49c3-b586-8b0368402095

- Technical Details:
  - Python flask for web server and pyodbc for database connection & query.
  - FastMCP and DeepSeek for AI MCP integration.
  - (BTW) The code sucks, using direct sql query, self defined database and ugly code. So it is a demo, not a production code.
- Steps to run:
  1. Clone the repository and go to `WIReview` folder.
  2. Install the required dependencies using `pip install -r requirements.txt`.
  3. Prepare a database named `OdysseyWIReview` and create a user in SSMS to access it.
  4. Run the `create_tables.sql` and `seed_data.sql` scripts in the database to create the required tables and seed the data.
  5. Apply a DeepSeek developer key [here](https://platform.deepseek.com) and create a API key.
  6. Change the setting in config.py based on your environment.
    - `DB_SERVER`: Your database server name.
    - `DB_NAME`: Your database name, default is `OdysseyWIReview`.
    - `DB_USER`: Your database user name.
    - `DB_PASSWORD`: Your database user password.
    - `DEEPSEEK_API_KEY`: Your DeepSeek API key.
  7. Run the web server using `python app.py`.
  8. Open your browser and go to `http://localhost:5000` to access the web application.

## Link

- [Prompt](https://github.com/WiseTechGlobal/WTG.AI.Prompts)
- [MCP For EdiProd](https://github.com/WiseTechGlobal/Rating.Tools.EdiProd)
- [DeepSeek and MCP Demo project](https://github.com/wink-wink-wink555/ai-github-assistant)
