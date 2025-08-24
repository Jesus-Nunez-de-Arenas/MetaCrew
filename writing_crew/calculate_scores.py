import os
import glob
import json

def main():
    print("Starting score calculation...")
    questions_file = "trivia_creative_writing_100_n_5.jsonl"
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")
    print(f"Processing questions from {questions_file}")
    
    scores = []
    average_score = 0

    with open(questions_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                question_data = json.loads(line)
                answers = question_data.get("answers", "")
                
                story = 'output_writing/story_' + str(line_num) + '/Review_and_Edit_the_Story.txt'
                
                score = 0
                previous_score = score
                
                for answer in answers:
                    print(f"Processing answer: {answer}")
                    
                    with open(story, "r", encoding="utf-8") as story_file:
                        story_text = story_file.read()

                    lowercase_story_text = story_text.lower()
                    
                    for keyword in answers:
                        for specific_keyword in keyword:
                            if str(specific_keyword).lower() in lowercase_story_text:
                                score += 1
                                break
                        if score > previous_score:
                            break
                    
                scores.append({"question_number": line_num, "score": score})
                average_score += score

            except Exception as e:
                print(f"Error processing question at line {line_num}: {e}")
    
    output_file = "scores.json"
    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(scores, out_f, ensure_ascii=False, indent=2)
    print(f"Scores saved to {output_file}")
    average_score /= len(scores) if scores else 1
    print(f"Average score: {average_score}")


if __name__ == "__main__":
    main()