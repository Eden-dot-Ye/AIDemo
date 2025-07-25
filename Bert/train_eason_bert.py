import torch
from transformers import BertTokenizer, BertForMaskedLM
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        self.tokenizer = tokenizer
        self.max_length = max_length
        with open(file_path, 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f if line.strip()]

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        line = self.lines[idx]
        encoding = self.tokenizer(
            line,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': encoding['input_ids'].flatten()
        }

def train(epoch):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    model.to(device)

    dataset = TextDataset('eason_comments.txt', tokenizer)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(epoch):
        total_loss = 0
        progress_bar = tqdm(dataloader, desc=f'Epoch {epoch + 1}')
        for batch in progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
            total_loss += loss.item()

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            progress_bar.set_postfix({'loss': loss.item()})

        avg_loss = total_loss / len(dataloader)
        print(f'Epoch {epoch + 1}, Average Loss: {avg_loss}')

    model.save_pretrained('eason_bert')
    tokenizer.save_pretrained('eason_bert')

def generate_text(prompt, model_path='eason_bert', num_samples=1):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForMaskedLM.from_pretrained(model_path)
    model.to(device)
    model.eval()

    for _ in range(num_samples):
        input_text = prompt + " [MASK]" * 10
        inputs = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        predicted_token_ids = torch.argmax(outputs.logits, dim=-1)
        generated = tokenizer.decode(predicted_token_ids[0], skip_special_tokens=True)
        generated = generated.split('[SEP]')[0].strip()
        print(f"Generated: {generated}")

if __name__ == '__main__':
    train(0)
    test_prompt = "Looks like playing football, if you can't shoot, pass it to your "
    print(f"\nTest prompt: '{test_prompt}'")
    print("Before training:")
    generate_text(test_prompt)
    print("\n--------------------------------------\n")
    train(3)
    print("\n--------------------------------------\n")
    print("After training:")
    generate_text(test_prompt)