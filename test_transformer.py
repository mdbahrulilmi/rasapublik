from transformers import TrainingArguments
print(TrainingArguments.__module__)

args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=1,
)
print("Berhasil!")
