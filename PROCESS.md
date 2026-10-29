## 1. Starting idea

I wanted to make a simple webpage for pet owners to keep track of vaccination dates. I have two cats myself, and I know how easy it is to lose track of when their jabs were given and when booster shots are due if I don’t write it down. A straightforward log that lets you instantly see whether a vaccine is still valid would be really handy. I’ve always liked the relaxed, informal look of a paper notebook, so I settled on that visual direction, paired with clear status labels rather than walls of raw data.

## 2. Design and code decisions

**Shifting from a clinical look to something more casual.** My first prototype just used Streamlit’s default plain layout. It worked, but it felt stark and impersonal. I wrote some custom CSS to change that: a cream background, gentle muted colours, and separate memo-style cards for each pet. The colour-coded status tags grab attention straight away, and the card layout keeps each pet’s records neatly apart, instead of lining everything up like rows in a database.

**Working without permanent storage.** All records live in Streamlit’s session state, which means everything disappears once the page refreshes. Adding a full database would have made the project far more complicated than it needed to be for this task. As a practical workaround, I built a PNG export option so users can save a static snapshot of their records. I noted this limitation openly in the README.

**One shared function to calculate vaccine status.** At the beginning, I wrote the status-checking logic twice — once for what appears on screen, and again for the exported PNG. That created a risk that the two versions would give conflicting results. I tidied this up by moving the logic into one reusable `get_status()` function. Any date the user submits gets passed into this function, which returns one of four statuses and sets the matching label colour.

**Guarding against user mistakes.** The tool won’t save entries if the pet name or vaccine name is blank, and it stops you from adding a pet with a name that already exists, showing a warning message instead. You also have to tick a confirmation box before wiping all records, to stop anyone from deleting everything by accident.

## 3. User trial and iteration

I sent the live demo link to a friend and asked her to try it out, without walking her through how it worked beforehand.
She found the input form without trouble, understood what the coloured status tags meant, and managed to export her record successfully. The only moment she paused was when downloading the PNG, but she worked it out quickly.
She said the instructions were easy to follow and the export flow felt smooth. I decided to keep the two-step export design, because it helps the page stay responsive even when there are lots of vaccine entries. I didn’t change anything on the interface; I only updated the README to spell out the storage limitation more clearly.

## 4. AI tools

I used Doubao and DeepSeek at different points while building this project.
**Doubao:** It helped me pick Streamlit for fast prototyping, and generated the first working version of the code for me to test and adjust locally.
**DeepSeek:** It helped me review my code and fix bugs.

- Adopted: Its solution for the PNG download button vanishing, by storing the image bytes inside `st.session_state`.
- Modified: Its original code treated future appointment dates as valid, so I added a separate “Scheduled” status for upcoming vaccinations.
- Modified: Early versions had no way to delete individual vaccine entries, which felt awkward to use. I added this feature.
- Modified: Once delete controls were in place, there was a risk of accidentally clearing everything, so I added confirmation prompts.
- Rejected: Its suggestion to use a SQLite database, which would have added unnecessary complexity.

## 5. Development history and credits

The commit history of this repository shows how the project evolved: starting from a basic input form, adding support for multiple vaccine entries, introducing colour-coded memo cards, then implementing fixes for future date handling, PNG export and single-record deletion.

Credits:

- Built from scratch for Assignment 3.
- Pixel pet avatars are original ASCII art made for this project.
- Developed with Streamlit and Matplotlib.
- No third-party code, assets or media were copied.