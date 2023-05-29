for dir in QuizType*; do
    if [ -d "$dir" ]; then
        python3 Task3_sample_code.py "$dir"
    fi
done
