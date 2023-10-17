from ctransformers import AutoModelForCausalLM

MARK_INSTRUCTIONS = """
>>>SYSTEM<<<
You are a teaching assistant, evaluating a student's answer to an exercise.
Give an honest evaluation of the student's answer, based on the answer sheet.
In your answer, you will speak directly to the student. Do not say hello, goodbye, or anything,
just evaluate the task. Be short but concise, short but comprehensive.
Important: end your answer with a mark.

>>>TASK<<<
{task}

>>>STUDENT ANSWER<<<
{student_answer}

>>>GROUND TRUTH SOLUTION<<<
{solution}

>>>MARKING SCHEME<<<
{marking_scheme}
"""

class Exercise:
    def __init__(self, task_path):
        self.task_path = task_path
        self.task_content = self.load_tex_file('task.tex')
        self.solution_content = self.load_tex_file('solution.tex')
        self.marking_scheme_content = self.load_tex_file('marking.tex')

    def load_tex_file(self, filename):
        file_path = f'{self.task_path}/{filename}'
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
    def describe(self):
        return self.task_content
    
    def get_solution(self):
        return self.solution_content


class TeachingAssistant:
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF", model_type="mistral", gpu_layers=50
        )

    def __call__(self, input_text):
        input_text = input_text.replace("<s>", "<start>")
        input_text = input_text.replace("[INST]", "[instruction]")
        input_text = input_text.replace("[/INST]", "[/instruction]")
        input_text = f"<s> [INST] {input_text} [/INST]"
        output = self.model(input_text)
        return output
    
    def mark(self, exercise, student_answer):
        query = MARK_INSTRUCTIONS.format(
            task=exercise.task_content,
            student_answer=student_answer,
            solution=exercise.solution_content,
            marking_scheme=exercise.marking_scheme_content
        )
        return self(query)
