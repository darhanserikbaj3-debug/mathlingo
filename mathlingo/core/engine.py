import re
import random

def validate_format(func):
    """Decorator ensuring evaluating elements strictly parse safely."""
    def wrapper(self, user_input, *args, **kwargs):
        if not re.match(r'^-?\d+(\.\d+)?$', str(user_input).strip()):
            return False 
        return func(self, user_input, *args, **kwargs)
    return wrapper

class MathEngine:
    def __init__(self):
        self.QUESTION_BANK = {
            "Arithmetic": {
                1: [
                    {"question": "Find the value of:\n12 + 15", "answer": 27, "options": ["22", "27", "35", "19"]},
                    {"question": "Find the value of:\n45 - 18", "answer": 27, "options": ["27", "31", "23", "17"]},
                    {"question": "Find the value of:\n6 * 7", "answer": 42, "options": ["36", "48", "42", "54"]},
                    {"question": "Find the value of:\n32 / 4", "answer": 8, "options": ["6", "8", "12", "4"]}
                ],
                2: [
                    {"question": "Find the value of:\n14 * 3", "answer": 42, "options": ["36", "48", "42", "52"]},
                    {"question": "Find the value of:\n125 / 5", "answer": 25, "options": ["20", "25", "15", "30"]},
                    {"question": "Find the value of:\n89 - 44", "answer": 45, "options": ["45", "35", "55", "41"]},
                    {"question": "Find the value of:\n72 + 39", "answer": 111, "options": ["101", "111", "121", "109"]}
                ]
            },
            "Powers": {
                1: [
                    {"question": "Evaluate the expression:\n2 to the power of 3", "answer": 8, "options": ["6", "8", "16", "12"]},
                    {"question": "Evaluate the expression:\n3 to the power of 2", "answer": 9, "options": ["6", "9", "12", "27"]},
                    {"question": "Evaluate the expression:\n5 to the power of 2", "answer": 25, "options": ["10", "20", "25", "30"]},
                    {"question": "Evaluate the expression:\n10 to the power of 2", "answer": 100, "options": ["20", "100", "1000", "50"]}
                ],
                2: [
                    {"question": "Evaluate the expression:\n2 to the power of 5", "answer": 32, "options": ["25", "10", "32", "64"]},
                    {"question": "Evaluate the expression:\n4 to the power of 3", "answer": 64, "options": ["12", "48", "64", "32"]},
                    {"question": "Evaluate the expression:\n3 to the power of 4", "answer": 81, "options": ["12", "27", "64", "81"]},
                    {"question": "Evaluate the expression:\n6 to the power of 3", "answer": 216, "options": ["18", "196", "216", "256"]}
                ]
            },
            "Equations": {
                1: [
                    {"question": "Solve for x:\n2x + 4 = 10", "answer": 3, "options": ["2", "3", "4", "5"]},
                    {"question": "Solve for x:\n3x - 5 = 10", "answer": 5, "options": ["3", "4", "5", "6"]},
                    {"question": "Solve for x:\n5x + 2 = 22", "answer": 4, "options": ["3", "4", "5", "6"]},
                    {"question": "Solve for x:\n4x - 8 = 12", "answer": 5, "options": ["4", "5", "6", "3"]}
                ],
                2: [
                    {"question": "Solve for x:\n7x + 9 = 30", "answer": 3, "options": ["2", "3", "4", "5"]},
                    {"question": "Solve for x:\n6x - 12 = 24", "answer": 6, "options": ["4", "5", "6", "7"]},
                    {"question": "Solve for x:\n9x + 4 = 40", "answer": 4, "options": ["3", "4", "5", "6"]},
                    {"question": "Solve for x:\n12x - 7 = 77", "answer": 7, "options": ["6", "7", "8", "9"]}
                ]
            },
            "Algebra": {
                1: [
                    {"question": "Evaluate the expression:\n3x + 4x, when x = 3", "answer": 21, "options": ["12", "18", "21", "24"]},
                    {"question": "Simplify and evaluate:\n5x - 2x, when x = 6", "answer": 18, "options": ["12", "15", "18", "24"]},
                    {"question": "Evaluate the expression:\n2x + 10, when x = 7", "answer": 24, "options": ["20", "24", "28", "32"]},
                    {"question": "Simplify and evaluate:\n4x + 2x - 3, when x = 2", "answer": 9, "options": ["7", "9", "11", "13"]}
                ],
                2: [
                    {"question": "Evaluate the expression:\nx² + 3x, when x = 4", "answer": 28, "options": ["16", "24", "28", "32"]},
                    {"question": "Evaluate the expression:\n2x² - 5, when x = 3", "answer": 13, "options": ["11", "13", "15", "17"]},
                    {"question": "Evaluate the expression:\n(x + 2)(x - 1), when x = 5", "answer": 28, "options": ["24", "28", "32", "35"]},
                    {"question": "Evaluate the expression:\n3x² + 2x + 1, when x = 2", "answer": 17, "options": ["13", "15", "17", "19"]}
                ]
            },
            "Geometry": {
                1: [
                    {"question": "Find the area of a rectangle\nwith width = 5 and height = 8", "answer": 40, "options": ["13", "26", "35", "40"]},
                    {"question": "Find the perimeter of a square\nwith side length = 6", "answer": 24, "options": ["12", "24", "36", "48"]},
                    {"question": "Find the area of a triangle\nwith base = 4 and height = 10", "answer": 20, "options": ["14", "20", "40", "25"]},
                    {"question": "Find the perimeter of a rectangle\nwith width = 3 and length = 7", "answer": 20, "options": ["10", "14", "20", "21"]}
                ],
                2: [
                    {"question": "Find the volume of a cube\nwith side length = 4", "answer": 64, "options": ["16", "24", "48", "64"]},
                    {"question": "Find the hypotenuse of a right triangle\nwith sides 3 and 4", "answer": 5, "options": ["5", "6", "7", "25"]},
                    {"question": "Find the surface area of a cube\nwith side length = 3", "answer": 54, "options": ["27", "36", "54", "72"]},
                    {"question": "Find the volume of a rectangular prism\nwith sides 2, 4, and 5", "answer": 40, "options": ["22", "40", "44", "50"]}
                ]
            },
            "Trigonometry": {
                1: [
                    {"question": "Evaluate the expression:\n10 * sin(30°) + 5", "answer": 10, "options": ["5", "10", "15", "20"]},
                    {"question": "Evaluate the expression:\n6 * cos(0°) - 2", "answer": 4, "options": ["2", "4", "6", "8"]},
                    {"question": "Evaluate the expression:\n4 * tan(45°) + 3", "answer": 7, "options": ["4", "5", "7", "9"]},
                    {"question": "Evaluate the expression:\n8 * sin(90°) + 2", "answer": 10, "options": ["6", "8", "10", "12"]}
                ],
                2: [
                    {"question": "Evaluate the expression:\n12 * sin(30°) + 4 * cos(60°)", "answer": 8, "options": ["6", "8", "10", "12"]},
                    {"question": "Evaluate the expression:\n5 * tan(45°) + 5 * cos(0°)", "answer": 10, "options": ["5", "10", "15", "20"]},
                    {"question": "Evaluate the expression:\n20 * sin(90°) - 10 * sin(30°)", "answer": 15, "options": ["5", "10", "15", "20"]},
                    {"question": "Evaluate the expression:\n16 * cos(60°) + 2 * tan(45°)", "answer": 10, "options": ["8", "10", "12", "14"]}
                ]
            },
            "Probability": {
                1: [
                    {"question": "How many unique outcomes are possible\nwhen flipping 2 fair coins?", "answer": 4, "options": ["2", "4", "6", "8"]},
                    {"question": "How many unique outcomes are possible\nwhen flipping 3 fair coins?", "answer": 8, "options": ["4", "6", "8", "12"]},
                    {"question": "What is the total number of outcomes\nwhen rolling a standard 6-sided die?", "answer": 6, "options": ["4", "6", "12", "36"]},
                    {"question": "If a bag has 3 red and 2 blue marbles,\nwhat is the total number of marbles?", "answer": 5, "options": ["3", "5", "6", "10"]}
                ],
                2: [
                    {"question": "How many unique outcomes are possible\nwhen rolling two standard 6-sided dice?", "answer": 36, "options": ["12", "18", "36", "24"]},
                    {"question": "How many unique outcomes are possible\nwhen flipping 4 fair coins?", "answer": 16, "options": ["8", "12", "16", "32"]},
                    {"question": "A bag has 4 red, 3 blue, and 3 green marbles.\nWhat is the total marble count?", "answer": 10, "options": ["7", "9", "10", "12"]},
                    {"question": "How many face cards (J, Q, K) are present\nin a standard deck of 52 cards?", "answer": 12, "options": ["4", "8", "12", "16"]}
                ]
            },
            "Logic": {
                1: [
                    {"question": "Find the next item in the sequence:\n2, 4, 6, 8, ...", "answer": 10, "options": ["9", "10", "11", "12"]},
                    {"question": "Find the next item in the sequence:\n5, 10, 15, 20, ...", "answer": 25, "options": ["22", "24", "25", "30"]},
                    {"question": "Find the next item in the sequence:\n1, 3, 5, 7, ...", "answer": 9, "options": ["8", "9", "10", "11"]},
                    {"question": "Find the next item in the sequence:\n20, 17, 14, 11, ...", "answer": 8, "options": ["7", "8", "9", "10"]}
                ],
                2: [
                    {"question": "Find the next item in the sequence:\n1, 4, 9, 16, ...", "answer": 25, "options": ["20", "23", "25", "36"]},
                    {"question": "Find the next item in the sequence:\n2, 4, 8, 16, ...", "answer": 32, "options": ["20", "24", "32", "64"]},
                    {"question": "Find the next item in the sequence:\n3, 7, 11, 15, ...", "answer": 19, "options": ["17", "18", "19", "20"]},
                    {"question": "Find the next item in the sequence:\n100, 90, 81, 73, ...", "answer": 66, "options": ["64", "65", "66", "67"]}
                ]
            },
            "Calculus": {
                1: [
                    {"question": "Find the derivative of f(x) = 3x²\nat the evaluation point x = 2", "answer": 12, "options": ["6", "10", "12", "18"]},
                    {"question": "Find the derivative of f(x) = 5x²\nat the evaluation point x = 1", "answer": 10, "options": ["5", "10", "15", "20"]},
                    {"question": "Find the derivative of f(x) = 2x²\nat the evaluation point x = 4", "answer": 16, "options": ["8", "12", "16", "32"]},
                    {"question": "Find the derivative of f(x) = 4x²\nat the evaluation point x = 3", "answer": 24, "options": ["12", "18", "24", "36"]}
                ],
                2: [
                    {"question": "Find the derivative of f(x) = 2x³\nat the evaluation point x = 2", "answer": 24, "options": ["12", "16", "24", "32"]},
                    {"question": "Find the derivative of f(x) = x³\nat the evaluation point x = 3", "answer": 27, "options": ["9", "18", "27", "81"]},
                    {"question": "Find the derivative of f(x) = 4x³\nat the evaluation point x = 1", "answer": 12, "options": ["4", "8", "12", "16"]},
                    {"question": "Find the derivative of f(x) = 3x³\nat the evaluation point x = 2", "answer": 36, "options": ["18", "24", "36", "54"]}
                ]
            },
            "Discrete Math": {
                1: [
                    {"question": "Evaluate the discrete factorial expression:\n3!", "answer": 6, "options": ["3", "6", "9", "12"]},
                    {"question": "Evaluate the discrete factorial expression:\ = \n4!", "answer": 24, "options": ["12", "16", "24", "48"]},
                    {"question": "Evaluate the discrete factorial expression:\n5!", "answer": 120, "options": ["60", "100", "120", "150"]},
                    {"question": "Evaluate the discrete factorial expression:\n2!", "answer": 2, "options": ["1", "2", "4", "6"]}
                ],
                2: [
                    {"question": "Evaluate the structural combination:\nCombinations of 4 items chosen 2 at a time (4C2)", "answer": 6, "options": ["4", "6", "8", "12"]},
                    {"question": "Evaluate the structural combination:\nCombinations of 5 items chosen 2 at a time (5C2)", "answer": 10, "options": ["5", "10", "15", "20"]},
                    {"question": "Evaluate the structural combination:\nCombinations of 6 items chosen 2 at a time (6C2)", "answer": 15, "options": ["12", "15", "18", "30"]},
                    {"question": "Evaluate the discrete factorial expression:\n6!", "answer": 720, "options": ["360", "540", "720", "1440"]}
                ]
            },
            "Real World Math": {
                1: [
                    {"question": "An item costs $100. After a\n20% discount, what is the final price?", "answer": 80, "options": ["20", "70", "80", "90"]},
                    {"question": "An item costs $50. After a\n10% discount, what is the final price?", "answer": 45, "options": ["40", "45", "48", "49"]},
                    {"question": "An item costs $200. After a\n50% discount, what is the final price?", "answer": 100, "options": ["50", "100", "150", "180"]},
                    {"question": "An item costs $500. After a\n20% discount, what is the final price?", "answer": 400, "options": ["300", "380", "400", "420"]}
                ],
                2: [
                    {"question": "If you leave a 15% tip on a $60 meal,\nwhat is the total bill amount?", "answer": 69, "options": ["66", "68", "69", "75"]},
                    {"question": "If you leave an 18% tip on a $50 meal,\nwhat is the total bill amount?", "answer": 59, "options": ["55", "58", "59", "68"]},
                    {"question": "An item costs $80. If sales tax is 5%,\nwhat is the total cost?", "answer": 84, "options": ["82", "84", "85", "88"]},
                    {"question": "An item costs $120. If sales tax is 10%,\nwhat is the total cost?", "answer": 132, "options": ["130", "132", "140", "142"]}
                ]
            },
            "Competitive Math": {
                1: [
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 10 inclusive.", "answer": 55, "options": ["45", "50", "55", "60"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 20 inclusive.", "answer": 210, "options": ["190", "200", "210", "220"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 5 inclusive.", "answer": 15, "options": ["10", "12", "15", "20"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 12 inclusive.", "answer": 78, "options": ["72", "78", "84", "90"]}
                ],
                2: [
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 40 inclusive.", "answer": 820, "options": ["800", "820", "840", "860"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 30 inclusive.", "answer": 465, "options": ["435", "450", "465", "480"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 50 inclusive.", "answer": 1275, "options": ["1225", "1250", "1275", "1300"]},
                    {"question": "Find the sum of all consecutive integers\nfrom 1 to 15 inclusive.", "answer": 120, "options": ["105", "115", "120", "135"]}
                ]
            }
        }

    def get_fixed_question(self, topic, difficulty_level, progress_score):
        """Fetches the sequential static item corresponding directly to lesson state."""
        question_idx = (progress_score // 25) % 4
        
        target_dataset = self.QUESTION_BANK.get(topic, self.QUESTION_BANK["Arithmetic"])[difficulty_level]
        selected_task = target_dataset[question_idx]
        
        shuffled_options = list(selected_task["options"])
        random.shuffle(shuffled_options)
        
        return {
            "question": selected_task["question"],
            "answer": selected_task["answer"],
            "options": shuffled_options
        }

    @validate_format
    def check_answer(self, user_input, correct_answer):
        return float(user_input.strip()) == float(correct_answer)