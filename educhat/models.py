import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

MARK_INSTRUCTIONS = """
>>>SYSTEM<<<
You are a teaching assistant, evaluating a student's answer to an exercise.
Give an honest evaluation of the student's answer, based on the answer sheet.
In your answer, you will speak directly to the student. Do not say hello, goodbye, or anything,
just evaluate the task. Be short but concise, short but comprehensive.
Important: end your answer with a mark.

>>>TASK<<<
{task}

>>>GROUND TRUTH SOLUTION<<<
{solution}

>>>MARKING SCHEME<<<
{marking_scheme}
"""

HINT_INSTRUCTIONS = """
>>>SYSTEM<<<
You are a teaching assistant, evaluating a student's answer to an exercise.
This time, the student asked for some assistance, because they are stuck.
You are here to provide a hint to the student, to help them solve the task.
Important: **You are not allowed to give the solution away, just give some hints.**

>>>TASK<<<
{task}

>>>GROUND TRUTH SOLUTION<<<
{solution}
"""

class Exercise:
    def __init__(self, topic, task, root='res/'):
        self.root = root
        self.topic = topic
        self.task = task
        self.task_content = self.load_tex_file('task.txt')
        self.solution_content = self.load_tex_file('solution.txt')
        self.marking_scheme_content = self.load_tex_file('marking.txt')

    @property
    def name(self):
        return self.task

    def load_tex_file(self, filename):
        file_path = os.path.join(self.root, self.topic, self.task, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
    def describe(self):
        return self.task_content
    
    def get_solution(self):
        return self.solution_content


class TeachingAssistant:
    def __init__(self):
        self.conversation = []
        
    @property
    def marked_task(self):
        return len(self.conversation) > 0
    
    def reset(self):
        self.conversation = []
    
    def chat(self, exercise, student_message):
        if not self.marked_task:
            return self.mark(exercise, student_message)
        else:
            return self.further_discuss(student_message)
    
    def mark(self, exercise, student_answer):
        query = MARK_INSTRUCTIONS.format(
            task=exercise.task_content,
            solution=exercise.solution_content,
            marking_scheme=exercise.marking_scheme_content
        )
        self.conversation = [
            {"role": "system", "content": query},
            {"role": "user", "content": "My solution goes like this: \n" + student_answer}
        ]
        answer = self._answer(self.conversation)
        self.conversation.append(answer)
        return answer['content']

    def hint(self, exercise):
        query = HINT_INSTRUCTIONS.format(
            task=exercise.task_content,
            solution=exercise.solution_content
        )
        hint_conversation = [
            {"role": "system", "content": query},
            {"role": "user", "content" : "Give me some hints."}
        ]
        return self._answer(hint_conversation)['content']
    
    def further_discuss(self, student_message):
        self.conversation.append({"role": "user", "content": student_message})
        answer = self._answer(self.conversation)
        self.conversation.append(answer)
        return answer['content']
    
    def _answer(self, messages):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=128,
            temperature=0.8,
            messages=messages
        )
        answer = completion.choices[0].message
        return answer
