for dir in PENSVM-*; do
    if [ -d "$dir" ]; then
	    for FILE in "$dir"/*; do 
	    	python3 get_accuracy.py $FILE $dir 
    	    done
    fi
done
python3 json_to_csv.py
