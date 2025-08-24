"""
Manual MMMU Crew Implementation
This bypasses CrewAI's LLM integration issues while maintaining the agent workflow structure
"""
import os
import json
from PIL import Image
from io import BytesIO
import base64
from tqdm import tqdm
from custom_tool import LLaVAImageTool
from datasets import load_dataset

def get_last_processed_index(progress_file):
    """Get the last processed index from progress file"""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def update_progress(progress_file, index):
    """Update progress file with current index"""
    os.makedirs(os.path.dirname(progress_file), exist_ok=True)
    with open(progress_file, 'w') as f:
        f.write(str(index))

def read_jsonline(file_path):
    """Read JSONL file"""
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    return data

def write_jsonline(file_path, data):
    """Write data to JSONL file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

class ManualAgent:
    """Simple agent that calls LLaVA directly"""
    
    def __init__(self, name, role, goal, backstory):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
    
    def execute_task(self, task_description, image_tool, context=""):
        """Execute a task using the LLaVA tool"""
        # Combine context and task
        full_prompt = f"""
You are {self.name}, a {self.role}.
Goal: {self.goal}
Backstory: {self.backstory}

Context: {context}

Task: {task_description}

Please analyze the image and provide a detailed response.
"""
        
        try:
            result = image_tool._run(prompt=full_prompt)
            return f"[{self.name}]: {result}"
        except Exception as e:
            return f"[{self.name}] Error: {e}"

class ManualMMmuCrew:
    """Manual implementation of MMMU crew that bypasses CrewAI LLM issues"""
    
    def __init__(self, image_data):
        self.image_tool = LLaVAImageTool(image_base64=image_data)
        self.setup_agents()
    
    def setup_agents(self):
        """Create the 5 agents manually"""
        self.agents = {
            'john_smith': ManualAgent(
                name="John Smith",
                role="Logic and Reasoning Expert",
                goal="Identify entities, variables, and clues from logic puzzles and word problems",
                backstory="You are an expert in logical thinking and problem-solving, with years of experience in analyzing complex scenarios."
            ),
            'larissa_green': ManualAgent(
                name="Larissa Green", 
                role="Relationship Analyst",
                goal="Formulate and map relationships between different elements identified in the problem",
                backstory="You specialize in understanding connections and relationships between different elements in complex problems."
            ),
            'mike_turner': ManualAgent(
                name="Mike Turner",
                role="Solution Generator", 
                goal="Generate possible arrangements and combinations based on identified relationships",
                backstory="You excel at creating systematic approaches to explore all possible solutions."
            ),
            'sophia_brown': ManualAgent(
                name="Sophia Brown",
                role="Validation Specialist",
                goal="Identify valid solutions that satisfy all given constraints and rules",
                backstory="You are meticulous in checking solutions against all given constraints and rules."
            ),
            'ethan_williams': ManualAgent(
                name="Ethan Williams", 
                role="Final Answer Coordinator",
                goal="Coordinate findings from all agents and provide the final answer",
                backstory="You synthesize information from multiple sources to provide clear, accurate final answers."
            )
        }
    
    def process_sample(self, question, options, correct_answer=None):
        """Process a single MMMU sample through all agents"""
        print(f"\n{'='*60}")
        print(f"PROCESSING QUESTION: {question}")
        print(f"OPTIONS: {options}")
        if correct_answer:
            print(f"CORRECT ANSWER: {correct_answer}")
        print(f"{'='*60}")
        
        results = []
        context = ""
        
        # Task 1: John Smith - Identify entities and clues
        task1 = f"Analyze the image and question: '{question}'. Options: {options}. Identify all relevant entities, variables, and clues present in the image."
        result1 = self.agents['john_smith'].execute_task(task1, self.image_tool, context)
        results.append(result1)
        context += f"\n\nJohn's Analysis: {result1}"
        print(f"\n{result1}")
        
        # Task 2: Larissa Green - Formulate relationships  
        task2 = f"Based on John's analysis, formulate relationships between the entities identified. Question: '{question}' Options: {options}"
        result2 = self.agents['larissa_green'].execute_task(task2, self.image_tool, context)
        results.append(result2)
        context += f"\n\nLarissa's Analysis: {result2}"
        print(f"\n{result2}")
        
        # Task 3: Mike Turner - Generate possible arrangements
        task3 = f"Generate possible arrangements or solutions based on the relationships identified. Question: '{question}' Options: {options}"
        result3 = self.agents['mike_turner'].execute_task(task3, self.image_tool, context)
        results.append(result3)
        context += f"\n\nMike's Analysis: {result3}"
        print(f"\n{result3}")
        
        # Task 4: Sophia Brown - Validate solutions
        task4 = f"Validate which of the generated solutions satisfy all constraints. Question: '{question}' Options: {options}"
        result4 = self.agents['sophia_brown'].execute_task(task4, self.image_tool, context)
        results.append(result4)
        context += f"\n\nSophia's Analysis: {result4}"
        print(f"\n{result4}")
        
        # Task 5: Ethan Williams - Final answer
        task5 = f"Based on all previous analyses, provide the final answer. Question: '{question}' Options: {options}. Choose the best answer and explain your reasoning."
        result5 = self.agents['ethan_williams'].execute_task(task5, self.image_tool, context)
        results.append(result5)
        print(f"\n{result5}")
        
        return results

def main():
    """Main function to run the manual MMMU crew"""
    print("Loading MMMU dataset for manual processing...")
    
    # Full MMMU benchmark classes
    all_classes = [
        'Accounting',
        'Agriculture', 
        'Architecture_and_Engineering',
        'Art',
        'Art_Theory',
        'Basic_Medical_Science',
        'Biology',
        'Chemistry',
        'Clinical_Medicine',
        'Computer_Science',
        'Design',
        'Diagnostics_and_Laboratory_Medicine',
        'Economics',
        'Electronics',
        'Energy_and_Power',
        'Finance',
        'Geography',
        'History',
        'Literature',
        'Manage',
        'Marketing',
        'Materials',
        'Math',
        'Mechanical_Engineering',
        'Music',
        'Pharmacy',
        'Physics',
        'Psychology',
        'Public_Health',
        'Sociology'
    ]
    
    output_dir = os.getenv("OUTPUT_DIR", "./output_mmmu/")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📊 Processing {len(all_classes)} MMMU classes for complete benchmark...")
    
    for cla in all_classes:
        print(f"\n🔄 Processing Class: {cla}")
        try:
            while True:
                try:
                    sub_dataset_val = load_dataset('MMMU/MMMU', cla, split='validation', cache_dir="MMMU/dataset")
                    print("Dataset loaded successfully.")
                    break
                except Exception as e:
                    print(f"Failed to load dataset: {e}. Retrying...")
                    continue
            
            total_files = len(sub_dataset_val)
            print(f"Total Files: {total_files}")
            print(f"Processing all {total_files} samples for class {cla}...")
            
            progress_file = f"{output_dir}/progress_manual_crew_{cla}.txt"
            start_index = get_last_processed_index(progress_file)
            dic = []
            result_file_path = f"{output_dir}/result_manual_crew_{cla}.jsonl"
            if os.path.exists(result_file_path):
                already = read_jsonline(result_file_path)
                for data in already:
                    dic.append(data["id"])

            with tqdm(total=total_files, desc=f"Processing {cla}", initial=start_index) as pbar:
                for i in range(start_index, total_files):  # Process all samples
                    try:
                        data = sub_dataset_val[i]

                        if data["id"] in dic:
                            update_progress(progress_file, i + 1)
                            pbar.update(1)
                            continue

                        # Get image and convert to base64
                        image = data['image_1']
                        if image is None:
                            print(f"No image found for sample {i}, skipping...")
                            update_progress(progress_file, i + 1)
                            pbar.update(1)
                            continue
                        
                        buffer = BytesIO()
                        image.save(buffer, format='PNG')
                        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

                        question = data['question']
                        print(f"Question type: {data.get('question_type', 'Unknown')}")
                        
                        # Format options properly
                        try:
                            options_list = eval(data['options']) if isinstance(data['options'], str) else data['options']
                            options = [f"{chr(65 + i)}. {item}" for i, item in enumerate(options_list)]
                            options_str = '\n'.join(options)
                        except:
                            options_str = str(data['options'])
                        
                        answer = data['answer']
                
                        # Create crew and process
                        crew = ManualMMmuCrew(image_data)
                        
                        print(f"\n🚀 Processing sample {i+1}/{total_files} from class {cla}")
                        results = crew.process_sample(question, options_str, answer)
                        
                        # Save results
                        result_data = {
                            "id": data["id"],
                            "class": cla,
                            "question": question,
                            "options": options_str,
                            "correct_answer": answer,
                            "crew_results": results,
                            "final_prediction": results[-1] if results else ""  # Last result is final answer
                        }
                        
                        # Save to JSONL
                        result_file = f"{output_dir}/result_manual_crew_{cla}.jsonl"
                        write_jsonline(result_file, result_data)
                        
                        update_progress(progress_file, i + 1)
                        pbar.update(1)
                        
                        print(f"✅ COMPLETED SAMPLE {i+1}")
                        print("-" * 80)
                        
                    except Exception as e:
                        print(f"❌ Error processing sample {i+1}: {e}")
                        # Still update progress to avoid getting stuck
                        update_progress(progress_file, i + 1)
                        pbar.update(1)
                        continue
            
            print(f"🎉 Finished processing class {cla} - {total_files} samples completed!")
            
        except Exception as e:
            print(f"❌ Fatal error processing class {cla}: {e}")
            print(f"⏭️ Skipping to next class...")
            continue
    
    print("\n" + "="*80)
    print("🎉 COMPLETE MMMU BENCHMARK FINISHED!")
    print(f"📊 Processed {len(all_classes)} classes")
    print("📁 Results saved in:", output_dir)
    print("="*80)

if __name__ == "__main__":
    main()
