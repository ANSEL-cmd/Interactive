# Pet Vaccine Record Log
This is a small interactive tool for pet owners to log and track pet vaccination records.
![Pet Vaccine Record Log screenshot](preview.png)
## Intended user
Pet owners who want a simple local tool to record vaccine dates and check vaccine expiry status.
## Main interaction
Users fill in the form: pet name, vaccine name, vaccination date and select a pixel pet avatar.
The form supports adding multiple vaccine entries for the same pet in one submission.
After submitting the form, a new vaccine card will appear. The program automatically calculates days since vaccination and shows colour-coded status: valid / soon due / expired.
Users can delete single records or reset all records.
If the user submits empty pet name or empty vaccine name, the program shows a warning message.
## How to run
1. Clone this repository to local
2. Enter the project folder in terminal
3. Run with uv:
```bash
uv run streamlit run app.py
