for dir in PENSVM-*; do
    if [ -d "$dir" ]; then
	    python3 training_testing_data.py $dir 
    fi
done
