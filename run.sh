echo "Running Adoptable Doggies"
cd react-frontend
npm run build
cd ..
cd flask-backend
python app.py
cd ..