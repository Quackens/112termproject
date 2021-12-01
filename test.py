hwAverage = 98.9       # This is the number you see in autolab
quizAverage = 90.2       # The number in autolab will change a tiny bit because of TP1/TP2
midtermAverage = 90.7    # This is the number you see in autolab
final = midtermAverage # Can replace with a hypothetical final exam score or keep as the midterm average
tp = 80                # Replace with a hypothetical TP score

grade = (0.3 * hwAverage) + (0.1 * quizAverage) + (0.2 * midtermAverage) + (0.2 * final) + (0.2 * tp)

if grade >= 89.5:
    print("A", grade)
elif grade >= 79.5:
    print("B", grade)
elif grade >= 69.5:
    print("C", grade)
elif grade >= 59.5:
    print("D", grade)
else:
    print("R", grade)