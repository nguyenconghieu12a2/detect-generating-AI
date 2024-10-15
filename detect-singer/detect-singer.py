import asyncio
import openai
import csv
import os
from dotenv import load_dotenv

class HANDLER:

    @staticmethod
    def remove_empty_lines(content):
        lines = content.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)

    # Ask CHAT GPT
    @staticmethod
    def ask_gpt(song_name):
        try:
            prompt_message = [
                {
                    "role": "system",
                    "content": "You are an expert at finding singers based on song names."
                },
                {
                    "role": "user",
                    "content": "Based on the song title below. Please give me the name of that singer. Note: for the returned results, just give me the name of singer, no explanation needed.\n This is the song name: " 
                    + song_name
                }
            ]
            response = openai.chat.completions.create(
                model=os.getenv("MODEL_GPT4"), messages=prompt_message,temperature=0 
            )
            assistant_reply = response.choices[0].message.content
            return assistant_reply
        except Exception as e:
            return  "Error: The prompt length exceeds the maximum allowed length of 8192 tokens."

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
                    + " <"
                    + row[1]
                    + "> "
                    + "______________"
                )
                gpt_result = HANDLER().ask_gpt(row[1])
                row[headers.index("AI Gen")] = HANDLER().remove_empty_lines(
                    gpt_result
                )
                writer.writerow(row)
                print("~~~~~~~~~~~~~ Success ~~~~~~~~~~~~~\n")

async def main():
    load_dotenv()
    
    openai.api_key = os.getenv("OPENAI_API_KEY")

    input_csv_path = "D:\\CV\\CV-Project\\detect-singer\\singer_sample.csv"
    output_csv_path = "D:\\CV\\CV-Project\\detect-singer\\detect_singer_result.csv"
    # input_csv_path = "detect_singer.csv"
    # output_csv_path = "detect_singer_result.csv"

    await HANDLER().loop_csv(input_csv_path, output_csv_path)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

