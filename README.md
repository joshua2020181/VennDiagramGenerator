# VennDiagramGenerator

This is an online Venn Diagram generator to visualize overlapping sets. This was my final project submission for my Discrete Math class in Spring 2021. Below is an example.

![image](https://github.com/user-attachments/assets/d2b11ce5-19f0-4cf4-b4a7-5b8afa63f99a)


## Usage Instructions:
1. Clone this repo
2. *Optional but recommended:* Create a python venv: `python3 -m venv .venv`. Activate it: `source .venv/bin/activate`
3. Install requirements: `pip install django sympy`
4. Run: `python manage.py runserver`
5. Go to `[127.0.0.1:8000](http://127.0.0.1:8000/)`. Some example sets to try: `(A ∩ !(B ∪ C))`, `(A ∪ B) ∩ C`
