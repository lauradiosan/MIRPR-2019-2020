# Setting the project up.

## Frontend
  0. Go into `frontend`
  1. Install npm + nodejs.
  2. Install elm.
  3. `yarn install` in the frontend directory.
  4. `yarn dev` in the frontend directory to serve the chat on `localhost:8080`.

## Backend
  0. Go into `backend`
  1. `npm install`
  2. `nodejs index.js` to run the backend.

## Python AI
  1. `pip3 install nltk`
  2. Ask if there are any other dependencies.
  3. Install [stanford corenlp](https://stanfordnlp.github.io/CoreNLP/download.html).
  4. Put it someplace.
  5. Edit the server.py in the root of the `mirpr` repository to point to the location of your unzipped corenlp download.
  6. `python3 server.py` to start the thing.

## Order of setup
  1. Python AI (if you haven't already got the corenlp)
  2. Backend.
  3. Frontend.
