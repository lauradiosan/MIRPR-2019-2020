const WebSocket = require('ws');
const shelljs = require('shelljs');
const database = require("./database.js");

const execCmd = content => {
  const cmd = "python3 ./ai-text-processor/main.py '" + content.replace(/[']/g, '') + "'";
  return shelljs.exec(cmd, { silent: false }).stdout;
};

const execModel2 = content => {
  const cmd = "python3 ./intent_classification_cloud_approach/main_intent.py '" + content.replace(/[']/g, '') + "'";
  return shelljs.exec(cmd, {silent: false}).stdout;
};

const wss = new WebSocket.Server({ port: 5000, host: '0.0.0.0' });

function abs(n) {
  if (n < 0) {
    return -n;
  }

  return n;
}

function calcScore(properties, struct) {
  let score = 0;

  for (let i = 0; i < struct.length; i++) {
    const currentStruct = struct[i];
    if (typeof currentStruct === 'string') continue;
    const propName = currentStruct.prop ? currentStruct.prop.props : '';
    const propScore = currentStruct.chance;

    const matchingProperty = abs((properties[propName] || 0) - propScore);

    // We basically penalize properties based on how much they differ.
    // The one penalized the least is the one with the highest score.
    score -= matchingProperty;
  }

  return score;
}

function interpretModality(struct, db) {
  if (db.length == 0) {
    return 'NONE';
  }

  let bestSolution = db[0].location;
  let bestScore = calcScore(db[0].properties, struct);

  for (let i = 1; i < db.length; i++) {
    let currentScore = calcScore(db[i].properties, struct);

    if (currentScore > bestScore) {
      bestScore = currentScore;
      bestSolution = db[i].location;
    }
  }

  return bestSolution;
}

function calcGraph(properties, graph) {
  let score = 0;

  for (let i = 0; i < graph.length; i++) {
    let prop = graph[i].word;
    let rank = graph[i].weight;

    score -= abs((properties[prop] || 0) - rank);
  }

  return score;
}

function interpretGraph(struct, db) {
  let bestSolution = db[0].location;
  let bestScore = calcGraph(db[0].properties, struct);

  for (let i = 1; i < db.length; i++) {
    let currentScore = calcGraph(db[i].properties, struct);

    if (currentScore > bestScore) {
      bestScore = currentScore;
      bestSolution = db[i].location;
    }
  }

  return bestSolution;
}

function calcFlat(properties, flatTags) {
  let score = 0;

  for (let i = 0; i < flatTags.length; i++) {
    tag = flatTags[i];

    score += properties[tag] || 0;
  }

  return score;
}

function interpretFlatTags(flatTags, db) {
  let bestSolution = db[0].location;
  let bestScore = calcFlat(db[0].properties, flatTags);

  for (let i = 1; i < db.length; i++) {
    let currentScore = calcFlat(db[i].properties, flatTags);

    if (currentScore > bestScore) {
      bestScore = currentScore;
      bestSolution = db[i].location;
    }
  }

  return bestSolution;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function suggest(msg, ws) {
  try {
    const result = JSON.parse(execCmd(msg));

    // Simulate some entropy.
    shuffleArray(database.database);
    const modality = interpretModality(result.modality, database.database);
    console.log(modality);
    shuffleArray(database.database);
    const depGraph = interpretGraph(result.depGraph, database.database);
    console.log(depGraph);
    shuffleArray(database.database);
    const flatTags = interpretFlatTags(result.flatTags, database.database);
    console.log(flatTags);

    const locations = [...new Set([modality, depGraph, flatTags])].join("; ");

    ws.send(`This is what I suggest: ${locations}`);
  } catch (e) {
    console.log(e);
  }
}

wss.on('connection', ws => {
  let AWAIT_DIRECTION = 0;
  let SEARCH = 1;
  let LIST = 2;
  let REVIEW = 3;
  let REVIEW_DESCRIPTION = 4;
  let reviewLocation = '';

  let currentState = 0;

  ws.on('message', data => {
    const msg = JSON.parse(data).message;

    if (currentState == SEARCH) {
      currentState = AWAIT_DIRECTION;
      suggest(msg, ws);
    }
    else if (currentState == REVIEW) {
      currentState = AWAIT_DIRECTION;
      ws.send(`How was ${msg}? Did you like it?`);
    }
    else if (currentState == REVIEW_DESCRIPTION) {
      ws.send('Alright, noted that one down!');
    }
    else {
      let result = JSON.parse(execModel2(msg));
      let intent = result['classifications'][0]['tag_name'];

      if (intent === 'vacation_review') {
        currentState = REVIEW;
        ws.send('What was the location that you want to review?')
      }
      else if (intent === 'vacation_list') {
        let names = database.database.slice(0, 3);
        for ( let i = 0; i < names.length; i++ ) {
          names[i] = names[i].location;
        }

        ws.send('Here are some places you may find interesting: ' + names.join("; "));
        shuffleArray(database.database);
      }
      else {
        currentState = SEARCH;
        ws.send('Please describe your dream holiday place!');
      }
    }
  });

  ws.send("Hello! I'm a chatbot. What would you want to do?");
});
