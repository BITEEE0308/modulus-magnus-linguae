import pandas as pd 
import matplotlib.pyplot as plt
import os
# text-ada-001.capitvlvm_1.style1.quizTypeA.json

roman_to_decimal = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
}

def create_pivot_table(df, index, columns, values): 
    df = df.groupby([index, columns])[values].mean().reset_index() 
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df


# iterate through all the files in results folder
directory = 'results'
data = []
for filename in os.listdir(directory):
    filePath = os.path.join(directory, filename)
    if os.path.isfile(filePath):
        with open(filePath) as f:
            rate = f.read()
            try:
                accuracy = float(rate)
            except ValueError:
                print(f"Could not convert {rate} to float. Skipping...")
                continue
        chapter, question_type, style, model, quiz_type = filename.split(".")[0:5]
        data.append([model, chapter, style, quiz_type, question_type, accuracy])


# making data frame
# text-ada-001.CAPITVLVM_I.style9.mc.PENSVM-A.json
df = pd.DataFrame(data, columns=["model", "chapter", "style", "quiz_type", "question_type", "accuracy"])
df['chapter'] = df['chapter'].str.split('_').str[1].map(roman_to_decimal)
print(df)
# pivoting to make specific tables

# model chapter table
pivot_df_model_chapter = create_pivot_table(df, 'model', 'chapter', 'accuracy')
pivot_df_model_chapter.to_csv('results-model-chapter.csv')

# model chapter plot
pivot_df_model_chapter.T.plot(kind='line').set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter')
plt.legend(title='Model', loc='upper right')
plt.savefig('model_chap.png')

# prompt quiz type table fixing ada
ada_df = df[df['model'] == 'text-ada-001']

pivot_df_style_quiztype = create_pivot_table(ada_df, 'style', 'quiz_type', 'accuracy')
pivot_df_style_quiztype.to_csv('results-style-quiz_type-ada.csv')

# question_type model table
pivot_df_model_question_type = create_pivot_table(df, 'model', 'question_type', 'accuracy')
pivot_df_model_question_type.to_csv('results-model-questionType.csv')

# chapter quiz type table
pivot_df_chapter_quiztype = create_pivot_table(df, 'chapter', 'quiz_type', 'accuracy')
pivot_df_chapter_quiztype.to_csv('results-chapter-quiz_type.csv')


