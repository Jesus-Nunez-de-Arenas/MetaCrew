import os
import glob
import json

def main():
    print("Starting score calculation...")
    questions_file = "codenames_50.jsonl"
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")
    print(f"Processing questions from {questions_file}")
    
    scores = []
    average_score = 0
    number_target_words = 0

    with open(questions_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                question_data = json.loads(line)
                target_words = question_data.get("target_words", "")


                answer_file_path = 'output_codenames/question_' + str(line_num) + '/prepare_results.txt'
                score = 0

                for target_word in target_words:
                    print(f"Processing target word: {target_word}")

                    with open(answer_file_path, "r", encoding="utf-8") as file_answer:
                        answers = file_answer.read()

                    lowercase_answers = answers.lower()

                    if str(target_word) in lowercase_answers:
                        score += 1

                scores.append({"question_number": line_num, "score": score})
                average_score += score
                number_target_words += len(target_words)

            except Exception as e:
                print(f"Error processing question at line {line_num}: {e}")
    
    output_file = "scores.json"
    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(scores, out_f, ensure_ascii=False, indent=2)
    print(f"Scores saved to {output_file}")
    print(f"Average score: {average_score}")
    print(f"Number of target words: {number_target_words}")


if __name__ == "__main__":
    main()