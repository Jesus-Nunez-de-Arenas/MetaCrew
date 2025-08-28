import os
import json

def main():

    for plan_number in range(1, 181):
        plan_name = f'plan_{plan_number}'
        generated_plan_file = f'output_travel/generated_{plan_name}.json'
        plan_file = f'output_travel/{plan_name}/arrange_transportation.txt'

        print(f"Checking plan_file: {plan_file}")

        if os.path.exists(plan_file):
            print(f"Found: {plan_file}")
            with open(plan_file, 'r', encoding='utf-8') as f:
                txt_content = f.read()

            print(f"Content of {plan_file} loaded.")

            data = {
                "gpt-4o-mini_direct_sole-planning_results": txt_content
            }
            data = [data]

            with open(generated_plan_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Written JSON to {generated_plan_file}")
        else:
            print(f"File does not exist: {plan_file}")

if __name__ == "__main__":
    main()