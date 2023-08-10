find ./src/jobs -type f -name "notebook.ipynb" -exec bash -c '{
  file="$1"
  echo "Processing $file"  
  jupyter nbconvert $file --to python --output=script.py
}' _ {} \;