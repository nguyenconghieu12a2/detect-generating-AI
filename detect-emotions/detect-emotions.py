import asyncio
import openai
import csv
import os
from dotenv import load_dotenv

class HANDLER:

    # Delete empty line if gpt_result have an empty line in result
    @staticmethod
    def remove_empty_lines(content):
        lines = content.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)

    # Ask CHAT GPT
    @staticmethod
    def ask_gpt(emotion_title):
        try:
            prompt_message = [
                {
                    "role": "system",
                    "content": "You are an translate emotion language machine.",
                },
                {
                    "role": "user",
                    "content": "Based on the title below. Please give me the right emotion of this title. Note: Just give me the result number based on six categories of emotions: sadness (0), joy (1), love (2), anger (3), fear (4), and surprise (5) .Note: Answer with format: 'love', do not write any number in the result.\n This is the title: " 
                    + emotion_title,
                },
            ]
            response = openai.chat.completions.create(
                model=os.getenv("MODEL_GPT4"), messages=prompt_message
            )
            assistant_reply = response.choices[0].message.content
            return assistant_reply
        except Exception as e:
            return "Error: The prompt length exceeds the maximum allowed length of 8192 tokens."

    @staticmethod
    async def loop_csv(input_csv_path, output_csv_path):
        with open(input_csv_path, "r", newline="", encoding="utf-8") as csv_file, open(
            output_csv_path, "w", newline="", encoding="utf-8"
        ) as output_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(output_file)

            headers = next(reader)
            writer.writerow(headers)
        
            for index, row in enumerate(reader):
                print(
                    "\n______________ Run times"
                    + " "
                    + str(index + 1)
                    + "______________"
                )
                gpt_result = HANDLER().ask_gpt(row[1])
                row[headers.index("AI Gen")] = HANDLER().remove_empty_lines(
                    gpt_result
                )
                writer.writerow(row)
                print("~~~~~~~~~~~~~ Emotion: "+ gpt_result +" ~~~~~~~~~~~~~\n")

async def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    input_csv_path = "D:\\CV\\CV-Project\\detect-emotions\\emotions_sample.csv"
    output_csv_path = "D:\\CV\\CV-Project\\detect-emotions\\detect_emotions_result.csv"

    await HANDLER().loop_csv(input_csv_path, output_csv_path)


if __name__ == "__main__":
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
