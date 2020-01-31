echo "Running Adoptable Doggies"
cd react-frontend
#rm -r build
yarn run build
cd ..
cd flask-backend
python app.py
cd ..