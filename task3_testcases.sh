for dir in quizType*; do
    if [ -d "$dir" ]; then
        diff -q "${dir}.csv" "Type${dir#quizType}_Test_case.csv"
        if [ $? -eq 0 ]; then
            echo "${dir}.csv and Type${dir#quizType}_Test_case.csv are the same"
        else
            echo "${dir}.csv and Type${dir#quizType}_Test_case.csv are different"
        fi
    fi
done
